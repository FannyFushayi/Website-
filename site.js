/* Small progressive enhancements; all content and navigation are static HTML. */
(() => {
  const nav = document.querySelector('.site-nav');
  const button = nav?.querySelector('.menu');
  const links = nav?.querySelector('.nav-links');
  if (button && links) {
    nav.classList.add('enhanced');
    const close = () => { links.classList.remove('open'); button.setAttribute('aria-expanded', 'false'); button.textContent = 'Menu'; };
    button.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      button.setAttribute('aria-expanded', String(open));
      button.textContent = open ? 'Close' : 'Menu';
    });
    links.addEventListener('click', e => { if (e.target.closest('a')) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && links.classList.contains('open')) { close(); button.focus(); } });
    document.addEventListener('click', e => { if (!nav.contains(e.target)) close(); });
    const update = () => nav.classList.toggle('is-scrolled', window.scrollY > 36);
    window.addEventListener('scroll', update, { passive: true }); update();
  }
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!reduced && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('show'); observer.unobserve(entry.target); }
    }), { threshold: 0.08 });
    document.querySelectorAll('.reveal').forEach(el => {
      el.classList.add('will-reveal'); observer.observe(el);
    });
  }
})();
