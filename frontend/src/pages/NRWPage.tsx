import { useState } from 'react';

// Mock data
const mockSummary = {
  nrw_percentage: 22.5,
  nrw_volume_m3: 4500,
  real_losses_m3: 3200,
  apparent_losses_m3: 1300,
  infrastructure_leakage_index: 2.8,
  trend: 'improving',
  trend_percentage: -3.2,
};

const mockZones = [
  { id: 'zone-a', name: 'Zone A - Downtown', ili: 3.5, mnf: 8.2, risk: 'medium' },
  { id: 'zone-b', name: 'Zone B - Residential', ili: 2.1, mnf: 5.4, risk: 'low' },
  { id: 'zone-c', name: 'Zone C - Industrial', ili: 4.8, mnf: 12.5, risk: 'high' },
];

export default function NRWPage() {
  const [selectedPeriod, setSelectedPeriod] = useState('30');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-black tracking-tight">Non-Revenue Water</h1>
          <p className="text-sm text-gray-500 mt-1">
            Monitor water losses and optimize distribution efficiency
          </p>
        </div>
        <select
          value={selectedPeriod}
          onChange={(e) => setSelectedPeriod(e.target.value)}
          className="input w-auto"
        >
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
          <option value="365">Last year</option>
        </select>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-px bg-gray-200">
        <div className="metric-card">
          <div className="metric-value">{mockSummary.nrw_percentage}</div>
          <div className="text-xs font-mono text-gray-400 -mt-1">%</div>
          <div className="metric-label">NRW PERCENTAGE</div>
          <div className="metric-trend text-green-600 font-mono">
            <span>↓</span>
            <span>{Math.abs(mockSummary.trend_percentage)}% vs last period</span>
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{mockSummary.nrw_volume_m3.toLocaleString()}</div>
          <div className="text-xs font-mono text-gray-400 -mt-1">m³</div>
          <div className="metric-label">NRW VOLUME</div>
        </div>
        <div className="metric-card">
          <div className="metric-value text-red-600">{mockSummary.real_losses_m3.toLocaleString()}</div>
          <div className="text-xs font-mono text-gray-400 -mt-1">m³</div>
          <div className="metric-label">REAL LOSSES</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{mockSummary.infrastructure_leakage_index}</div>
          <div className="metric-label">ILI</div>
          <div className="text-xs font-mono text-gray-400 mt-1">Target: &lt; 2.0</div>
        </div>
      </div>

      {/* IWA Water Balance */}
      <div className="panel">
        <div className="panel-header">
          <h3 className="panel-title">IWA WATER BALANCE</h3>
        </div>
        <div className="panel-body">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Sankey-style breakdown */}
            <div className="space-y-3 font-mono text-sm">
              <div className="flex items-center gap-3">
                <div className="w-28 text-gray-500 text-xs">SYSTEM INPUT</div>
                <div className="flex-1 h-8 bg-black text-white flex items-center px-3 text-xs">
                  20,000 m³ (100%)
                </div>
              </div>
              <div className="flex items-center gap-3 pl-6">
                <div className="w-22 text-gray-500 text-xs">REVENUE</div>
                <div className="flex-1 h-8 bg-green-600 text-white flex items-center px-3 text-xs">
                  15,500 m³ (77.5%)
                </div>
              </div>
              <div className="flex items-center gap-3 pl-6">
                <div className="w-22 text-gray-500 text-xs">NON-REV</div>
                <div className="flex-1 h-8 bg-amber-500 text-white flex items-center px-3 text-xs">
                  4,500 m³ (22.5%)
                </div>
              </div>
              <div className="flex items-center gap-3 pl-12">
                <div className="w-16 text-gray-400 text-xs">REAL</div>
                <div className="flex-1 h-6 bg-red-500 text-white flex items-center px-2 text-xs">
                  3,200 m³ (16%)
                </div>
              </div>
              <div className="flex items-center gap-3 pl-12">
                <div className="w-16 text-gray-400 text-xs">APPARENT</div>
                <div className="flex-1 h-6 bg-orange-400 text-white flex items-center px-2 text-xs">
                  1,300 m³ (6.5%)
                </div>
              </div>
            </div>

            {/* Performance indicators */}
            <div className="space-y-4">
              <div className="p-4 border border-gray-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs uppercase tracking-wider text-gray-500">ILI RATING</span>
                  <span className="badge badge-warn">GOOD</span>
                </div>
                <p className="text-sm text-gray-600">
                  ILI of 2.8 is within acceptable range but above world-class target of 2.0
                </p>
              </div>
              <div className="p-4 border border-green-200 bg-green-50">
                <div className="flex items-center gap-2 mb-2">
                  <span className="status-dot healthy" />
                  <span className="text-xs uppercase tracking-wider text-green-700">IMPROVING TREND</span>
                </div>
                <p className="text-sm text-green-700">
                  NRW has decreased 3.2% compared to previous period
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Zone Analysis */}
      <div className="panel">
        <div className="panel-header">
          <h3 className="panel-title">DISTRIBUTION ZONE ANALYSIS</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>ZONE</th>
                <th>ILI</th>
                <th>MNF (m³/h)</th>
                <th>RISK</th>
                <th>ACTION</th>
              </tr>
            </thead>
            <tbody>
              {mockZones.map((zone) => (
                <tr key={zone.id}>
                  <td className="font-medium text-black">{zone.name}</td>
                  <td className="font-mono">{zone.ili}</td>
                  <td className="font-mono">{zone.mnf}</td>
                  <td>
                    <span
                      className={`badge ${
                        zone.risk === 'high'
                          ? 'badge-error'
                          : zone.risk === 'medium'
                            ? 'badge-warn'
                            : 'badge-ok'
                      }`}
                    >
                      {zone.risk.toUpperCase()}
                    </span>
                  </td>
                  <td>
                    <button className="text-xs text-black hover:underline font-medium">
                      ANALYZE
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recommendations */}
      <div className="panel">
        <div className="panel-header">
          <h3 className="panel-title">RECOMMENDATIONS</h3>
        </div>
        <div className="divide-y divide-gray-100">
          <div className="p-5 flex items-start gap-4">
            <span className="status-dot warning mt-1.5" />
            <div>
              <h4 className="text-sm font-medium text-black">
                Zone C requires attention
              </h4>
              <p className="text-sm text-gray-600 mt-1">
                ILI of 4.8 is above target. Consider scheduling acoustic leak detection survey within the next 30 days.
              </p>
            </div>
          </div>
          <div className="p-5 flex items-start gap-4">
            <span className="status-dot healthy mt-1.5" />
            <div>
              <h4 className="text-sm font-medium text-black">Continue monitoring Zone B</h4>
              <p className="text-sm text-gray-600 mt-1">
                Performance is excellent with ILI of 2.1. Maintain current monitoring schedule.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
