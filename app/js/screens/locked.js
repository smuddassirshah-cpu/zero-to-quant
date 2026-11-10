/* The locked card (ENGINE-BACKLOG 483; docs/AUTHORING.md section 11). ZQ.lockedCard(host, spec) draws what is missing before a
   lesson, review, homework or mock opens, from ZQ.prereq: grouped Stage, then Topic, then Course, then level or lesson, each
   with a count. Direct prerequisites come first and are open; indirect ones collapse to one line per stage. "Start here" is the
   primary button. Each missing level offers "Test out" (#testout/<course>/<n>). Outside Strict mode "Open anyway" records the
   override and opens the target. spec: { title, route, openKey, missing, back } where route is the hash to open and openKey the
   state.prereq.opened key (a level key, or exam/<id>). Selectors carry the lk- prefix. */
(function () {
  'use strict';
  const Z = window.ZQ;

  const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
  const hoursLeft = (t) => { const h = Math.max(1, Math.ceil((t - Date.now()) / 3600e3)); return h === 1 ? 'about an hour' : `${h} hours`; };

  /* One missing level or lesson */
  const row = (nd, esc) => {
    let st;
    if (nd.kind === 'lesson') st = nd.done ? 'finished, quiz not passed yet' : 'not finished';
    else {
      const bits = [`${nd.lessonsDone} of ${nd.lessonsWritten} lessons finished`];
      if (nd.lessonsWritten < nd.lessonsTotal) bits.push(`${nd.lessonsTotal - nd.lessonsWritten} not yet written`);
      bits.push(nd.reviewWritten ? 'review not passed' : 'no review written yet');
      if (nd.perf && !nd.perf.passed) bits.push('performance task not passed');   // ENGINE-BACKLOG 529
      st = nd.lessonsWritten === 0 && !nd.reviewWritten ? 'not yet written' : bits.join(', ');
    }
    const t = nd.testOut;
    const to = nd.kind === 'lesson' ? '' : nd.lessonsWritten === 0 && !t.written ? `<span class="t-caption muted lk-wait">Not yet written: this opens when it is written</span>` : t.can ? `<button type="button" class="btn secondary lk-testout" data-testout="${esc(nd.course)}/${nd.n}">Test out</button>`
      : t.nextAt ? `<span class="t-caption muted lk-wait">Test out again in ${hoursLeft(t.nextAt)}</span>`
      : `<span class="t-caption muted lk-wait">Finish its lessons to unlock it</span>`;
    const title = nd.kind === 'lesson' ? `Lesson: ${nd.name}` : `Level ${nd.n}${nd.levelName ? ': ' + nd.levelName : ''}`;
    const why = nd.why ? `<p class="t-caption secondary lk-why">${esc(nd.why)}</p>` : '';   // one line from course.json (ENGINE-BACKLOG 551)
    return `<li class="lk-row" data-ref="${esc(nd.ref)}"><div class="lk-row-t"><a class="lk-row-n" href="#course/${esc(nd.course)}">${esc(title)}</a><span class="t-caption secondary">${esc(st)}</span></div>${why}${to}</li>`;
  };
  /* Stage > Topic > Course groups, open, each with a count */
  const tree = (nodes, esc) => {
    const stages = new Map();
    nodes.forEach(nd => {
      const s = stages.get(nd.stage) || stages.set(nd.stage, new Map()).get(nd.stage);
      const t = s.get(nd.topic) || s.set(nd.topic, { name: nd.topicName, courses: new Map() }).get(nd.topic);
      (t.courses.get(nd.course) || t.courses.set(nd.course, { name: nd.courseName, nodes: [] }).get(nd.course)).nodes.push(nd);
    });
    const count = (n) => plural(n, 'item', 'items');
    return [...stages.entries()].map(([sid, topics]) => {
      const n = [...topics.values()].reduce((a, t) => a + [...t.courses.values()].reduce((b, c) => b + c.nodes.length, 0), 0);
      return `<details class="lk-g lk-stage" open><summary><span class="lk-g-n">Stage ${esc(sid)}</span><span class="lk-g-c tnum">${count(n)}</span></summary>${[...topics.entries()].map(([tid, t]) => {
        const tn = [...t.courses.values()].reduce((b, c) => b + c.nodes.length, 0);
        return `<details class="lk-g lk-topic" open><summary><span class="lk-g-n">${esc(tid)} ${esc(t.name)}</span><span class="lk-g-c tnum">${count(tn)}</span></summary>${[...t.courses.entries()].map(([cid, c]) =>
          `<details class="lk-g lk-course" open><summary><span class="lk-g-n">${esc(c.name)}</span><span class="lk-g-c tnum">${count(c.nodes.length)}</span></summary><ul class="lk-rows">${c.nodes.map(nd => row(nd, esc)).join('')}</ul></details>`).join('')}</details>`;
      }).join('')}</details>`;
    }).join('');
  };

  /* "Check first" lines for diagnostic requires (gate: false): never a lock, the reason and a link to sit that level's review */
  Z.checkFirst = (nodes, esc) => (nodes || []).map(nd => {
    const name = nd.kind === 'lesson' ? nd.name : `${nd.courseName}, level ${nd.n}`;
    return `<p class="t-caption secondary lk-check" data-ref="${esc(nd.ref)}"><b>Check first:</b> ${esc(name)}${nd.why ? `. ${esc(nd.why)}` : ''}${nd.route ? ` <a href="#${esc(nd.route)}">Sit its review as a check</a>` : ''}</p>`;
  }).join('');
  /* "Route limited: X unwritten", one chip per course */
  Z.routeLimited = (list, esc) => (list || []).map(c => `<span class="rl-chip" data-course="${esc(c.course)}">${Z.icon('lock', 'xs')}<span>${esc(Z.prereq.routeText(c))}</span></span>`).join('');

  Z.lockedCard = function (host, spec) {
    const esc = Z.esc, S = Z.state, P = Z.prereq;
    const m = spec.missing, back = spec.back || '#learn';
    const strict = P.strict();
    const direct = m.direct.length ? `<section class="lk-sec" aria-labelledby="lk-direct-h"><h2 class="t-h2" id="lk-direct-h">Finish these first <span class="lk-n tnum">${m.direct.length}</span></h2>${tree(m.direct, esc)}</section>` : '';
    const byStage = new Map();
    m.indirect.forEach(nd => (byStage.get(nd.stage) || byStage.set(nd.stage, []).get(nd.stage)).push(nd));
    const indirect = m.indirect.length ? `<section class="lk-sec" aria-labelledby="lk-ind-h"><h2 class="t-h2" id="lk-ind-h">What those need in turn <span class="lk-n tnum">${m.indirect.length}</span></h2>${[...byStage.entries()].map(([sid, nds]) =>
      `<details class="lk-more" data-stage="${esc(sid)}"><summary>and ${nds.length} more in Stage ${esc(sid)}</summary>${tree(nds, esc)}</details>`).join('')}</section>` : '';
    const start = m.start ? `<button type="button" class="btn lg lk-start" data-start="${esc(m.start.route)}">Start here</button><p class="t-caption secondary lk-start-c">${esc(m.start.label)}${m.start.node.kind === 'level' ? `, ${esc(m.start.node.courseName)} level ${m.start.node.n}` : ''}</p>` : '';
    host.innerHTML = `<div class="lk">
      <a class="lk-back" href="${esc(back)}">${Z.icon('chevronL', 'sm')}<span>Back</span></a>
      <header class="lk-head"><span class="lk-ic" aria-hidden="true">${Z.icon('lock')}</span>
        <span class="t-overline muted">Locked</span>
        <h1 class="t-h1">${esc(spec.title)}</h1>
        <p class="t-body secondary">${plural(m.count, 'thing', 'things')} to finish before this opens. Each one is used by what comes after it, so a solid base saves you coming back.</p>
        ${start}
        ${spec.limits && spec.limits.length ? `<div class="rl-row">${Z.routeLimited(spec.limits, esc)}</div>` : ''}
      </header>
      ${spec.check && spec.check.length ? `<section class="lk-sec lk-checks">${Z.checkFirst(spec.check, esc)}</section>` : ''}
      ${direct}${indirect}
      <footer class="lk-foot">
        <p class="t-caption muted">A level counts as met when you pass its review, pass the topic exam or stage test, or test out of it. Opening a lesson does not count. Nothing you have unlocked locks again.</p>
        ${strict ? '<p class="t-caption muted lk-strict">Strict prerequisites are on, so a locked lesson cannot be opened early. You can switch this off under You, Settings.</p>'
          : `<div class="lk-open"><button type="button" class="btn secondary" data-open>Open anyway</button><p class="t-caption muted">Opens it and counts it under Opened early on You.</p></div>`}
      </footer></div>`;
    Z.mathify(host);
    const onClick = (e) => {
      const go = e.target.closest('[data-start]');
      if (go) { Z.sound('tap'); Z.go(go.dataset.start); return; }
      const to = e.target.closest('[data-testout]');
      if (to) { Z.go('testout/' + to.dataset.testout); return; }
      if (e.target.closest('[data-open]') && !P.strict()) { S.prereq.open(spec.openKey); Z.go(spec.route); }
    };
    host.addEventListener('click', onClick);
    return () => host.removeEventListener('click', onClick);
  };

  /* Shared by lesson.js and review.js: the card for a locked lesson, review or homework id, or null when it is open */
  Z.lockedFor = function (host, cid, id, route) {
    const P = Z.prereq;
    if (!P || !cid || !id || !P.itemLocked(cid, id)) return null;
    const lv = P.levelHolding(cid, id);
    const isLesson = (lv.lessons || []).includes(id);
    const x = Z.content.courseLessons(cid).find(y => y.id === id);
    const name = isLesson ? (x ? x.name : id) : lv.review === id ? `Level ${lv.n} review` : id === `problems-${lv.n}` ? `Problem set ${lv.n}` : `Homework ${lv.n}`;
    return Z.lockedCard(host, { title: `${name} is locked`, route, openKey: P.keyOfLevel(cid, lv.n),
      missing: isLesson ? P.missingFor(cid, id) : P.missingForLevel(cid, lv.n), back: `#course/${cid}`,
      check: isLesson ? P.diagnosticsFor(cid, id) : P.diagnosticsForLevel(cid, lv.n), limits: isLesson ? P.routeLimitsForLesson(cid, id) : P.routeLimitsForLevel(cid, lv.n) });
  };
})();
