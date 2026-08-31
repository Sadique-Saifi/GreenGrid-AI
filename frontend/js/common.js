/* ============================================================
   common.js — shared across every page
   - highlights the active sidebar button (based on <body data-page>)
   - runs the live clock
   - sets shared Chart.js defaults (if Chart.js is loaded on the page)
   ============================================================ */

(function highlightActiveNav(){
  const current = document.body.dataset.page;
  document.querySelectorAll('.nav-btn').forEach(btn=>{
    btn.classList.toggle('active', btn.dataset.page === current);
  });
})();

function tickClock(){
  const el = document.getElementById('clock');
  if(!el) return;
  const d = new Date();
  el.textContent = d.toLocaleTimeString('en-IN', { hour12:false });
}
setInterval(tickClock, 1000);
tickClock();

if(window.Chart){
  Chart.defaults.color = '#84A395';
  Chart.defaults.font.family = "'Inter', sans-serif";
  Chart.defaults.font.size = 11;
}
