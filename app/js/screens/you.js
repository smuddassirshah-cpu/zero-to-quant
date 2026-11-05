/* You (#you): profile, stats, mastery map, streak calendar, exam history, hours, drill record, settings and data.
   Everything is read from ZQ.state (summary(), profile, settings, skills, streak.days, hours, exams, drills) and
   ZQ.content (tracks, stages, topics, courses and their skill labels). Writes go through the mutators only:
   ZQ.setSetting for theme, motion and sound, ZQ.state.settings.set for the streak switch, ZQ.state.profile.set for the
   weekly goal and track, ZQ.state.hours.log for manual time, ZQ.state.export / import / reset for the data.
   Spec: docs/design-research.md 7.5 (You), 6.2 (streak, rest days, goals), 2.6 (single-hue sequential ramp, tooltips,
   table views), 4.9 (motion, sound). No league board and no achievements (docs/PLAN.md 2).
   Screen selectors carry .screen-you; sheets live in <body>, so their classes carry the yu-sh- prefix. */
(function () {
  'use strict';

  const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const MONTH = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const WD = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const BLOCKS = [['main', 'Main subject'], ['build', 'Build'], ['review', 'Review'], ['mental', 'Mental arithmetic']];
  const TRACKS = [['Trader', 'Trader'], ['Researcher', 'Researcher'], ['Developer', 'Developer'], ['Strats', 'Strats'], ['Undecided', 'Not sure']];
  const BIN_LABEL = ['Not started', '1 to 16%', '17 to 33%', '34 to 50%', '51 to 66%', '67 to 83%', '84 to 100%'];
  const RESET_WORD = 'RESET';

  const MOD = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent || '') ? '⌘' : 'Ctrl';
  const SHORTCUTS = [
    ['Lessons and practice', [[['Enter'], 'Check, then Continue'], [['1', '9'], 'Pick an answer option', 'to'], [['Esc'], 'Close a sheet or explanation']]],
    ['Code drills', [[['Tab'], 'Indent'], [['Shift', 'Tab'], 'Dedent', '+'], [['Esc', 'Tab'], 'Leave the editor', 'then'],
      [[MOD, 'Enter'], 'Run the examples', '+'], [[MOD, 'Shift', 'Enter'], 'Submit for the hidden tests', '+']]],
    ['Everywhere', [[['Tab'], 'Move between controls (in the code editor, press Esc first)'], [['Esc'], 'Close a sheet or dialog'],
      [['↑', '↓', '←', '→'], 'Move around the mastery map and the calendar']]],
  ];

  const fmtH = (v) => { const r = Math.round(v * 10) / 10; return r.toLocaleString('en-GB'); };
  const plural = (n, one, many) => `${n.toLocaleString('en-GB')} ${n === 1 ? one : many}`;
  const hm = (m) => { m = Math.round(m); return m >= 60 ? `${Math.floor(m / 60)} h${m % 60 ? ` ${m % 60} min` : ''}` : `${m} min`; };
  const yearsAt = (goal) => { const y = 3100 / (goal * 52.18); return y >= 3 ? String(Math.round(y)) : y.toFixed(1); };

  ZQ.screen({
    id: 'you', title: 'You', group: 'App', shell: true, tab: 'you',
    render(root, Z) {
      const { esc, icon } = Z;
      const S = Z.state, C = Z.content, D = S.dates;
      const cleanups = [];
      const listen = (el, ev, fn, opt) => { el.addEventListener(ev, fn, opt); cleanups.push(() => el.removeEventListener(ev, fn, opt)); };
      const dayLabel = (k) => { const d = D.parseKey(k); return `${WD[d.getDay()]} ${d.getDate()} ${MON[d.getMonth()]}`; };
      const dateLong = (t) => { const d = new Date(t); return `${d.getDate()} ${MON[d.getMonth()]} ${d.getFullYear()}`; };
      const streakOff = () => S.settings.streakMode === 'off';

      /* ---------- Skill labels and the curriculum's shape ---------- */
      const tracks = C.tracks || {};
      const trackIds = Object.keys(tracks).length ? Object.keys(tracks) : ['maths', 'prob', 'code', 'fin', 'ml', 'speed'];
      const skillLabel = {};
      C.courses().forEach(c => Object.entries(c.skills || {}).forEach(([k, v]) => { if (!skillLabel[k]) skillLabel[k] = v; }));
      const topicsByTrack = {};
      const buildTopics = () => { // again after "Quant path only" changes
        Object.keys(topicsByTrack).forEach(k => delete topicsByTrack[k]);
        C.stages().forEach(st => st.topics.forEach(t => {
          const courses = (t.courses || []).map(id => C.course(id)).filter(c => c && Object.keys(c.skills || {}).length);
          if (courses.length) (topicsByTrack[t.track] = topicsByTrack[t.track] || []).push({ ...t, stage: st.id, courses });
        }));
      };
      buildTopics();
      const mastery = (skill) => { const r = S.skills[skill]; return r && r.seen ? (S.summary().skillMastery[skill] || 0) : null; };
      const bin = (v) => (v == null ? 0 : Math.max(1, Math.min(6, Math.ceil(v * 6))));
      const pct = (v) => Math.round(v * 100);

      /* =====================================================================
         Header: avatar, name, stage and track, member since, this week against the goal, stats
         ===================================================================== */
      const headerHTML = () => {
        const L = S.summary(), P = S.profile.get();
        const stage = C.stage(P.startStage);
        const since = P.createdAt ? `Member since ${MONTH[new Date(P.createdAt).getMonth()]} ${new Date(P.createdAt).getFullYear()}` : 'New here';
        const firstStat = streakOff()
          ? `<div class="yu-stat"><span class="yu-stat-v tnum">${icon('terminal', 'sm')}${drillCounts().verified}</span><span class="t-caption muted">verified drills</span></div>`
          : `<button type="button" class="yu-stat is-btn" data-act="streak" aria-label="${L.streak} day streak, ${L.restDays} of 2 rest days held. Open streak details.">
              <span class="yu-stat-v tnum">${L.streak}${Z.bolt(L.todayQualified)}</span><span class="yu-stat-c t-caption muted">day streak${icon('chevronR', 'xs')}</span></button>`;
        const tile = (ic, v, label) => `<li><div class="yu-stat"><span class="yu-stat-v tnum">${ic}${v}</span><span class="t-caption muted">${label}</span></div></li>`;
        const done = L.hoursWeekTotal, goal = L.weeklyGoalH;
        return `
          <div class="yu-id">
            <span class="avatar yu-av" aria-hidden="true">${esc(L.initial || '?')}</span>
            <div class="yu-id-t">
              <h1 class="t-h1" id="yu-name">${esc(P.name || 'You')}</h1>
              <p class="t-body secondary">${stage ? `Started at Stage ${stage.id}, ${esc(stage.name)}` : `Stage ${P.startStage}`} · ${P.track === 'Undecided' ? 'Track not chosen yet' : esc(P.track) + ' track'}</p>
              <p class="t-caption muted">${since}</p>
            </div>
            <button class="icon-btn yu-gear" type="button" data-act="settings" aria-label="Go to settings">${icon('settings')}</button>
          </div>
          <div class="yu-week">
            <div class="yu-week-h"><span class="t-overline muted">This week</span><span class="t-label tnum"><b>${fmtH(done)}</b> of ${goal} h</span></div>
            <div class="bar" role="progressbar" aria-label="Hours this week" aria-valuemin="0" aria-valuemax="${goal}" aria-valuenow="${fmtH(Math.min(done, goal))}" aria-valuetext="${fmtH(done)} of ${goal} hours"><i style="width:${Math.min(100, done / goal * 100).toFixed(1)}%"></i></div>
            <span class="t-caption muted">${done >= goal ? 'Goal met. Anything more this week is extra.' : `${fmtH(goal - done)} h to go. The week resets on Monday.`}</span>
          </div>
          <ul class="yu-stats">
            <li data-stat-first>${firstStat}</li>
            ${streakOff() ? '' : tile(icon('trophy', 'sm'), L.best, 'longest streak')}
            ${tile(Z.spark(L.xp > 0), L.xp.toLocaleString('en-GB'), 'XP')}
            ${tile(icon('target', 'sm'), L.mp.toLocaleString('en-GB'), 'mastery points')}
            ${tile(icon('book', 'sm'), L.lessonsDone.toLocaleString('en-GB'), 'lessons complete')}
            ${tile(icon('star', 'sm'), L.mastered.toLocaleString('en-GB'), 'lessons mastered')}
            ${Z.prereq && Z.prereq.openedCount() ? tile(icon('lock', 'sm'), Z.prereq.openedCount(), 'opened early') : ''}
          </ul>`;
      };

      /* =====================================================================
         Mastery map: track, then topic, then course; one cell per skill
         ===================================================================== */
      const openTracks = new Set();
      const trackStats = (tr) => {
        let n = 0, started = 0, sum = 0;
        (topicsByTrack[tr] || []).forEach(t => t.courses.forEach(c => Object.keys(c.skills).forEach(s => { n++; const v = mastery(s); if (v != null) { started++; sum += v; } })));
        return { n, started, mean: started ? sum / started : 0 };
      };
      (() => { // open the tracks with progress; on a fresh start, the first one
        trackIds.forEach(tr => { if (trackStats(tr).started) openTracks.add(tr); });
        if (!openTracks.size && trackIds.length) openTracks.add(trackIds[0]);
      })();
      const courseRow = (t, c, r) => {
        const skills = Object.entries(c.skills);
        const started = skills.map(([s]) => mastery(s)).filter(v => v != null);
        const avg = started.length ? `${pct(started.reduce((a, b) => a + b, 0) / started.length)}%` : '';
        return `<div class="yu-mm-row" role="row">
            <div class="yu-mm-lbl" role="rowheader"><span class="yu-mm-name">${esc(c.name)}</span>${avg ? `<span class="yu-mm-avg t-caption tnum" title="Mean of the skills started"><span class="sr-only">, average </span>${avg}</span>` : ''}</div>
            ${skills.map(([s, label], col) => {
              const v = mastery(s);
              return `<div class="yu-cell b${bin(v)}" role="gridcell" tabindex="${r === 0 && col === 0 ? 0 : -1}" data-r="${r}" data-c="${col}"
                data-tip="${esc(c.name + ': ' + label)}" data-v="${v == null ? '' : pct(v)}" aria-label="${esc(label)}, ${v == null ? 'not started' : pct(v) + '%'}"></div>`;
            }).join('')}
          </div>`;
      };
      const mapHTML = () => trackIds.filter(tr => (topicsByTrack[tr] || []).length).map(tr => {
        const st = trackStats(tr), open = openTracks.has(tr);
        return `<div class="yu-mm-track" data-track="${esc(tr)}">
            <button type="button" class="yu-mm-th" data-mmtrack="${esc(tr)}" aria-expanded="${open}" aria-controls="yu-mm-b-${esc(tr)}">
              <span class="yu-mm-dot" aria-hidden="true"></span><span class="t-h2">${esc(tracks[tr] || tr)}</span>
              <span class="t-caption muted tnum">${st.started ? `${st.started} of ${st.n} skills started · ${pct(st.mean)}% mean` : `${st.n} skills, none started`}</span>${icon('chevronD', 'sm yu-mm-chev')}</button>
            <div class="yu-mm-body" id="yu-mm-b-${esc(tr)}"${open ? '' : ' hidden'}>
              ${topicsByTrack[tr].map(t => `<div class="yu-mm-topic">
                <h3 class="yu-mm-tt" id="yu-mm-t-${esc(t.id)}"><span class="yu-tag">${esc(t.id)}</span><span class="t-label">${esc(t.name)}</span><span class="t-caption muted">Stage ${t.stage}</span></h3>
                <div class="yu-mm-grid" role="grid" aria-labelledby="yu-mm-t-${esc(t.id)}" aria-describedby="yu-mm-help" data-grid>${t.courses.map((c, r) => courseRow(t, c, r)).join('')}</div>
              </div>`).join('')}
            </div></div>`;
      }).join('');
      const mapTable = () => `<div class="yu-tablewrap" tabindex="0" role="region" aria-label="Mastery map as a table">
          <table class="yu-tbl">
            <caption class="sr-only">Mastery by skill, by topic and course</caption>
            <thead><tr><th scope="col">Skill</th><th scope="col">Course</th><th scope="col" class="num">Mastery</th></tr></thead>
            ${trackIds.flatMap(tr => (topicsByTrack[tr] || []).map(t => `<tbody>
              <tr class="yu-tgrp"><th scope="rowgroup" colspan="3" data-track="${esc(tr)}"><span class="yu-tag">${esc(t.id)}</span> ${esc(t.name)}<span class="muted">, ${esc(tracks[tr] || tr)}</span></th></tr>
              ${t.courses.flatMap(c => Object.entries(c.skills).map(([s, label]) => { const v = mastery(s); return `<tr><td>${esc(label)}</td><td class="muted">${esc(c.name)}</td><td class="num tnum">${v == null ? '<span class="muted">Not started</span>' : pct(v) + '%'}</td></tr>`; })).join('')}</tbody>`)).join('')}
          </table></div>`;
      const legend = `<div class="yu-legend" aria-hidden="true">
          <span class="yu-lg-item"><i class="yu-swatch b0"></i>Not started</span>
          <span class="yu-ramp"><span>0%</span>${[1, 2, 3, 4, 5, 6].map(b => `<i class="yu-swatch b${b}" title="${BIN_LABEL[b]}"></i>`).join('')}<span>100%</span></span>
        </div>`;

      /* =====================================================================
         Streak calendar: the last 12 weeks, Monday rows, from streak.days
         ===================================================================== */
      const DAYS = ['M', 'T', 'W', 'Th', 'F', 'S', 'Su'];
      const DAYS_LONG = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
      const calData = () => {
        const today = D.todayKey(), start = D.addDays(D.weekStart(), -77);
        const days = S.streak.days || {}, P = S.profile.get();
        const created = P.createdAt ? D.todayKey(P.createdAt) : today;
        const mins = {};
        S.hours.list().forEach(e => { mins[e.date] = (mins[e.date] || 0) + e.minutes; });
        const cells = Array.from({ length: 84 }, (_, i) => {
          const k = D.addDays(start, i), v = days[k];
          let st;
          if (k > today) st = 'future';
          else if (v === true) st = 'lit';
          else if (v === 'rest') st = 'rest';
          else if (k === today) st = 'today';
          else if (k < created) st = 'before';
          else st = 'missed';
          return { k, st, today: k === today, m: mins[k] || 0 };
        });
        return { cells, start, today };
      };
      const heat = (m) => (m < 45 ? 'h1' : m < 120 ? 'h2' : 'h3');
      const calCell = (c, r, col, isTab) => {
        const label = { lit: 'studied', rest: 'rest day used, streak kept', today: 'today, not counted yet', before: 'before you started', missed: 'missed', future: 'to come' }[c.st];
        const det = c.st === 'lit' && c.m ? hm(c.m) : c.st === 'lit' && c.today ? 'today' : '';
        const cls = c.st === 'lit' ? `lit ${heat(c.m)}` : c.st === 'before' ? 'future' : c.st;
        return `<div class="yu-day ${cls}${c.today ? ' today' : ''}" role="gridcell" tabindex="${isTab ? 0 : -1}" data-r="${r}" data-c="${col}"
          data-tip="${esc(dayLabel(c.k))}" data-tv="${esc(label.charAt(0).toUpperCase() + label.slice(1))}" data-td="${esc(det)}" aria-label="${esc(dayLabel(c.k))}: ${esc(label)}${det ? ', ' + esc(det) : ''}">${c.st === 'rest' ? icon('rest') : ''}</div>`;
      };
      const calHTML = () => {
        const { cells, start, today } = calData();
        const ti = cells.findIndex(c => c.k === today);
        const monthOf = (w) => {
          for (let d = 0; d < 7; d++) { const dt = D.parseKey(cells[w * 7 + d].k); if (dt.getDate() === 1 || (w === 0 && d === 0)) return MON[dt.getMonth()]; }
          return '';
        };
        const s0 = D.parseKey(start), from = `${s0.getDate()} ${MON[s0.getMonth()]}`;
        const desk = `<div class="yu-cal yu-cal-desk" role="grid" aria-label="Streak calendar, 12 weeks from ${from}. Rows are days of the week, Monday first; columns are weeks." data-grid>
            <div class="yu-cal-months" role="presentation" aria-hidden="true">${Array.from({ length: 12 }, (_, w) => { const m = monthOf(w); return m ? `<span style="grid-column:${w + 2}">${m}</span>` : ''; }).join('')}</div>
            ${DAYS.map((dl, r) => `<div class="yu-cal-row" role="row"><span class="yu-cal-d" role="rowheader" aria-label="${DAYS_LONG[r]}s">${dl}</span>${
              Array.from({ length: 12 }, (_, w) => calCell(cells[w * 7 + r], r, w, w * 7 + r === ti)).join('')}</div>`).join('')}
          </div>`;
        const mob = `<div class="yu-cal yu-cal-mob" role="grid" aria-label="Streak calendar, 12 weeks from ${from}. Rows are weeks, oldest first; columns are days, Monday first." data-grid>
            <div class="yu-cal-row yu-cal-hd" role="row"><span role="columnheader"><span class="sr-only">Week of</span></span>${DAYS.map((dl, d) => `<span class="yu-cal-d" role="columnheader" aria-label="${DAYS_LONG[d]}">${dl}</span>`).join('')}</div>
            ${Array.from({ length: 12 }, (_, w) => { const wk = D.parseKey(cells[w * 7].k); return `<div class="yu-cal-row" role="row"><span class="yu-cal-d yu-cal-m" role="rowheader" aria-label="Week of ${wk.getDate()} ${MON[wk.getMonth()]}">${monthOf(w)}</span>${
              Array.from({ length: 7 }, (_, d) => calCell(cells[w * 7 + d], w, d, w * 7 + d === ti)).join('')}</div>`; }).join('')}
          </div>`;
        const rows = Array.from({ length: 12 }, (_, w) => {
          const wc = cells.slice(w * 7, w * 7 + 7), wk = D.parseKey(wc[0].k);
          const n = (st) => wc.filter(c => c.st === st).length;
          return `<tr><th scope="row" class="yu-wk">${wk.getDate()} ${MON[wk.getMonth()]}${w === 11 ? '<span class="t-caption muted">This week</span>' : ''}</th>
            <td class="num tnum">${n('lit')}</td><td class="num tnum">${n('rest')}</td><td class="num tnum">${n('missed')}</td><td class="num tnum">${fmtH(wc.reduce((a, c) => a + c.m, 0) / 60)}</td></tr>`;
        }).reverse().join('');
        const table = `<div class="yu-tablewrap" tabindex="0" role="region" aria-label="Streak calendar as a table">
            <table class="yu-tbl"><caption class="sr-only">Days studied per week, newest first</caption>
            <thead><tr><th scope="col">Week of</th><th scope="col" class="num">Studied</th><th scope="col" class="num">Rest</th><th scope="col" class="num">Missed</th><th scope="col" class="num">Hours</th></tr></thead>
            <tbody>${rows}</tbody></table></div>`;
        const L = S.summary();
        const past = cells.filter(c => c.k <= today && c.st !== 'before');
        const studied = past.filter(c => c.st === 'lit').length;
        return `
          <div class="yu-st-stats">
            <div class="yu-run is-static"><span class="t-overline muted">Current</span><span class="yu-run-v tnum">${plural(L.streak, 'day', 'days')}</span><span class="t-caption muted">${L.todayQualified ? 'today counts' : 'today not counted yet'}</span></div>
            <div class="yu-run is-static"><span class="t-overline muted">Longest</span><span class="yu-run-v tnum">${plural(L.best, 'day', 'days')}</span><span class="t-caption muted">since you started</span></div>
            <div class="yu-run is-static"><span class="t-overline muted">Studied</span><span class="yu-run-v tnum">${studied} of ${past.length}</span><span class="t-caption muted">days in these 12 weeks</span></div>
            <div class="yu-run is-static"><span class="t-overline muted">Rest days</span><span class="yu-run-v tnum">${L.restDays} of 2</span><span class="t-caption muted">held now</span></div>
          </div>
          <div class="yu-chart" data-chart="cal">
            <div data-view="map">${desk}${mob}
              <ul class="yu-cal-key" aria-hidden="true">
                <li class="yu-cal-ramp"><span>Time logged: less</span><i class="yu-day lit h1"></i><i class="yu-day lit h2"></i><i class="yu-day lit h3"></i><span>more</span></li>
                <li><i class="yu-day rest">${icon('rest')}</i>Rest day used</li>
                <li><i class="yu-day missed"></i>Missed</li>
                <li><i class="yu-day today"></i>Today</li>
                <li><i class="yu-day future"></i>To come, or before you started</li>
              </ul>
            </div>
            <div data-view="table" hidden>${table}</div>
            <div class="yu-tip" aria-hidden="true" hidden></div>
          </div>`;
      };

      /* =====================================================================
         Exam history, from ZQ.state.exams
         ===================================================================== */
      const examDocs = {};
      const examName = (id) => {
        let m;
        if ((m = String(id).match(/^topic-(.+)$/))) { const t = C.topic(m[1]); return { tag: m[1], name: t ? t.name : `Topic ${m[1]}`, kind: 'Topic exam', track: t ? t.track : 'maths' }; }
        if ((m = String(id).match(/^stage-(\d+)$/))) { const s = C.stage(+m[1]); return { tag: 'S' + m[1], name: s ? `Stage ${m[1]}: ${s.name}` : `Stage ${m[1]}`, kind: 'Stage exit', track: 'maths' }; }
        if (/^mock-/.test(String(id))) { const d = examDocs[id]; return { tag: 'M', name: (d && d.name) || id, kind: 'Mock assessment', track: ZQ.mock ? ZQ.mock.style(d && d.style).track : 'speed' }; }
        return { tag: '', name: id, kind: 'Exam', track: 'maths' };
      };
      /* A mock keeps a net score; its pass mark may be a net score too */
      const netOf = (e) => (typeof e.net === 'number' ? ZQ.mock.signed(e.net) : null);
      const passText = (id) => { const d = examDocs[id]; if (!d) return null; const p = (d.parts || []).find(x => x.kind === 'paper') || d; return typeof p.passNet === 'number' ? `${ZQ.mock.signed(p.passNet)} net` : null; };
      const examRows = () => {
        const out = [];
        Object.entries(S.exams || {}).forEach(([id, rec]) => (rec.attempts || []).forEach((a, i) => out.push({ id, i, ...a, ...examName(id) })));
        return out.sort((a, b) => (b.at || 0) - (a.at || 0));
      };
      const passMark = (id) => { const d = examDocs[id]; if (!d) return null; if (typeof d.pass === 'number') return d.pass; const p = (d.parts || []).find(x => typeof x.pass === 'number'); return p ? p.pass : null; };
      const examsHTML = () => {
        const rows = examRows();
        if (!rows.length) return `<p class="t-body secondary yu-empty">No exams sat yet. Topic exams open on Review once every course in a topic has a mastered lesson, and you can always sit one early.</p>`;
        return `<table class="yu-extbl">
            <caption class="sr-only">Exam history, newest first</caption>
            <thead><tr><th scope="col">Date</th><th scope="col">Exam</th><th scope="col" class="num">Score</th><th scope="col" class="num">Pass mark</th><th scope="col">Result</th></tr></thead>
            <tbody>${rows.map((e, k) => { const share = e.items ? e.score / e.items : 0, pm = passMark(e.id); return `<tr data-track="${esc(e.track)}">
              <td class="yu-ex-d"><time datetime="${e.at ? new Date(e.at).toISOString() : ''}">${e.at ? dateLong(e.at) : ''}</time></td>
              <th scope="row" class="yu-ex-n"><button type="button" class="yu-ex-b" data-exam="${k}" aria-haspopup="dialog">
                ${e.tag ? `<span class="yu-tag">${esc(e.tag)}</span>` : ''}<span class="yu-ex-t"><span class="t-label">${esc(e.name)}</span><span class="t-caption muted">${esc(e.kind)}</span></span>${icon('chevronR', 'sm yu-chev')}</button></th>
              <td class="yu-ex-s num tnum"><span class="yu-ex-pct">${netOf(e) != null ? netOf(e) + ' net' : Math.round(share * 100) + '%'}</span><span class="yu-ex-got">${e.score} of ${e.items}${netOf(e) != null ? ' right' : ''}</span></td>
              <td class="yu-ex-p num tnum"><span class="yu-k">Pass </span>${passText(e.id) || (pm == null ? '<span class="muted">…</span>' : Math.round(pm * 100) + '%')}</td>
              <td class="yu-ex-r">${e.passed ? `<span class="chip correct">${icon('check', 'xs')}Passed</span>` : `<span class="chip notyet">${icon('cross', 'xs')}Not passed</span>`}</td>
            </tr>`; }).join('')}</tbody>
          </table>`;
      };

      /* =====================================================================
         Hours: all time and this week by block, and manual entry
         ===================================================================== */
      const hoursHTML = () => {
        const L = S.summary(), all = { main: 0, build: 0, review: 0, mental: 0 };
        S.hours.list().forEach(e => { if (all[e.block] != null) all[e.block] += e.minutes / 60; });
        const total = Object.values(all).reduce((a, b) => a + b, 0);
        return `
          <div class="yu-card-h"><div><h2 class="t-h1" id="yu-hr-h">Hours</h2>
            <p class="t-caption secondary">Lessons, quizzes, reviews and exams count as main; drills as build; redo and practice as review; the warm-up as mental arithmetic.</p></div>
            <span class="yu-dr-total"><span class="t-stat tnum">${fmtH(total)}</span><span class="t-caption muted">hours in all</span></span></div>
          <ul class="yu-hr-list">${BLOCKS.map(([b, name]) => { const wk = L.hoursWeek[b] || 0, goal = L.weekGoal[b] || 0; return `<li>
              <span class="yu-hr-n t-label">${name}</span><span class="yu-hr-all t-caption tnum"><b>${fmtH(all[b])} h</b> in all</span>
              <span class="yu-dr-bar" role="img" aria-label="${name}: ${fmtH(wk)} of ${fmtH(goal)} hours this week"><i style="width:${goal ? Math.min(100, wk / goal * 100).toFixed(1) : 0}%"></i></span>
              <span class="yu-hr-wk t-caption tnum">${fmtH(wk)} of ${fmtH(goal)} h this week</span></li>`; }).join('')}</ul>
          <form class="yu-log" data-log novalidate>
            <h3 class="t-overline muted">Log time</h3>
            <p class="t-caption secondary">For study away from the app: a textbook chapter, a past paper, a project on your own machine.</p>
            <div class="yu-log-f">
              <label class="yu-sh-f"><span class="t-label">Block</span><select name="block">${BLOCKS.map(([b, n]) => `<option value="${b}">${n}</option>`).join('')}</select></label>
              <label class="yu-sh-f yu-log-min"><span class="t-label">Minutes</span><input name="minutes" type="number" inputmode="numeric" min="1" max="720" step="1" placeholder="45" required></label>
              <label class="yu-sh-f"><span class="t-label">Date</span><input name="date" type="date" value="${D.todayKey()}" max="${D.todayKey()}" required></label>
            </div>
            <div class="yu-log-act"><button type="submit" class="btn secondary yu-set-btn">${icon('plus', 'sm')}Add time</button><span class="t-caption yu-log-msg" role="status" aria-live="polite"></span></div>
          </form>`;
      };

      /* =====================================================================
         Drill record: verified drills by course
         ===================================================================== */
      const drillCounts = () => {
        const list = C.drills(), rec = (S.drills && S.drills.get()) || {};
        return { list, rec, verified: list.filter(d => rec[d.id] && rec[d.id].verified).length };
      };
      const drillsHTML = () => {
        const { list, rec, verified } = drillCounts();
        const groups = [];
        list.forEach(d => { let g = groups.find(x => x.course === d.course); if (!g) { const c = C.course(d.course) || {}; g = { course: d.course, name: c.name || d.course, topic: c.topic || '', track: c.track || 'code', n: 0, v: 0 }; groups.push(g); } g.n++; if (rec[d.id] && rec[d.id].verified) g.v++; });
        return `
          <div class="yu-card-h"><div><h2 class="t-h1" id="yu-dr-h">Drill record</h2>
            <p class="t-caption secondary">A drill counts once your code passes every hidden test.</p></div>
            <span class="yu-dr-total"><span class="t-stat tnum">${verified}</span><span class="t-caption muted">of ${list.length} verified</span></span></div>
          ${groups.length ? `<ul class="yu-dr-list">${groups.map(g => `<li data-track="${esc(g.track)}">
              <span class="yu-tag">${esc(g.topic)}</span><span class="yu-dr-n t-label">${esc(g.name)}</span>
              <span class="yu-dr-bar" role="img" aria-label="${g.v} of ${g.n} drills verified"><i style="width:${(g.v / g.n * 100).toFixed(1)}%"></i></span>
              <span class="yu-dr-v t-caption tnum"><b>${g.v}</b> of ${g.n}</span></li>`).join('')}</ul>` : '<p class="t-body secondary">No drills are written yet.</p>'}
          <a class="btn secondary yu-dr-go" href="#drill">${icon('terminal', 'sm')}Open code drills</a>`;
      };

      /* =====================================================================
         Capstone (ENGINE-BACKLOG 566): read-only records, one per role, the learner's role first. The reviewer fills content/capstones.json.
         ===================================================================== */
      const ROLE_NAME = { trader: 'Trader', researcher: 'Researcher', developer: 'Developer', strats: 'Strats', 'strats-deriv': 'Strats (derivatives)' };
      const capstoneHTML = () => {
        const own = C.readiness.roleKey(S.profile.get().track);
        const order = ['trader', 'researcher', 'developer', 'strats', 'strats-deriv'];
        const roles = order.includes(own) ? [own, ...order.filter(r => r !== own)] : order;
        const link = (u) => (/^https:\/\//.test(u) ? `<a href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(u.replace(/^https:\/\//, ''))}</a>` : esc(u));
        const row = (k, v) => `<div class="yu-cp-r"><dt class="t-caption muted">${k}</dt><dd class="t-body">${v || '<span class="muted">Not recorded</span>'}</dd></div>`;
        return `<div class="yu-card-h"><div><h2 class="t-h1" id="yu-cp-h">Capstone</h2>
            <p class="t-caption secondary">A role is ready only with its required levels met and an external capstone, rerun from clean and reviewed. The reviewer fills these records in <code>content/capstones.json</code>.</p></div></div>
          <ul class="yu-cp-list">${roles.map(r => {
            const rec = C.readiness.capstone(r) || {}, st = C.readiness.status(r), done = !!rec.role && C.readiness.capstoneComplete(rec);
            const label = done ? 'Capstone complete' : (rec.role && (rec.external || rec.repo || rec.reviewer || rec.date || rec.project)) ? 'Capstone incomplete' : 'Capstone not recorded';
            return `<li class="yu-cp${r === own ? ' is-own' : ''}" data-role="${r}">
              <div class="yu-cp-h"><span class="t-label">${ROLE_NAME[r]}${r === own ? ' (your role)' : ''}</span>
                <span class="chip ${done ? 'correct' : 'notyet'}">${label}</span></div>
              <dl class="yu-cp-d">${row('Project', esc(rec.project || ''))}${row('Repo', rec.repo ? link(rec.repo) : '')}${row('Reviewer', esc(rec.reviewer || ''))}${row('Date', esc(rec.date || ''))}${row('Rerun from clean', esc(rec.rerun || ''))}${row('External', rec.external === true ? 'Yes' : 'No')}${row('Defence notes', esc(rec.defence || ''))}</dl></li>`; }).join('')}</ul>`;
      };

      /* =====================================================================
         Settings and data
         ===================================================================== */
      const seg = (name, label, opts, val, help = '') => `<div class="yu-set-row yu-set-stack">
          <div class="yu-set-t"><span class="t-label" id="yu-l-${name}">${label}</span>${help ? `<span class="t-caption muted" id="yu-h-${name}">${help}</span>` : ''}</div>
          <div class="yu-seg" role="radiogroup" aria-labelledby="yu-l-${name}" ${help ? `aria-describedby="yu-h-${name}"` : ''}>
            ${opts.map(([v, l]) => `<label><input type="radio" name="yu-${name}" value="${v}" ${String(val) === String(v) ? 'checked' : ''}><span>${l}</span></label>`).join('')}
          </div></div>`;
      const sw = (id, label, help, on) => `<div class="yu-set-row">
          <label class="yu-set-t" for="yu-${id}"><span class="t-label">${label}</span>${help ? `<span class="t-caption muted" id="yu-h-${id}">${help}</span>` : ''}</label>
          <span class="yu-sw"><input type="checkbox" role="switch" id="yu-${id}" ${on ? 'checked' : ''} ${help ? `aria-describedby="yu-h-${id}"` : ''}><i aria-hidden="true"></i></span>
        </div>`;
      const act = (a, label, help, btn, ic, extra = '') => `<div class="yu-set-row${extra ? ' yu-set-wrap' : ''}">
          <div class="yu-set-t"><span class="t-label">${label}</span><span class="t-caption muted">${help}</span>${extra}</div>
          <button type="button" class="btn secondary yu-set-btn" data-act="${a}">${ic ? icon(ic, 'sm') : ''}${btn}</button>
        </div>`;
      const goalHelp = (g) => `The full path is 3,100 hours: about ${yearsAt(g)} years at ${g} h a week.`;
      const settingsHTML = () => {
        const P = S.profile.get();
        return `
          <h2 class="t-h1" id="yu-set-h">Settings</h2>
          <div class="yu-set-cols">
            <div class="yu-set-g">
              <h3 class="t-overline muted">Display and feedback</h3>
              ${seg('theme', 'Theme', [['system', 'System'], ['light', 'Light'], ['dark', 'Dark']], Z.settings.theme, 'System follows your device.')}
              ${seg('motion', 'Motion', [['system', 'System'], ['full', 'Full'], ['reduced', 'Reduced']], Z.settings.motion, 'Reduced swaps movement for quick fades and shows totals at once.')}
              ${sw('sound', 'Sound', 'Short tones for right answers, misses and finishing a lesson.', Z.settings.sound)}
            </div>
            <div class="yu-set-g">
              <h3 class="t-overline muted">Study plan</h3>
              ${seg('goal', 'Weekly goal', [[5, '5 h'], [10, '10 h'], [15, '15 h'], [25, '25 h']], P.weeklyGoalH, goalHelp(P.weeklyGoalH))}
              ${seg('track', 'Track', TRACKS, P.track, 'Stages 0 and 1 are the same for every track. The track shapes Stage 2 onwards and the Paths view on Learn.')}
              ${sw('quantonly', 'Quant path only', 'Hides the pure maths courses and topics, and leaves them out of stage progress. They stay one tap away if you open them from a link.', !!S.settings.quantOnly)}
              ${sw('strictprereqs', 'Strict prerequisites', `On keeps a lesson locked until the levels it relies on are met, with no way round except a test-out. Off adds Open anyway to the locked card.${Z.prereq && Z.prereq.openedCount() ? ` Opened early so far: ${Z.prereq.openedCount()}.` : ''}`, S.settings.strictPrereqs !== false)}
              ${sw('streak', 'Streak', 'Off hides the streak count, the bolt and the calendar everywhere.', !streakOff())}
              ${act('setup', 'Run setup again', 'Change your name, track, weekly hours or starting stage. Your progress stays.', 'Run setup', 'replay')}
            </div>
            <div class="yu-set-g">
              <h3 class="t-overline muted">Your data</h3>
              ${act('export', 'Export', 'Download everything as one JSON file. Keep it as a backup or move it to another browser.', 'Export', '')}
              ${act('import', 'Import', 'Replace everything here with an exported file.', 'Import', '', '<span class="t-caption yu-err" data-import-err role="alert"></span>')}
              <input type="file" accept="application/json,.json" data-import hidden>
              ${act('reset', 'Reset progress', 'Start again from nothing. This clears everything, settings included.', 'Reset', '')}
            </div>
            <div class="yu-set-g">
              <h3 class="t-overline muted">Help</h3>
              ${act('keys', 'Keyboard shortcuts', 'Every lesson, drill and exam works from the keyboard.', 'View', '')}
              ${act('system', 'Design system', 'Every colour, type style, diagram and answer widget on one page.', 'Open', '')}
            </div>
          </div>`;
      };

      /* =====================================================================
         Mount
         ===================================================================== */
      root.innerHTML = `<div class="yu${streakOff() ? ' is-streak-off' : ''}">
          <section class="card yu-head" aria-labelledby="yu-name" data-card="head"></section>
          <div class="yu-cols">
            <div class="yu-side">
              <section class="card yu-card yu-hr" aria-labelledby="yu-hr-h" data-card="hours"></section>
              <section class="card yu-card yu-dr" aria-labelledby="yu-dr-h" data-card="drills"></section>
            </div>
            <div class="yu-main">
              <section class="card yu-card yu-mm" aria-labelledby="yu-mm-h">
                <div class="yu-card-h">
                  <div><h2 class="t-h1" id="yu-mm-h">Mastery map</h2>
                    <p class="t-caption secondary" id="yu-mm-help">One cell per skill, shaded by mastery from first-try answers in quizzes, reviews, homework, exams and redos. Lessons alone do not move it.<span data-keyhelp> Use the arrow keys to move between skills.</span></p></div>
                  <button type="button" class="yu-view" data-act="mm-view" aria-pressed="false">${icon('grid', 'xs')}<span>Table view</span></button>
                </div>
                ${legend}
                <div class="yu-chart" data-chart="mm">
                  <div data-view="map" data-card="map"></div>
                  <div data-view="table" hidden data-card="maptable"></div>
                  <div class="yu-tip" aria-hidden="true" hidden></div>
                </div>
              </section>
              <section class="card yu-card yu-sm" aria-labelledby="yu-sm-h" data-card="selfmarked" hidden></section>
              <section class="card yu-card yu-st" aria-labelledby="yu-st-h"${streakOff() ? ' hidden' : ''}>
                <div class="yu-card-h">
                  <div><h2 class="t-h1" id="yu-st-h">Streak calendar</h2>
                    <p class="t-caption secondary">The last 12 weeks. A day counts after one finished lesson, quiz, review or homework, or three graded problems.</p></div>
                  <button type="button" class="yu-view" data-act="cal-view" aria-pressed="false">${icon('grid', 'xs')}<span>Table view</span></button>
                </div>
                <div data-card="cal"></div>
              </section>
              <section class="card yu-card yu-ex" aria-labelledby="yu-ex-h">
                <div class="yu-card-h"><div><h2 class="t-h1" id="yu-ex-h">Exam history</h2>
                  <p class="t-caption secondary" data-ex-sub></p></div></div>
                <div data-card="exams"></div>
              </section>
              <section class="card yu-card yu-cps" aria-labelledby="yu-cp-h" data-card="capstone"></section>
            </div>
          </div>
          <section class="card yu-card yu-set" id="yu-settings" aria-labelledby="yu-set-h" tabindex="-1" data-card="settings"></section>
        </div>`;
      const $ = (s) => root.querySelector(s), $$ = (s) => Array.from(root.querySelectorAll(s));

      /* Mark the shell's avatar link as the current page */
      const shellAv = root.closest('.shell') && root.closest('.shell').querySelector('.shell-header .avatar');
      if (shellAv) shellAv.setAttribute('aria-current', 'page');

      /* ---------- Tooltips and roving focus for the two heatmaps ---------- */
      const tipFor = (chart) => chart.querySelector('.yu-tip');
      const showTip = (cell) => {
        const chart = cell.closest('.yu-chart'); if (!chart) return;
        const tip = tipFor(chart);
        tip.replaceChildren();
        const a = document.createElement('span'), b = document.createElement('b');
        if (chart.dataset.chart === 'mm') { a.textContent = cell.dataset.tip + ' · '; b.textContent = cell.dataset.v === '' ? 'not started' : cell.dataset.v + '%'; tip.append(a, b); }
        else { a.textContent = cell.dataset.tip + ' · '; b.textContent = cell.dataset.tv; const c = document.createElement('span'); c.textContent = cell.dataset.td ? ', ' + cell.dataset.td : ''; tip.append(a, b, c); }
        tip.hidden = false;
        const cr = chart.getBoundingClientRect(), r = cell.getBoundingClientRect();
        const tw = tip.offsetWidth, th = tip.offsetHeight;
        let x = r.left - cr.left + r.width / 2 - tw / 2, y = r.top - cr.top - th - 8;
        x = Math.max(0, Math.min(cr.width - tw, x));
        if (y < -cr.top + 8 && r.bottom - cr.top + th + 8 < cr.height) y = r.bottom - cr.top + 8;
        tip.style.left = x + 'px'; tip.style.top = y + 'px';
        chart.querySelectorAll('.is-hot').forEach(n => n.classList.remove('is-hot'));
        cell.classList.add('is-hot');
      };
      const hideTip = (chart) => { const t = tipFor(chart); if (t) t.hidden = true; chart.querySelectorAll('.is-hot').forEach(n => n.classList.remove('is-hot')); };
      listen(root, 'pointerover', (e) => { const c = e.target.closest('.yu-chart [role="gridcell"]'); if (c) showTip(c); });
      listen(root, 'pointerout', (e) => {
        const chart = e.target.closest && e.target.closest('.yu-chart'); if (!chart || chart.contains(e.relatedTarget)) return;
        const f = document.activeElement; if (f && chart.contains(f) && f.matches('[role="gridcell"]')) showTip(f); else hideTip(chart);
      });
      listen(root, 'focusin', (e) => { if (e.target.matches('.yu-chart [role="gridcell"]')) showTip(e.target); });
      listen(root, 'focusout', (e) => { const chart = e.target.closest && e.target.closest('.yu-chart'); if (chart && !chart.contains(e.relatedTarget)) hideTip(chart); });
      listen(root, 'keydown', (e) => {
        const cell = e.target.closest && e.target.closest('.yu-chart [role="gridcell"]'); if (!cell) return;
        const chart = cell.closest('.yu-chart');
        if (e.key === 'Escape') { hideTip(chart); return; }
        const grid = cell.closest('[data-grid]');
        const cells = Array.from(grid.querySelectorAll('[role="gridcell"]'));
        const r = +cell.dataset.r, c = +cell.dataset.c;
        const maxR = Math.max(...cells.map(n => +n.dataset.r));
        const rowMax = (row) => Math.max(...cells.filter(n => +n.dataset.r === row).map(n => +n.dataset.c));
        const mv = { ArrowUp: [-1, 0], ArrowDown: [1, 0], ArrowLeft: [0, -1], ArrowRight: [0, 1] }[e.key];
        let nr = r, nc = c;
        if (mv) { nr = Math.max(0, Math.min(maxR, r + mv[0])); nc = Math.max(0, Math.min(rowMax(nr), c + mv[1])); }
        else if (e.key === 'Home') nc = 0; else if (e.key === 'End') nc = rowMax(r); else return;
        e.preventDefault();
        const next = cells.find(n => +n.dataset.r === nr && +n.dataset.c === nc);
        if (next && next !== cell) { cell.tabIndex = -1; next.tabIndex = 0; next.focus(); }
      });

      const views = { map: false, cal: false };
      /* ---------- Table views ---------- */
      const setView = (which, on) => {
        views[which] = on;
        const btn = $(`[data-act="${which === 'map' ? 'mm' : 'cal'}-view"]`);
        const card = btn.closest('.yu-card'), chart = card.querySelector('.yu-chart');
        btn.setAttribute('aria-pressed', String(on));
        btn.querySelector('span').textContent = on ? (which === 'map' ? 'Map view' : 'Calendar view') : 'Table view';
        if (!chart) return;
        chart.querySelector('[data-view="map"]').hidden = on;
        chart.querySelector('[data-view="table"]').hidden = !on;
        hideTip(chart);
        const lg = card.querySelector('.yu-legend'); if (lg) lg.hidden = on;
        const kh = card.querySelector('[data-keyhelp]'); if (kh) kh.hidden = on;
      };

      /* Self-marked work (N01): ticks the learner gave themselves. Kept out of the mastery map and every prerequisite. */
      const selfHTML = () => {
        const rows = Object.entries(S.selfMarked || {}).filter(([, v]) => v && v.seen).map(([k, v]) => ({ label: skillLabel[k] || k, c: v.correct | 0, t: v.seen | 0 })).sort((a, b) => a.label.localeCompare(b.label));
        if (!rows.length) return '';
        return `<div class="yu-card-h"><div><h2 class="t-h1" id="yu-sm-h">Self-marked</h2>
            <p class="t-caption secondary">Written answers you marked yourself. They do not move the mastery map or unlock anything.</p></div></div>
          <div class="yu-tablewrap" tabindex="0" role="region" aria-label="Self-marked work as a table"><table class="yu-tbl">
            <caption class="sr-only">Self-marked answers by skill</caption>
            <thead><tr><th scope="col">Skill</th><th scope="col" class="num">Marked right</th></tr></thead>
            <tbody>${rows.map(r => `<tr><td>${esc(r.label)}</td><td class="num tnum">${r.c} of ${r.t}</td></tr>`).join('')}</tbody></table></div>`;
      };
      const paint = {
        head: () => { $('[data-card="head"]').innerHTML = headerHTML(); },
        hours: () => { const f = $('[data-log]'); const keep = f ? { block: f.block.value, date: f.date.value } : null; $('[data-card="hours"]').innerHTML = hoursHTML(); if (keep) { const g = $('[data-log]'); g.block.value = keep.block; g.date.value = keep.date; } },
        drills: () => { $('[data-card="drills"]').innerHTML = drillsHTML(); },
        map: () => { $('[data-card="map"]').innerHTML = mapHTML(); $('[data-card="maptable"]').innerHTML = mapTable(); const sm = $('[data-card="selfmarked"]'), h = selfHTML(); sm.innerHTML = h; sm.hidden = !h; },
        cal: () => { $('[data-card="cal"]').innerHTML = calHTML(); setView('cal', views.cal); },
        exams: () => {
          const rows = examRows();
          $('[data-ex-sub]').textContent = rows.length ? `${rows.filter(e => e.passed).length} passed, ${rows.filter(e => !e.passed).length} not passed. Open one to see marks by skill.` : 'Your topic and stage exams appear here.';
          $('[data-card="exams"]').innerHTML = examsHTML();
        },
        capstone: () => { $('[data-card="capstone"]').innerHTML = capstoneHTML(); },
        settings: () => { $('[data-card="settings"]').innerHTML = settingsHTML(); },
      };
      const paintAll = () => Object.values(paint).forEach(f => f());
      paintAll();
      /* Pass marks come from the exam files; fetch the ones in the history, then fill them in */
      const examIds = Array.from(new Set(examRows().map(e => e.id)));
      if (examIds.length) Promise.all(examIds.map(id => Promise.resolve(C.exam(id)).then(d => { if (d) examDocs[id] = d; }).catch(() => null))).then(() => { if ($('[data-card="exams"]')) paint.exams(); });

      /* ---------- Sheets ---------- */
      const examSheet = (e) => {
        const pm = passMark(e.id);
        const skills = Object.entries(e.bySkill || {}).map(([s, v]) => { const [c, t] = Array.isArray(v) ? v : [v, v]; const doc = examDocs[e.id]; return { s, c, t, label: (doc && doc.skills && doc.skills[s]) || skillLabel[s] || s }; });
        const under = pm == null ? [] : skills.filter(x => x.t && x.c / x.t < pm);
        const listAnd = (a) => (a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1]);
        const share = e.items ? e.score / e.items : 0;
        const note = !skills.length ? '' : under.length ? `Under the pass mark on ${listAnd(under.map(x => `${esc(x.label)} (${x.c} of ${x.t})`))}. Questions you missed went to your redo queue.` : 'Every skill at or above the pass mark.';
        Z.sheet(`<div class="yu-sh" data-track="${esc(e.track)}">
            <div class="yu-sh-h">${e.tag ? `<span class="yu-sh-tag">${esc(e.tag)}</span>` : ''}<div><h2 class="t-sheet-title">${esc(e.name)}</h2><p class="t-caption muted">${esc(e.kind)}${e.at ? ' · ' + dateLong(e.at) : ''}</p></div></div>
            <div class="yu-sh-score"><span class="t-stat tnum">${netOf(e) != null ? netOf(e) : Math.round(share * 100) + '%'}</span>
              <span class="yu-sh-meta"><span class="t-label tnum">${netOf(e) != null ? `net score, ${e.score} of ${e.items} right` : `${e.score} of ${e.items} correct`}</span>${passText(e.id) ? `<span class="t-caption muted tnum">Pass mark ${passText(e.id)}</span>` : pm == null ? '' : `<span class="t-caption muted tnum">Pass mark ${Math.round(pm * 100)}%</span>`}</span>
              ${e.passed ? `<span class="chip correct">${icon('check', 'xs')}Passed</span>` : `<span class="chip notyet">${icon('cross', 'xs')}Not passed</span>`}</div>
            ${skills.length ? `<div class="yu-sh-sk">
              <p class="t-caption secondary">Share correct in each skill.${pm == null ? '' : ` The dashed line is the ${Math.round(pm * 100)}% pass mark.`}</p>
              <ul style="--pm:${pm == null ? -10 : pm * 100}%">${skills.map(x => `<li><span class="t-label">${esc(x.label)}</span><span class="t-caption tnum muted">${x.c} of ${x.t}</span>
                <span class="yu-sh-bar${pm == null ? ' no-pm' : ''}" role="img" aria-label="${esc(x.label)}: ${x.c} of ${x.t}, ${x.t ? Math.round(x.c / x.t * 100) : 0}%"><i style="width:${x.t ? (x.c / x.t * 100).toFixed(1) : 0}%"></i></span></li>`).join('')}</ul>
            </div>` : ''}
            ${note ? `<p class="t-body yu-sh-note">${note}</p>` : ''}
            <div class="yu-sh-acts"><a class="btn secondary" href="#exam/${esc(e.id)}">Open this exam</a></div>
          </div>`, { label: `${e.name}${e.at ? ', ' + dateLong(e.at) : ''}` });
      };
      const keysSheet = () => Z.sheet(`<div class="yu-sh">
          <h2 class="t-sheet-title">Keyboard shortcuts</h2>
          ${SHORTCUTS.map(([g, list]) => `<div class="yu-sh-keys"><h3 class="t-overline muted">${g}</h3><dl>${list.map(([k, d, sep]) =>
            `<div><dt>${k.map(x => `<kbd>${esc(x)}</kbd>`).join(sep ? `<span class="muted">${sep}</span>` : '')}</dt><dd>${d}</dd></div>`).join('')}</dl></div>`).join('')}
        </div>`, { label: 'Keyboard shortcuts' });

      /* Export: the whole state document as JSON */
      const download = (blob, name) => {
        const url = URL.createObjectURL(blob), a = document.createElement('a');
        a.href = url; a.download = name; document.body.append(a); a.click(); a.remove();
        setTimeout(() => URL.revokeObjectURL(url), 2000);
      };
      const exportState = () => {
        const name = `zq-state-${D.todayKey()}.json`;
        download(new Blob([S.export()], { type: 'application/json' }), name);
        Z.toast(`${icon('check', 'sm')}<span>Saved as ${esc(name)}. Check your downloads folder.</span>`);
      };
      /* Import: read the file, show what it holds, replace on confirmation */
      const importErr = (msg) => { const el = $('[data-import-err]'); if (el) el.textContent = msg || ''; };
      const importFile = (file) => {
        importErr('');
        const rd = new FileReader();
        rd.onerror = () => importErr('That file could not be read.');
        rd.onload = () => {
          const text = String(rd.result || '');
          let raw = null;
          try { raw = JSON.parse(text); } catch { importErr('That file is not valid JSON.'); return; }
          const lessons = raw && raw.lessons ? Object.values(raw.lessons).filter(l => l && l.done).length : 0;
          const close = Z.sheet(`<div class="yu-sh">
              <h2 class="t-sheet-title">Replace your progress?</h2>
              <p class="t-body">${esc(file.name)} holds ${raw && raw.profile && raw.profile.name ? esc(raw.profile.name) + '’s' : 'a'} record: ${plural(lessons, 'lesson', 'lessons')} complete and ${plural(Number(raw && raw.xp) || 0, 'XP', 'XP')}.</p>
              <p class="t-caption muted">Everything in this browser is replaced, settings included. Export first if you want to keep it.</p>
              <p class="t-caption yu-err" data-imp-msg role="alert"></p>
              <div class="yu-sh-acts"><button type="button" class="btn secondary" data-close autofocus>Cancel</button><button type="button" class="btn" data-replace>Replace</button></div>
            </div>`, { modal: true, label: 'Replace your progress' });
          const b = document.querySelector('.yu-sh [data-replace]');
          b && b.addEventListener('click', () => {
            const r = S.import(text);
            if (!r || !r.ok) { const m = document.querySelector('.yu-sh [data-imp-msg]'); if (m) m.textContent = (r && r.error) || 'That file could not be imported.'; importErr((r && r.error) || 'That file could not be imported.'); return; }
            close();
            Z.toast(`${icon('check', 'sm')}<span>Imported ${esc(file.name)}.</span>`);
            Z.go(S.flags.setupDone ? 'you' : 'setup');
          });
        };
        rd.readAsText(file);
      };
      /* Reset: typed confirmation */
      const resetSheet = () => {
        const close = Z.sheet(`<div class="yu-sh">
            <h2 class="t-sheet-title">Reset everything?</h2>
            <p class="t-body">This clears your streak, XP, mastery points, mastery map, lessons, exams, drills, hours and settings. It cannot be undone.</p>
            <p class="t-caption muted">Export first if you want to keep a copy.</p>
            <label class="yu-sh-f"><span class="t-label">Type ${RESET_WORD} to confirm</span><input type="text" data-reset-word autocomplete="off" spellcheck="false" autocapitalize="characters" aria-describedby="yu-reset-help"></label>
            <p class="t-caption muted" id="yu-reset-help">Capital letters, as shown.</p>
            <div class="yu-sh-acts"><button type="button" class="btn secondary" data-close>Keep my progress</button><button type="button" class="btn notyet" data-reset disabled>Reset everything</button></div>
          </div>`, { modal: true, label: 'Reset everything' });
        const word = document.querySelector('.yu-sh [data-reset-word]'), b = document.querySelector('.yu-sh [data-reset]');
        if (!word || !b) return;
        setTimeout(() => word.focus(), 60);
        word.addEventListener('input', () => { b.disabled = word.value.trim() !== RESET_WORD; });
        word.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !b.disabled) b.click(); });
        b.addEventListener('click', () => { if (word.value.trim() !== RESET_WORD) return; S.reset(); close(); Z.go('setup'); });
      };

      /* ---------- Clicks ---------- */
      listen(root, 'click', (e) => {
        const ex = e.target.closest('[data-exam]'); if (ex) { examSheet(examRows()[+ex.dataset.exam]); return; }
        const tr = e.target.closest('[data-mmtrack]');
        if (tr) {
          const id = tr.dataset.mmtrack, open = tr.getAttribute('aria-expanded') !== 'true';
          if (open) openTracks.add(id); else openTracks.delete(id);
          tr.setAttribute('aria-expanded', String(open));
          const body = root.querySelector('#yu-mm-b-' + CSS.escape(id)); if (body) body.hidden = !open;
          return;
        }
        const b = e.target.closest('[data-act]'); if (!b) return;
        const a = b.dataset.act;
        if (a === 'streak') Z.streakSheet();
        else if (a === 'settings') { const s = $('#yu-settings'); s.scrollIntoView({ behavior: Z.reducedMotion() ? 'auto' : 'smooth', block: 'start' }); s.focus({ preventScroll: true }); }
        else if (a === 'mm-view') setView('map', !views.map);
        else if (a === 'cal-view') setView('cal', !views.cal);
        else if (a === 'keys') keysSheet();
        else if (a === 'setup') Z.go('setup');
        else if (a === 'system') Z.go('system');
        else if (a === 'export') exportState();
        else if (a === 'import') { importErr(''); const f = $('[data-import]'); f.value = ''; f.click(); }
        else if (a === 'reset') resetSheet();
      });

      /* ---------- Manual hours ---------- */
      listen(root, 'submit', (e) => {
        const f = e.target.closest('[data-log]'); if (!f) return;
        e.preventDefault();
        const msg = f.querySelector('.yu-log-msg');
        const minutes = Number(f.minutes.value), date = f.date.value, block = f.block.value;
        const fail = (t) => { msg.textContent = t; msg.classList.add('is-err'); f.minutes.setAttribute('aria-invalid', 'true'); };
        if (!Number.isFinite(minutes) || minutes < 1) return fail('Enter the minutes you studied, 1 or more.');
        if (minutes > 720) return fail('That is more than 12 hours. Log long days as two entries.');
        if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) return fail('Pick the date you studied.');
        if (date > D.todayKey()) return fail('The date cannot be in the future.');
        try { S.hours.log({ block, minutes, date, source: 'manual' }); } catch (err) { return fail(String(err.message || err)); }
        paint.hours(); paint.head(); paint.cal();
        const m2 = root.querySelector('[data-log] .yu-log-msg');
        if (m2) { m2.classList.remove('is-err'); m2.textContent = `Logged ${hm(minutes)} of ${BLOCKS.find(x => x[0] === block)[1].toLowerCase()} on ${dayLabel(date)}.`; }
      });
      listen(root, 'input', (e) => { if (e.target.closest('[data-log]')) { e.target.removeAttribute('aria-invalid'); const m = root.querySelector('[data-log] .yu-log-msg'); if (m && m.classList.contains('is-err')) { m.textContent = ''; m.classList.remove('is-err'); } } });

      /* ---------- Settings controls ---------- */
      const applyStreakMode = () => {
        const off = streakOff();
        root.querySelector('.yu').classList.toggle('is-streak-off', off);
        $('.yu-st').hidden = off;
        paint.head();
      };
      listen(root, 'change', (e) => {
        const t = e.target;
        if (t.matches('[data-import]')) { if (t.files && t.files[0]) importFile(t.files[0]); return; }
        if (t.name === 'yu-theme') Z.setSetting('theme', t.value);
        else if (t.name === 'yu-motion') Z.setSetting('motion', t.value);
        else if (t.id === 'yu-sound') { Z.setSetting('sound', t.checked); Z.sound('tap'); }
        else if (t.name === 'yu-goal') {
          S.profile.set({ weeklyGoalH: Number(t.value) });
          const h = $('#yu-h-goal'); if (h) h.textContent = goalHelp(Number(t.value));
          paint.head(); paint.hours();
        } else if (t.name === 'yu-track') { S.profile.set({ track: t.value }); paint.head(); }
        else if (t.id === 'yu-quantonly') { S.settings.set({ quantOnly: t.checked }); buildTopics(); paint.map(); paint.head(); }
        else if (t.id === 'yu-strictprereqs') { S.settings.set({ strictPrereqs: t.checked }); }
        else if (t.id === 'yu-streak') { S.settings.set({ streakMode: t.checked ? 'daily' : 'off' }); applyStreakMode(); Z.refreshShell(); }
      });

      /* Theme, motion and sound can also change from the screens panel: keep the radios in step */
      const offSettings = Z.on('settings', (s) => {
        const pick = (name, v) => { const r = root.querySelector(`input[name="yu-${name}"][value="${v}"]`); if (r) r.checked = true; };
        pick('theme', s.theme); pick('motion', s.motion);
        const so = root.querySelector('#yu-sound'); if (so) so.checked = !!s.sound;
      });

      /* QA hook for screenshots */
      window.ZQYouDebug = { tip: (sel) => { const c = Array.from(root.querySelectorAll(sel)).find(n => n.offsetParent); if (c) { c.scrollIntoView({ block: 'center' }); c.focus(); showTip(c); } }, view: setView, openAll: () => { trackIds.forEach(t => openTracks.add(t)); paint.map(); } };

      return () => { cleanups.forEach(f => f()); if (typeof offSettings === 'function') offSettings(); delete window.ZQYouDebug; };
    },
  });
})();
