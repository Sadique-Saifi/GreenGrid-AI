/* ============================================================
   forecast.js — 6-hour demand vs solar prediction chart
   TODO: replace static arrays with GET /forecast/demand + /forecast/solar
   ============================================================ */

const hrs = ['+1h','+2h','+3h','+4h','+5h','+6h'];

new Chart(document.getElementById('forecastChart'), {
  type: 'line',
  data: {
    labels: hrs,
    datasets: [
      { label:'Predicted demand (kWh)', data:[4.2,5.1,3.4,3.8,6.2,7.9], borderColor:'#7C93FF', backgroundColor:'rgba(124,147,255,0.08)', fill:true, tension:.4, pointRadius:3 },
      { label:'Predicted solar (kWh)', data:[3.1,1.8,0.6,0.1,0,0], borderColor:'#F2B705', backgroundColor:'rgba(242,183,5,0.08)', fill:true, tension:.4, pointRadius:3 },
    ]
  },
  options: {
    responsive:true, maintainAspectRatio:false,
    plugins:{ legend:{ position:'top', align:'end', labels:{ boxWidth:8, boxHeight:8, usePointStyle:true } } },
    scales:{ x:{ grid:{ display:false } }, y:{ grid:{ color:'rgba(237,242,239,0.05)' } } }
  }
});
