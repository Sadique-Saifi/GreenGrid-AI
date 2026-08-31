/* ============================================================
   simulator.js — what-if simulator (sliders -> optimizer -> result)
   Mirrors the rule-based optimization logic described in the
   project synopsis (Case 1: generation > demand, Case 2: generation < demand)
   ============================================================ */

const simSolar  = document.getElementById('sim-solar');
const simDemand = document.getElementById('sim-demand');
const simBatt   = document.getElementById('sim-batt');

function runSim(){
  const s = parseFloat(simSolar.value);
  const d = parseFloat(simDemand.value);
  const b = parseFloat(simBatt.value);

  document.getElementById('sim-solar-val').textContent  = s + ' kW';
  document.getElementById('sim-demand-val').textContent = d + ' kW';
  document.getElementById('sim-batt-val').textContent   = b + '%';

  const solarToHouse    = Math.min(s, d);
  const surplus         = Math.max(0, s - d);
  const shortfall       = Math.max(0, d - s);
  const solarToBatt     = surplus;
  const battAvailableKw = (b - 15) / 100 * 100 * 0.5; // rough available discharge kW
  const battToHouse     = Math.min(shortfall, Math.max(0, battAvailableKw));
  const gridToHouse     = Math.max(0, shortfall - battToHouse);

  document.getElementById('res-solar-house').textContent = solarToHouse.toFixed(1) + ' kW';
  document.getElementById('res-batt-house').textContent  = battToHouse.toFixed(1) + ' kW';
  document.getElementById('res-solar-batt').textContent  = solarToBatt.toFixed(1) + ' kW';
  document.getElementById('res-grid').textContent        = gridToHouse.toFixed(1) + ' kW';
  document.getElementById('res-cost').textContent        = 'Rs. ' + Math.round((solarToHouse + battToHouse) * 7.2);
  document.getElementById('res-co2').textContent         = ((solarToHouse + battToHouse) * 0.45).toFixed(1) + ' kg';

  let note = 'Surplus solar is charging the battery — no grid dependency right now.';
  if(gridToHouse > 0.5){
    note = `Solar and battery can't fully cover demand — drawing ${gridToHouse.toFixed(1)} kW from the grid.`;
  } else if(battToHouse > 0.5){
    note = `Solar generation is low — battery is discharging ${battToHouse.toFixed(1)} kW to cover the shortfall.`;
  }
  document.getElementById('res-note').textContent = note;
}

[simSolar, simDemand, simBatt].forEach(s => s.addEventListener('input', runSim));
document.getElementById('sim-run').addEventListener('click', runSim);
document.getElementById('sim-cloudy').addEventListener('click', () => { simSolar.value = 12; runSim(); });
document.getElementById('sim-peak').addEventListener('click', () => { simDemand.value = 55; runSim(); });
runSim();
