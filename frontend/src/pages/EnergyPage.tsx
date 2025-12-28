import { useState } from 'react';
import { BoltIcon, ClockIcon, CurrencyDollarIcon } from '@heroicons/react/24/outline';

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
        <h1 className="text-2xl font-bold text-slate-900">Energy Management</h1>
        <p className="text-slate-500 mt-1">
          Optimize pump operations and reduce energy costs
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="metric-card">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center">
              <CurrencyDollarIcon className="w-5 h-5 text-amber-600" />
            </div>
          </div>
          <div className="metric-value">${mockSummary.total_cost_usd.toLocaleString()}</div>
          <div className="metric-label">Monthly Energy Cost</div>
        </div>
        <div className="metric-card">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-water-100 flex items-center justify-center">
              <BoltIcon className="w-5 h-5 text-water-600" />
            </div>
          </div>
          <div className="metric-value">{mockSummary.total_energy_kwh.toLocaleString()}</div>
          <div className="metric-label">Energy (kWh)</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{(mockSummary.average_efficiency * 100).toFixed(0)}%</div>
          <div className="metric-label">Average Efficiency</div>
          <div className="text-xs text-amber-600 mt-1">Below target (75%)</div>
        </div>
        <div className="metric-card bg-emerald-50 border-emerald-200">
          <div className="metric-value text-emerald-600">
            ${mockSummary.potential_savings_usd}
          </div>
          <div className="metric-label">Potential Monthly Savings</div>
          <div className="text-xs text-emerald-600 mt-1">15% through optimization</div>
        </div>
      </div>

      {/* Pump Status */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Pump Status</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {mockPumps.map((pump) => (
            <div
              key={pump.id}
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all ${
                selectedPump === pump.id
                  ? 'border-water-500 bg-water-50'
                  : 'border-slate-200 hover:border-slate-300'
              }`}
              onClick={() => setSelectedPump(pump.id)}
            >
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-medium text-slate-900">{pump.name}</h4>
                <span
                  className={`flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium ${
                    pump.status === 'running'
                      ? 'bg-emerald-100 text-emerald-700'
                      : 'bg-slate-100 text-slate-600'
                  }`}
                >
                  <span
                    className={`w-2 h-2 rounded-full ${
                      pump.status === 'running' ? 'bg-emerald-500' : 'bg-slate-400'
                    }`}
                  />
                  {pump.status}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-lg font-semibold text-slate-900">
                    {(pump.efficiency * 100).toFixed(0)}%
                  </div>
                  <div className="text-xs text-slate-500">Efficiency</div>
                </div>
                <div>
                  <div className="text-lg font-semibold text-slate-900">
                    {pump.runtime}h
                  </div>
                  <div className="text-xs text-slate-500">Runtime Today</div>
                </div>
                <div>
                  <div className="text-lg font-semibold text-slate-900">
                    {pump.power}kW
                  </div>
                  <div className="text-xs text-slate-500">Power</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Optimized Schedule */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-slate-900">
            Optimized Pump Schedule
          </h3>
          <button className="px-4 py-2 bg-water-600 text-white rounded-lg text-sm font-medium hover:bg-water-700 transition-colors">
            Generate New Schedule
          </button>
        </div>
        <div className="overflow-x-auto">
          <div className="min-w-[600px]">
            {/* Schedule visualization */}
            <div className="flex items-end gap-1 h-32 mb-2">
              {mockSchedule.map((hour) => (
                <div
                  key={hour.hour}
                  className="flex-1 flex flex-col items-center"
                >
                  <div
                    className={`w-full rounded-t ${
                      hour.pump ? 'bg-water-500' : 'bg-slate-200'
                    }`}
                    style={{ height: `${(hour.level / 500) * 100}%` }}
                  />
                </div>
              ))}
            </div>
            <div className="flex gap-1">
              {mockSchedule.map((hour) => (
                <div
                  key={hour.hour}
                  className="flex-1 text-center text-xs text-slate-500"
                >
                  {hour.hour}
                </div>
              ))}
            </div>
            <div className="flex gap-1 mt-1">
              {mockSchedule.map((hour) => (
                <div
                  key={hour.hour}
                  className={`flex-1 text-center text-xs ${
                    hour.rate > 0.1 ? 'text-red-500' : 'text-emerald-500'
                  }`}
                >
                  ${hour.rate}
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-6 mt-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-water-500 rounded" />
            <span className="text-slate-600">Pump Running</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-slate-200 rounded" />
            <span className="text-slate-600">Pump Off</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-emerald-500">Green Rate</span>
            <span className="text-slate-400">= Off-Peak</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-red-500">Red Rate</span>
            <span className="text-slate-400">= Peak</span>
          </div>
        </div>
      </div>

      {/* Time-of-Use Analysis */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">
          Time-of-Use Distribution
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-emerald-50 rounded-lg">
            <div className="text-2xl font-bold text-emerald-700">42%</div>
            <div className="text-sm text-emerald-600">Off-Peak Usage</div>
            <div className="text-xs text-slate-500 mt-1">$0.08/kWh • 10pm-6am</div>
          </div>
          <div className="p-4 bg-amber-50 rounded-lg">
            <div className="text-2xl font-bold text-amber-700">33%</div>
            <div className="text-sm text-amber-600">Mid-Peak Usage</div>
            <div className="text-xs text-slate-500 mt-1">$0.12/kWh • 6am-2pm</div>
          </div>
          <div className="p-4 bg-red-50 rounded-lg">
            <div className="text-2xl font-bold text-red-700">25%</div>
            <div className="text-sm text-red-600">On-Peak Usage</div>
            <div className="text-xs text-slate-500 mt-1">$0.18/kWh • 2pm-10pm</div>
          </div>
        </div>
        <p className="text-sm text-slate-500 mt-4">
          Recommendation: Shift 15% more usage to off-peak hours to save approximately
          $810/month.
        </p>
      </div>
    </div>
  );
}

