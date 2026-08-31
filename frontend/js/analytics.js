/* ============================================================
   analytics.js — 7-day generation vs consumption chart + table
   TODO: replace static arrays with GET /energy/history
   ============================================================ */

const days    = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
const genData = [260,275,240,290,310,300,285];
const useData = [300,320,310,330,340,310,330];

new Chart(document.getElementById('analyticsChart'), {
  type: 'bar',
  data: {
    labels: days,
    datasets: [
      { label:'Generated (kWh)', data:genData, backgroundColor:'#F2B705', borderRadius:6, maxBarThickness:28 },
      { label:'Consumed (kWh)', data:useData, backgroundColor:'#7C93FF', borderRadius:6, maxBarThickness:28 },
    ]
  },
  options: {
    responsive:true, maintainAspectRatio:false,
    plugins:{ legend:{ position:'top', align:'end', labels:{ boxWidth:8, boxHeight:8, usePointStyle:true } } },
    scales:{ x:{ grid:{ display:false } }, y:{ grid:{ color:'rgba(237,242,239,0.05)' } } }
  }
});

const srcTags = {
  solar: '<span class="tag solar">Solar</span>',
  batt:  '<span class="tag batt">Battery</span>',
  grid:  '<span class="tag grid">Grid</span>'
};
const rows = [
  ['18:40','2.1 kW','5.4 kW','batt'],
  ['18:20','5.8 kW','5.0 kW','solar'],
  ['18:00','9.4 kW','4.8 kW','solar'],
  ['17:40','14.2 kW','4.6 kW','solar'],
  ['17:20','19.6 kW','4.9 kW','solar'],
];
document.getElementById('analytics-table').innerHTML = rows.map(r =>
  `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td><td>${(Math.random()*30+50).toFixed(0)}%</td><td>${srcTags[r[3]]}</td></tr>`
).join('');
