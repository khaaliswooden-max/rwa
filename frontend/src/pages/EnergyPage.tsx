import { useState } from 'react';

// Mock data
const mockSummary = {
  total_energy_kwh: 45000,
  total_cost_usd: 5400,
  average_efficiency: 0.68,
  peak_demand_kw: 125,
  off_peak_usage_percentage: 42,
  potential_savings_usd: 810,
};

const mockPumps = [
  {
    id: 'pump-001',
    name: 'Main Well Pump',
    status: 'running',
    efficiency: 0.72,
    runtime: 8.5,
    power: 22,
  },
  {
    id: 'pump-002',
    name: 'Booster Pump A',
    status: 'idle',
    efficiency: 0.65,
    runtime: 3.2,
    power: 15,
  },
];

const mockSchedule = [
  { hour: 0, pump: true, rate: 0.08, level: 340 },
  { hour: 1, pump: true, rate: 0.08, level: 380 },
  { hour: 2, pump: true, rate: 0.08, level: 420 },
  { hour: 3, pump: false, rate: 0.08, level: 400 },
  { hour: 4, pump: false, rate: 0.08, level: 380 },
  { hour: 5, pump: false, rate: 0.08, level: 350 },
  { hour: 6, pump: false, rate: 0.12, level: 310 },
  { hour: 7, pump: false, rate: 0.12, level: 260 },
  { hour: 8, pump: false, rate: 0.12, level: 210 },
  { hour: 9, pump: true, rate: 0.12, level: 180 },
  { hour: 10, pump: true, rate: 0.12, level: 210 },
  { hour: 11, pump: false, rate: 0.12, level: 180 },
];

