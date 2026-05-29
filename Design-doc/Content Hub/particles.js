// Ambient particle field — drifts behind everything, tints to --page-accent.
// Reads the CSS variable each frame so the color follows view changes.

(function () {
  if (window.__particlesMounted) return;
  window.__particlesMounted = true;

  const canvas = document.createElement("canvas");
  canvas.id = "__particles";
  canvas.setAttribute("aria-hidden", "true");
  canvas.style.cssText =
    "position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:0;";
  // Insert as the first body child so app content stacks above it
  if (document.body) document.body.prepend(canvas);
  else document.addEventListener("DOMContentLoaded", () => document.body.prepend(canvas));

  const ctx = canvas.getContext("2d");
  const DPR = Math.min(window.devicePixelRatio || 1, 2);
  let W = 0;
  let H = 0;

  function resize() {
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = W * DPR;
    canvas.height = H * DPR;
    canvas.style.width = W + "px";
    canvas.style.height = H + "px";
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  }
  resize();
  window.addEventListener("resize", resize);

  // Tune density to viewport area — dense, visible field
  const targetCount = () => Math.min(220, Math.floor((W * H) / 9500));

  const rand = (a, b) => a + Math.random() * (b - a);
  const particles = [];
  function spawn(n) {
    for (let i = 0; i < n; i++) {
      particles.push({
        x: Math.random() * W,
        y: Math.random() * H,
        vx: rand(-0.1, 0.1),
        vy: rand(-0.08, 0.08),
        r: rand(0.7, 2.3),
        baseA: rand(0.32, 0.78),
        twinkle: Math.random() * Math.PI * 2,
        twinkleSpeed: rand(0.008, 0.022),
        big: Math.random() < 0.08, // ~8% are larger "stars" with halo
      });
    }
  }
  spawn(targetCount());

  // Color parsing — accept #rrggbb, #rgb, rgb(), or oklch fallback
  let lastColorStr = "";
  let lastRGB = [91, 141, 239];
  function readAccent() {
    const s = getComputedStyle(document.documentElement)
      .getPropertyValue("--page-accent")
      .trim() || "#5B8DEF";
    if (s === lastColorStr) return lastRGB;
    lastColorStr = s;

    // Parse hex
    let m = s.match(/^#([0-9a-f]{3,8})$/i);
    if (m) {
      let h = m[1];
      if (h.length === 3) h = h.split("").map((c) => c + c).join("");
      const r = parseInt(h.slice(0, 2), 16);
      const g = parseInt(h.slice(2, 4), 16);
      const b = parseInt(h.slice(4, 6), 16);
      lastRGB = [r, g, b];
      return lastRGB;
    }
    // Parse rgb()
    m = s.match(/rgba?\(([^)]+)\)/i);
    if (m) {
      const parts = m[1].split(",").map((p) => parseFloat(p.trim()));
      lastRGB = [parts[0] | 0, parts[1] | 0, parts[2] | 0];
      return lastRGB;
    }
    // Fallback — paint a single pixel through a temp canvas
    try {
      const tmp = document.createElement("canvas");
      tmp.width = tmp.height = 1;
      const tctx = tmp.getContext("2d");
      tctx.fillStyle = s;
      tctx.fillRect(0, 0, 1, 1);
      const d = tctx.getImageData(0, 0, 1, 1).data;
      lastRGB = [d[0], d[1], d[2]];
    } catch (e) {
      // keep last
    }
    return lastRGB;
  }

  // Smooth color transition between view changes
  const cur = [91, 141, 239];
  function stepColor() {
    const tgt = readAccent();
    cur[0] += (tgt[0] - cur[0]) * 0.04;
    cur[1] += (tgt[1] - cur[1]) * 0.04;
    cur[2] += (tgt[2] - cur[2]) * 0.04;
  }

  const MAX_LINK = 165;
  let t = 0;
  function frame() {
    t += 0.016;
    stepColor();
    const r = cur[0] | 0;
    const g = cur[1] | 0;
    const b = cur[2] | 0;

    ctx.clearRect(0, 0, W, H);

    // Particles
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.twinkle += p.twinkleSpeed;
      if (p.x < -20) p.x = W + 20;
      if (p.x > W + 20) p.x = -20;
      if (p.y < -20) p.y = H + 20;
      if (p.y > H + 20) p.y = -20;
      const a = p.baseA * (0.55 + 0.45 * Math.sin(p.twinkle));

      // Bigger "star" particles get a soft halo
      if (p.big) {
        const halo = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 6);
        halo.addColorStop(0, `rgba(${r},${g},${b},${a * 0.55})`);
        halo.addColorStop(1, `rgba(${r},${g},${b},0)`);
        ctx.fillStyle = halo;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * 6, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${r},${g},${b},${a})`;
      ctx.fill();
    }

    // Connecting lines (subtle web)
    for (let i = 0; i < particles.length; i++) {
      const a = particles[i];
      for (let j = i + 1; j < particles.length; j++) {
        const c = particles[j];
        const dx = a.x - c.x;
        const dy = a.y - c.y;
        const d2 = dx * dx + dy * dy;
        if (d2 < MAX_LINK * MAX_LINK) {
          const d = Math.sqrt(d2);
          const alpha = 0.11 * (1 - d / MAX_LINK);
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(c.x, c.y);
          ctx.strokeStyle = `rgba(${r},${g},${b},${alpha})`;
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      }
    }

    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
