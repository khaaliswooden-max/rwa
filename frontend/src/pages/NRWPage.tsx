import { useState } from 'react';
import {
  ArrowTrendingDownIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
} from '@heroicons/react/24/outline';

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
          <h1 className="text-2xl font-bold text-slate-900">Non-Revenue Water</h1>
          <p className="text-slate-500 mt-1">
            Monitor water losses and optimize distribution efficiency
          </p>
        </div>
        <select
          value={selectedPeriod}
          onChange={(e) => setSelectedPeriod(e.target.value)}
          className="px-4 py-2 border border-slate-300 rounded-lg bg-white text-sm"
        >
          <option value="7">Last 7 days</option>
          <option value="30">Last 30 days</option>
          <option value="90">Last 90 days</option>
          <option value="365">Last year</option>
        </select>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="metric-card">
          <div className="metric-value text-water-600">
            {mockSummary.nrw_percentage}%
          </div>
          <div className="metric-label">NRW Percentage</div>
          <div className="metric-trend text-emerald-600">
            <ArrowTrendingDownIcon className="w-4 h-4" />
            <span>{Math.abs(mockSummary.trend_percentage)}% vs last period</span>
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{mockSummary.nrw_volume_m3.toLocaleString()}</div>
          <div className="metric-label">NRW Volume (m³)</div>
        </div>
        <div className="metric-card">
          <div className="metric-value text-red-600">
            {mockSummary.real_losses_m3.toLocaleString()}
          </div>
          <div className="metric-label">Real Losses (m³)</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{mockSummary.infrastructure_leakage_index}</div>
          <div className="metric-label">Infrastructure Leakage Index</div>
          <div className="text-xs text-slate-500 mt-1">Target: &lt; 2.0</div>
        </div>
      </div>

      {/* IWA Water Balance */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">
          IWA Water Balance
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Sankey-style breakdown */}
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <div className="w-32 text-sm text-slate-600">System Input</div>
              <div className="flex-1 h-8 bg-water-500 rounded text-white text-sm flex items-center px-3 font-medium">
                20,000 m³ (100%)
              </div>
            </div>
            <div className="flex items-center gap-3 pl-8">
              <div className="w-24 text-sm text-slate-600">Revenue Water</div>
              <div className="flex-1 h-8 bg-emerald-500 rounded text-white text-sm flex items-center px-3 font-medium">
                15,500 m³ (77.5%)
              </div>
            </div>
            <div className="flex items-center gap-3 pl-8">
              <div className="w-24 text-sm text-slate-600">Non-Revenue</div>
              <div className="flex-1 h-8 bg-amber-500 rounded text-white text-sm flex items-center px-3 font-medium">
                4,500 m³ (22.5%)
              </div>
            </div>
            <div className="flex items-center gap-3 pl-16">
              <div className="w-20 text-sm text-slate-500">Real Losses</div>
              <div className="flex-1 h-6 bg-red-400 rounded text-white text-xs flex items-center px-2">
                3,200 m³ (16%)
              </div>
            </div>
            <div className="flex items-center gap-3 pl-16">
              <div className="w-20 text-sm text-slate-500">Apparent</div>
              <div className="flex-1 h-6 bg-orange-400 rounded text-white text-xs flex items-center px-2">
                1,300 m³ (6.5%)
              </div>
            </div>
          </div>

          {/* Performance indicators */}
          <div className="space-y-4">
            <div className="p-4 bg-slate-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-slate-700">ILI Rating</span>
                <span className="px-2 py-1 text-xs font-medium rounded-full bg-amber-100 text-amber-700">
                  Good
                </span>
              </div>
              <p className="text-sm text-slate-500">
                ILI of 2.8 is within acceptable range but above world-class target of
                2.0
              </p>
            </div>
            <div className="p-4 bg-emerald-50 rounded-lg border border-emerald-200">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircleIcon className="w-5 h-5 text-emerald-600" />
                <span className="font-medium text-emerald-700">Improving Trend</span>
              </div>
              <p className="text-sm text-emerald-600">
                NRW has decreased 3.2% compared to previous period
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Zone Analysis */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">
          Distribution Zone Analysis
        </h3>
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>Zone</th>
                <th>ILI</th>
                <th>MNF (m³/h)</th>
                <th>Risk Level</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {mockZones.map((zone) => (
                <tr key={zone.id}>
                  <td className="font-medium">{zone.name}</td>
                  <td>{zone.ili}</td>
                  <td>{zone.mnf}</td>
                  <td>
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded-full ${
                        zone.risk === 'high'
                          ? 'bg-red-100 text-red-700'
                          : zone.risk === 'medium'
                            ? 'bg-amber-100 text-amber-700'
                            : 'bg-emerald-100 text-emerald-700'
                      }`}
                    >
                      {zone.risk}
                    </span>
                  </td>
                  <td>
                    <button className="text-sm text-water-600 hover:text-water-700 font-medium">
                      Analyze
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">
          Recommendations
        </h3>
        <div className="space-y-4">
          <div className="flex items-start gap-4 p-4 bg-amber-50 rounded-lg border border-amber-200">
            <ExclamationTriangleIcon className="w-6 h-6 text-amber-500 flex-shrink-0" />
            <div>
              <h4 className="font-medium text-slate-900">
                Zone C requires attention
              </h4>
              <p className="text-sm text-slate-600 mt-1">
                ILI of 4.8 is above target. Consider scheduling acoustic leak
                detection survey within the next 30 days.
              </p>
            </div>
          </div>
          <div className="flex items-start gap-4 p-4 bg-slate-50 rounded-lg">
            <CheckCircleIcon className="w-6 h-6 text-slate-400 flex-shrink-0" />
            <div>
              <h4 className="font-medium text-slate-900">Continue monitoring Zone B</h4>
              <p className="text-sm text-slate-600 mt-1">
                Performance is excellent with ILI of 2.1. Maintain current
                monitoring schedule.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

