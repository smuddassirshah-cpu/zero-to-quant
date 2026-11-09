/* Weekly mixed review (ENGINE-BACKLOG 820 to 829; docs/AUTHORING.md section 16, "The weekly review").
   Route: #weekly. Today lists it as due work once a week (ZQ.select.cumulativeStatus): seven days after the last one was finished, the first
   seven days after the first level was met. It is not opt-in, and "Not today" only postpones it: it stays due. The 20 items come from
   ZQ.select.weeklyReview (generated Fluency items first, then authored items never seen, then the least recently seen review items, at most
   four from one course), run through ZQ.player.runSet on the shared set page (ZQ.setPage). The result is recorded by ZQ.select.weeklyFinish:
   a history row (date, score, misses per level), authored misses to the redo queue, family counts to the Fluency save. No gate. */
(function () {
  'use strict';
  const ZQ = window.ZQ;

  function mountWeekly(root, Z) {
    const S = () => ZQ.state, esc = Z.esc;
    const courseName = (cid) => { try { return (ZQ.content.course(cid) || {}).name || cid; } catch { return cid; } };
    const levelLines = (byLevel) => Object.entries(byLevel || {}).sort((a, b) => b[1] - a[1] || (a[0] < b[0] ? -1 : 1)).map(([k, n]) => { const i = k.lastIndexOf('/L'); return `${esc(courseName(k.slice(0, i)))}, level ${esc(k.slice(i + 2))}: ${n}`; });
    const hours = (seconds) => { const m = seconds / 60; if (m >= 0.1) { try { S().hours.log({ block: 'review', minutes: m, source: 'weekly-review' }); } catch (e) { console.error(e); } } };
    const cfg = {
      title: 'Weekly mixed review', sub: 'Every level you have met', over: 'This week', heading: 'Weekly mixed review', track: 'maths', perItem: 1, overview: false,
      back: 'today', backLabel: 'Today',
      lede: 'Twenty questions from every level you have met: fresh generated ones first, then questions you have not seen, then those you have seen least recently. It comes round once a week. It locks and unlocks nothing.',
      facts: [['review', 'At most four questions from one course, so no topic crowds out the others.'], ['replay', 'A miss joins your redo queue, back in 7 days.']],
      later: { label: 'Not today', run: () => S().cumulative.postpone() },
      emptyTitle: 'Nothing to review yet', emptyText: 'The weekly review draws on the levels you have met. It arrives a week after the first one.',
      doneTitle: 'Weekly review done', setTitle: 'Weekly review',
      load: () => ZQ.select.weeklyReview(),
      record: (items, res, seconds) => {
        const r = ZQ.select.weeklyFinish(items, res);
        hours(seconds);
        const lines = levelLines(r.byLevel);
        return {
          badges: [[r.queued, r.queued === 1 ? 'miss joins the redo queue' : 'misses join the redo queue'], [Object.keys(r.byLevel).length, Object.keys(r.byLevel).length === 1 ? 'level with a miss' : 'levels with a miss']],
          note: lines.length ? `Misses by level: ${lines.join('; ')}. The next review comes in seven days.` : 'Every question right. The next review comes in seven days.',
        };
      },
      partial: (items, res, seconds) => { ZQ.select.weeklyFinish(items, res, { partial: true }); hours(seconds); },
    };
    return ZQ.setPage(root, Z, cfg);
  }

  ZQ.screen({ id: 'weekly', title: 'Weekly mixed review', group: 'Practice', hidden: true, shell: false, render: (root, Z) => mountWeekly(root, Z) });
})();
