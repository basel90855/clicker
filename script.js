'use strict';

const button = document.getElementById('mariamButton');
const canvas = document.getElementById('confettiCanvas');
const ctx = canvas.getContext('2d');

let stateIndex = -1; // -1 = initial greeting at center
const states = [
  { leftPct: 50, topPct: 12, label: 'ops sorry u gotta follow up' },
  { leftPct: 50, topPct: 86, label: 'معلش بقي عارفك مش بتحبي المشي بس قربنا' },
  { leftPct: 88, topPct: 50, label: 'اخر مره' },
  { leftPct: 50, topPct: 50, label: 'اجدع رجالة المنوفيه', celebrate: true },
];

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Ensure button starts centered and idles subtly
function init() {
  setButtonPosition(50, 50);
  button.classList.add('idle');
}

function setButtonPosition(leftPct, topPct) {
  button.style.left = `${leftPct}%`;
  button.style.top = `${topPct}%`;
  // Keep translate to center anchor
  button.style.transform = 'translate(-50%, -50%)';
}

function nextState() {
  if (stateIndex === -1) {
    stateIndex = 0;
  } else {
    stateIndex = (stateIndex + 1) % states.length;
  }

  const current = states[stateIndex];
  button.classList.remove('idle');
  button.textContent = current.label;
  setButtonPosition(current.leftPct, current.topPct);

  if (current.celebrate) {
    burstConfetti();
    button.classList.add('pulse');
    setTimeout(() => button.classList.remove('pulse'), 1000);
  }
}

button.addEventListener('click', nextState);
init();

// Confetti animation
function burstConfetti() {
  const durationMs = 2200;
  const endTime = performance.now() + durationMs;
  const particles = createConfettiParticles(120);

  function frame(now) {
    // clear canvas with slight trail
    ctx.globalCompositeOperation = 'destination-out';
    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.globalCompositeOperation = 'lighter';

    for (const p of particles) {
      p.vy += p.gravity;
      p.x += p.vx;
      p.y += p.vy;
      p.rotation += p.rotationSpeed;

      // wrap horizontally a bit for fun
      if (p.x < -20) p.x = canvas.width + 20;
      if (p.x > canvas.width + 20) p.x = -20;

      drawConfettiParticle(p);
    }

    if (now < endTime) {
      requestAnimationFrame(frame);
    }
  }

  requestAnimationFrame(frame);
}

function createConfettiParticles(count) {
  const colors = ['#8a5cff', '#00e0ff', '#ff5cab', '#ffd166', '#06d6a0'];
  const particles = [];
  const originX = canvas.width / 2;
  const originY = canvas.height / 2;

  for (let i = 0; i < count; i++) {
    const angle = (Math.random() * Math.PI * 2);
    const speed = 3 + Math.random() * 4.5;
    particles.push({
      x: originX + Math.cos(angle) * 10,
      y: originY + Math.sin(angle) * 10,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed - 2,
      size: 6 + Math.random() * 6,
      color: colors[Math.floor(Math.random() * colors.length)],
      rotation: Math.random() * Math.PI,
      rotationSpeed: (Math.random() - 0.5) * 0.3,
      gravity: 0.08 + Math.random() * 0.12,
      shape: Math.random() < 0.5 ? 'rect' : 'triangle',
    });
  }
  return particles;
}

function drawConfettiParticle(p) {
  ctx.save();
  ctx.translate(p.x, p.y);
  ctx.rotate(p.rotation);
  ctx.fillStyle = p.color;

  if (p.shape === 'rect') {
    ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
  } else {
    ctx.beginPath();
    ctx.moveTo(0, -p.size / 1.5);
    ctx.lineTo(p.size / 1.2, p.size / 1.5);
    ctx.lineTo(-p.size / 1.2, p.size / 1.5);
    ctx.closePath();
    ctx.fill();
  }

  ctx.restore();
}