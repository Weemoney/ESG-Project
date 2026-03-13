function animNum(id, target) {
const el = document.getElementById(id);
if (!el) return;
let start = null;
const step = (ts) => {
        if (!start) start = ts;
        const p = Math.min((ts - start) / 1400, 1);
        const e = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(e * target);
        if (p < 1) requestAnimationFrame(step);
        };
requestAnimationFrame(step);
}

window.addEventListener('load', () => {
    setTimeout(() => {
document.getElementById('b1').style.width = '87%';
document.getElementById('b2').style.width = '82%';
document.getElementById('b3').style.width = '68%';
    animNum('n1', 87);
    animNum('n2', 82);
    animNum('n3', 68);
    }, 600);
});