export default function EnergyPage() {
  const [selectedPump, setSelectedPump] = useState('pump-001');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-semibold text-black tracking-tight">Energy Management</h1>
        <p className="text-sm text-gray-500 mt-1">
          Optimize pump operations and reduce energy costs
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-px bg-gray-200">
        <div className="metric-card">
          <div className="metric-value">${mockSummary.total_cost_usd.toLocaleString()}</div>
          <div className="metric-label">MONTHLY COST</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{mockSummary.total_energy_kwh.toLocaleString()}</div>
          <div className="text-xs font-mono text-gray-400 -mt-1">kWh</div>
          <div className="metric-label">ENERGY USAGE</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{(mockSummary.average_efficiency * 100).toFixed(0)}</div>
          <div className="text-xs font-mono text-gray-400 -mt-1">%</div>
          <div className="metric-label">AVG EFFICIENCY</div>
          <div className="text-xs font-mono text-amber-600 mt-1">Below target (75%)</div>
        </div>
        <div className="metric-card bg-green-50 border-green-200">
          <div className="metric-value text-green-600">${mockSummary.potential_savings_usd}</div>
          <div className="metric-label text-green-700">POTENTIAL SAVINGS</div>
          <div className="text-xs font-mono text-green-600 mt-1">15% through optimization</div>
        </div>
      </div>

      {/* Pump Status */}
      <div className="panel">
        <div className="panel-header">
          <h3 className="panel-title">PUMP STATUS</h3>
        </div>
        <div className="panel-body">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {mockPumps.map((pump) => (
              <div
                key={pump.id}
                className={`p-4 border cursor-pointer transition-colors ${
                  selectedPump === pump.id
                    ? 'border-black bg-gray-50'
                    : 'border-gray-200 hover:border-gray-400'
                }`}
                onClick={() => setSelectedPump(pump.id)}
              >
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-medium text-black text-sm">{pump.name}</h4>
                  <span
                    className={`badge ${
                      pump.status === 'running' ? 'badge-ok' : 'badge-neutral'
                    }`}
                  >
                    {pump.status.toUpperCase()}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <div className="text-xl font-mono font-semibold text-black">
                      {(pump.efficiency * 100).toFixed(0)}%
                    </div>
                    <div className="text-xs text-gray-500 uppercase tracking-wider">Efficiency</div>
                  </div>
                  <div>
                    <div className="text-xl font-mono font-semibold text-black">
                      {pump.runtime}h
                    </div>
                    <div className="text-xs text-gray-500 uppercase tracking-wider">Runtime</div>
                  </div>
                  <div>
                    <div className="text-xl font-mono font-semibold text-black">
                      {pump.power}kW
                    </div>
                    <div className="text-xs text-gray-500 uppercase tracking-wider">Power</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Optimized Schedule */}
      <div className="panel">
        <div className="panel-header flex items-center justify-between">
          <h3 className="panel-title">OPTIMIZED PUMP SCHEDULE</h3>
          <button className="btn btn-primary text-xs">
            GENERATE NEW SCHEDULE
          </button>
        </div>
        <div className="panel-body">
          <div className="overflow-x-auto">
            <div className="min-w-[600px]">
              {/* Schedule visualization */}
              <div className="flex items-end gap-0.5 h-32 mb-2">
                {mockSchedule.map((hour) => (
                  <div
                    key={hour.hour}
                    className="flex-1 flex flex-col items-center"
                  >
                    <div
                      className={`w-full ${hour.pump ? 'bg-black' : 'bg-gray-200'}`}
                      style={{ height: `${(hour.level / 500) * 100}%` }}
                    />
                  </div>
                ))}
              </div>
              <div className="flex gap-0.5">
                {mockSchedule.map((hour) => (
                  <div
                    key={hour.hour}
                    className="flex-1 text-center text-xs text-gray-500 font-mono"
                  >
                    {hour.hour.toString().padStart(2, '0')}
                  </div>
                ))}
              </div>
              <div className="flex gap-0.5 mt-1">
                {mockSchedule.map((hour) => (
                  <div
                    key={hour.hour}
                    className={`flex-1 text-center text-xs font-mono ${
                      hour.rate > 0.1 ? 'text-red-500' : 'text-green-600'
                    }`}
                  >
                    ${hour.rate}
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="flex items-center gap-6 mt-6 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-black" />
              <span className="text-gray-600">PUMP ON</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-gray-200" />
              <span className="text-gray-600">PUMP OFF</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-green-600 font-mono">$0.08</span>
              <span className="text-gray-400">OFF-PEAK</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-red-500 font-mono">$0.12</span>
              <span className="text-gray-400">PEAK</span>
            </div>
          </div>
        </div>
      </div>

      {/* Time-of-Use Analysis */}
      <div className="panel">
        <div className="panel-header">
          <h3 className="panel-title">TIME-OF-USE DISTRIBUTION</h3>
        </div>
        <div className="panel-body">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 border border-green-200 bg-green-50">
              <div className="text-2xl font-mono font-semibold text-green-700">42%</div>
              <div className="text-xs uppercase tracking-wider text-green-600 mt-1">OFF-PEAK USAGE</div>
              <div className="text-xs font-mono text-gray-500 mt-2">$0.08/kWh · 10pm-6am</div>
            </div>
            <div className="p-4 border border-amber-200 bg-amber-50">
              <div className="text-2xl font-mono font-semibold text-amber-700">33%</div>
              <div className="text-xs uppercase tracking-wider text-amber-600 mt-1">MID-PEAK USAGE</div>
              <div className="text-xs font-mono text-gray-500 mt-2">$0.12/kWh · 6am-2pm</div>
            </div>
            <div className="p-4 border border-red-200 bg-red-50">
              <div className="text-2xl font-mono font-semibold text-red-700">25%</div>
              <div className="text-xs uppercase tracking-wider text-red-600 mt-1">ON-PEAK USAGE</div>
              <div className="text-xs font-mono text-gray-500 mt-2">$0.18/kWh · 2pm-10pm</div>
            </div>
          </div>
          <p className="text-sm text-gray-500 mt-4">
            Recommendation: Shift 15% more usage to off-peak hours to save approximately $810/month.
          </p>
        </div>
      </div>
    </div>
  );
}
