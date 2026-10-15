/* Lesson screen: a thin wrapper that mounts the lesson player (js/engine/player.js) from the route.
   Routes: #lesson/<course>/<lesson> starts or resumes, #lesson/<course>/<lesson>/quiz opens the quiz,
   #lesson/<course>/<lesson>/done opens the celebration. The router passes params as ['<course>', '<lesson>', ...];
   if it does not, the params are read from location.hash. A bare #lesson reopens the last lesson played. */
(function () {
  'use strict';

  const fromHash = () => {
    const parts = (location.hash || '').replace(/^#/, '').split('/').filter(Boolean).map(decodeURIComponent);
    return parts[0] === 'lesson' ? parts.slice(1) : [];
  };

  ZQ.screen({
    id: 'lesson', title: 'Lesson', hidden: true, shell: false,
    render(mount, api, params) {
      const Z = window.ZQ;
      let p = Array.isArray(params) && params.length ? params.slice() : fromHash();
      if (p.length < 2) {
        const last = Z.store.get('lesson.last', null);
        p = last && last.course && last.lesson ? [last.course, last.lesson] : ['conditional', 'l3-shrinking'];
      }
      const [course, lesson, start] = p;
      Z.store.set('lesson.last', { course, lesson });
      if (!Z.player) { mount.innerHTML = '<p style="padding:24px">The lesson player did not load.</p>'; return null; }
      return Z.player.mount(mount, { course, lesson, start: start || undefined });
    },
  });
})();
