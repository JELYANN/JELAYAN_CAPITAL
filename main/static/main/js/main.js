// main.js
document.addEventListener('DOMContentLoaded', function () {
  // Smooth scroll on nav clicks
  document.querySelectorAll('.nav-link').forEach(link=>{
    link.addEventListener('click', e=>{
      e.preventDefault();
      document.querySelectorAll('.nav-link').forEach(l=>l.classList.remove('active'));
      e.currentTarget.classList.add('active');
      const target = document.querySelector(e.currentTarget.getAttribute('href'));
      target.scrollIntoView({behavior:'smooth', block:'start'});
    });
  });

  // GSAP animations
  if(window.gsap && window.ScrollTrigger){
    gsap.registerPlugin(ScrollTrigger);

    // big heading reveal (fade + slide)
    gsap.utils.toArray('.panel').forEach((panel, i) => {
      const title = panel.querySelector('.big');
      const eyebrow = panel.querySelector('.eyebrow');
      const sub = panel.querySelector('.sub');

      gsap.from([eyebrow, title, sub], {
        scrollTrigger: {
          trigger: panel,
          start: 'top 60%',
        },
        y: 30,
        opacity: 0,
        stagger: 0.12,
        duration: 0.9,
        ease: 'power2.out'
      });

      // highlight nav item on enter
      const id = panel.getAttribute('id');
      if(id){
        ScrollTrigger.create({
          trigger: panel,
          start: 'top 45%',
          end: 'bottom 45%',
          onEnter: () => setActiveNav(id),
          onEnterBack: () => setActiveNav(id)
        });
      }
    });

    // subtle parallax on background
    gsap.to('.hero-bg', {
      yPercent: 10,
      ease: 'none',
      scrollTrigger: {
        scrub: 0.7
      }
    });
  } // end gsap

  function setActiveNav(id){
    document.querySelectorAll('.nav-link').forEach(a=>{
      a.classList.toggle('active', a.getAttribute('href') === `#${id}`);
    });
  }

  // initial active
  setTimeout(()=>{ // highlight first on load
    setActiveNav('tesis');
  }, 80);
});
