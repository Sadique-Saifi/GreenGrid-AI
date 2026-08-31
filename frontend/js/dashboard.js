/* ============================================================
   dashboard.js — live metrics, energy-flow diagram, live chart
   Simulated data now; swap the marked TODOs for real fetch()
   calls to your FastAPI backend (GET /energy/current, etc.)
   ============================================================ */

let solar = 42, demand = 31, batt = 66;

function randWalk(v, min, max, step){
  v += (Math.random() - 0.5) * step;
  return Math.max(min, Math.min(max, v));
}

function updateDashboard(){
  // TODO: replace the two lines below with a fetch('/energy/current')
  solar = randWalk(solar, 10, 50, 3);
  demand = randWalk(demand, 15, 45, 2);

  const toHouse   = Math.min(solar, demand);
  const surplus   = Math.max(0, solar - demand);
  const shortfall = Math.max(0, demand - solar);
  const toBatt    = Math.min(surplus, 15);
  const fromBatt  = Math.min(shortfall, batt > 15 ? shortfall : 0);
  const fromGrid  = Math.max(0, shortfall - fromBatt);
  batt = Math.max(10, Math.min(98, batt + (toBatt > 0 ? toBatt * 0.06 : -fromBatt * 0.05)));
  const renewPct  = Math.min(100, Math.round(((toHouse + toBatt) / (demand + toBatt || 1)) * 100));

  document.getElementById('v-solar').innerHTML   = solar.toFixed(1) + '<span>kW</span>';
  document.getElementById('v-demand').innerHTML  = demand.toFixed(1) + '<span>kW</span>';
  document.getElementById('v-battery').innerHTML = Math.round(batt) + '<span>%</span>';
  document.getElementById('v-grid').innerHTML    = fromGrid.toFixed(1) + '<span>kW</span>';
  document.getElementById('v-renew').innerHTML   = renewPct + '<span>%</span>';

  document.getElementById('s-grid').textContent = fromGrid > 0.5
    ? `Drawing ${fromGrid.toFixed(1)} kW from grid` : 'No grid draw needed';
  document.getElementById('s-battery').textContent = toBatt > 0.3
    ? `▲ Charging · ${toBatt.toFixed(1)} kW in`
    : (fromBatt > 0.3 ? `▼ Discharging · ${fromBatt.toFixed(1)} kW out` : 'Idle');

  document.getElementById('flow-total').textContent = solar.toFixed(0) + ' kW';
  document.getElementById('flow-solar-lbl').textContent = solar.toFixed(0) + ' kW';
  document.getElementById('flow-to-house').textContent = toHouse.toFixed(1) + ' kW';
  document.getElementById('flow-to-batt').textContent =
    (toBatt + fromBatt > 0 ? (toBatt > 0 ? toBatt : fromBatt).toFixed(1) : '0.0') + ' kW';
  document.getElementById('flow-batt-soc').textContent = Math.round(batt) + '% SOC';

  const now = new Date().toLocaleTimeString('en-IN', { hour12:false, hour:'2-digit', minute:'2-digit', second:'2-digit' });
  liveChart.data.labels.push(now);
  liveChart.data.datasets[0].data.push(solar);
  liveChart.data.datasets[1].data.push(demand);
  liveChart.data.datasets[2].data.push(batt / 2);
  if(liveChart.data.labels.length > 20){
    liveChart.data.labels.shift();
    liveChart.data.datasets.forEach(ds => ds.data.shift());
  }
  liveChart.update('none');
}

const liveChart = new Chart(document.getElementById('liveChart'), {
  type: 'line',
  data: {
    labels: [],
    datasets: [
      { label:'Solar (kW)', data:[], borderColor:'#F2B705', backgroundColor:'rgba(242,183,5,0.08)', tension:.35, fill:true, pointRadius:0, borderWidth:2 },
      { label:'Demand (kW)', data:[], borderColor:'#7C93FF', backgroundColor:'rgba(124,147,255,0.06)', tension:.35, fill:true, pointRadius:0, borderWidth:2 },
      { label:'Battery/2 (%)', data:[], borderColor:'#2FD4B0', backgroundColor:'transparent', tension:.35, fill:false, pointRadius:0, borderWidth:1.5, borderDash:[4,3] },
    ]
  },
  options: {
    responsive:true, maintainAspectRatio:false,
    interaction:{ intersect:false, mode:'index' },
    plugins:{ legend:{ position:'top', align:'end', labels:{ boxWidth:8, boxHeight:8, usePointStyle:true } } },
    scales:{
      x:{ grid:{ color:'rgba(237,242,239,0.05)' }, ticks:{ maxTicksLimit:6 } },
      y:{ grid:{ color:'rgba(237,242,239,0.05)' } }
    }
  }
});

setInterval(updateDashboard, 3000);
updateDashboard();
