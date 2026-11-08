// Night sky: a few tiny twinkling stars and, now and then, a faint falling star. Same as the app's home.
(function () {
  const forced = new URLSearchParams(location.search).get("theme");
  if (forced) document.documentElement.dataset.theme = forced;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.querySelectorAll("canvas.stars").forEach((canvas) => {
    const g = canvas.getContext("2d");
    let seed = 0x1dea11ce;
    const rand = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);
    const stars = Array.from({ length: 70 }, () => ({
      x: rand(), y: rand() * 0.8, r: 0.5 + rand() * 0.9, a: 0.18 + rand() * 0.35, s: 0.4 + rand() * 0.9, p: rand() * 6.28,
    }));
    let w = 0, h = 0;
    const size = () => {
      const dpr = Math.min(devicePixelRatio || 1, 2);
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr;
      g.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    size();
    addEventListener("resize", size);

    const draw = (ms) => {
      if (!canvas.offsetParent && getComputedStyle(canvas).display === "none") return requestAnimationFrame(draw);
      const t = still ? 0 : ms / 1000;
      g.clearRect(0, 0, w, h);
      for (const s of stars) {
        const tw = 0.65 + 0.35 * Math.sin(t * s.s + s.p);
        g.fillStyle = `rgba(255,246,218,${s.a * tw})`;
        g.beginPath(); g.arc(s.x * w, s.y * h, s.r, 0, 6.283); g.fill();
      }
      if (!still) {
        const every = 9, dur = 0.9, cycle = Math.floor(t / every);
        let fs = (cycle * 2654435761) >>> 0;
        const r2 = () => ((fs = (fs * 1664525 + 1013904223) >>> 0) / 4294967296);
        const p = (t - cycle * every) / dur;
        if (r2() < 0.65 && p >= 0 && p <= 1) {
          const sx = w * (0.25 + r2() * 0.65), sy = h * (0.05 + r2() * 0.3);
          const hx = sx - 0.86 * 220 * p, hy = sy + 0.5 * 220 * p;
          const tx = hx + 0.86 * 80, ty = hy - 0.5 * 80;
          const grad = g.createLinearGradient(tx, ty, hx, hy);
          grad.addColorStop(0, "rgba(255,255,255,0)");
          grad.addColorStop(1, `rgba(255,246,218,${Math.sin(p * Math.PI) * 0.6})`);
          g.strokeStyle = grad; g.lineWidth = 1.3; g.lineCap = "round";
          g.beginPath(); g.moveTo(tx, ty); g.lineTo(hx, hy); g.stroke();
        }
      }
      if (!still) requestAnimationFrame(draw);
    };
    requestAnimationFrame(draw);
  });

  // Fade sections in as they arrive.
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { threshold: 0.12 });
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));
})();
