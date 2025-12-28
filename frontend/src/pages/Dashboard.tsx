import { Link } from 'react-router-dom';

// Mock data - in production would come from API
const mockData = {
  nrw: {
    percentage: 22.5,
    trend: -3.2,
    volume: 4500,
  },
  energy: {
    cost: 5400,
    trend: -15.0,
    efficiency: 68,
  },
  compliance: {
    score: 85,
    pending: 4,
    overdue: 2,
  },
};

const systemStats = [
  { label: 'CONNECTIONS', value: '850', unit: '' },
  { label: 'AVG FLOW', value: '175', unit: 'K GAL/D' },
  { label: 'PUMPS', value: '2', unit: 'ONLINE' },
  { label: 'TANK', value: '72', unit: '%' },
];

const alerts = [
  { id: 1, code: 'OBL-002', message: '2 Overdue obligations require attention', severity: 'error', time: '15D AGO' },
  { id: 2, code: 'MNF-001', message: 'High minimum night flow detected in Zone A', severity: 'warn', time: '2H AGO' },
  { id: 3, code: 'PMP-002', message: 'Pump efficiency below threshold at 65%', severity: 'warn', time: 'ONGOING' },
];

const upcomingDeadlines = [
  { obligation: 'Monthly Coliform Sampling', category: 'MONITORING', due: 'JAN 15', status: 'Due in 5 days', statusType: 'warn' },
  { obligation: 'Monthly Operating Report', category: 'REPORTING', due: 'JAN 28', status: 'Due in 18 days', statusType: 'neutral' },
  { obligation: 'Quarterly DBP Sampling', category: 'MONITORING', due: 'FEB 15', status: 'Due in 36 days', statusType: 'neutral' },
];

export default function Dashboard() {
  return (
    <div className="space-y-6">
      {/* Header metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-px bg-gray-200">
        {/* NRW */}
        <Link to="/nrw" className="metric-card group hover:bg-gray-50 transition-colors">
          <div className="flex items-baseline justify-between">
            <span className="text-xs text-gray-400 font-mono">01</span>
            <span className="text-xs text-gray-400 group-hover:text-black transition-colors">→</span>
          </div>
          <div className="mt-4">
            <div className="metric-value">{mockData.nrw.percentage}</div>
            <div className="text-xs font-mono text-gray-400 -mt-1">%</div>
          </div>
          <div className="metric-label">NON-REVENUE WATER</div>
          <div className="metric-trend text-green-600 font-mono">
            <span>↓</span>
            <span>{Math.abs(mockData.nrw.trend)}% vs last month</span>
          </div>
        </Link>

        {/* Energy */}
        <Link to="/energy" className="metric-card group hover:bg-gray-50 transition-colors">
          <div className="flex items-baseline justify-between">
            <span className="text-xs text-gray-400 font-mono">02</span>
            <span className="text-xs text-gray-400 group-hover:text-black transition-colors">→</span>
          </div>
          <div className="mt-4">
            <div className="metric-value">${mockData.energy.cost.toLocaleString()}</div>
          </div>
          <div className="metric-label">ENERGY COST</div>
          <div className="metric-trend text-green-600 font-mono">
            <span>↓</span>
            <span>{Math.abs(mockData.energy.trend)}% savings</span>
          </div>
        </Link>

        {/* Compliance */}
        <Link to="/compliance" className="metric-card group hover:bg-gray-50 transition-colors">
          <div className="flex items-baseline justify-between">
            <span className="text-xs text-gray-400 font-mono">03</span>
            <span className="text-xs text-gray-400 group-hover:text-black transition-colors">→</span>
          </div>
          <div className="mt-4">
            <div className="metric-value">{mockData.compliance.score}</div>
            <div className="text-xs font-mono text-gray-400 -mt-1">/100</div>
          </div>
          <div className="metric-label">COMPLIANCE SCORE</div>
          <div className="metric-trend text-gray-500 font-mono">
            <span>{mockData.compliance.pending} pending</span>
            <span className="mx-1">·</span>
            <span className="text-red-600">{mockData.compliance.overdue} overdue</span>
          </div>
        </Link>
      </div>

      {/* System overview + Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* System stats */}
        <div className="lg:col-span-2 panel">
          <div className="panel-header">
            <h3 className="panel-title">SYSTEM OVERVIEW</h3>
          </div>
          <div className="panel-body">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {systemStats.map((stat) => (
                <div key={stat.label} className="text-center py-4 border border-gray-100">
                  <div className="text-2xl font-mono font-semibold text-black">{stat.value}</div>
                  <div className="text-xs font-mono text-gray-400 mt-0.5">{stat.unit}</div>
                  <div className="text-xs text-gray-500 mt-2 uppercase tracking-wider">{stat.label}</div>
                </div>
              ))}
            </div>

            {/* Placeholder for chart */}
            <div className="mt-6 h-40 border border-gray-100 flex items-center justify-center">
              <div className="text-center">
                <div className="text-xs text-gray-400 uppercase tracking-wider">PRODUCTION TREND</div>
                <div className="text-xs text-gray-300 font-mono mt-1">[ CHART PLACEHOLDER ]</div>
              </div>
            </div>
          </div>
        </div>

        {/* Alerts */}
        <div className="panel">
          <div className="panel-header flex items-center justify-between">
            <h3 className="panel-title">ACTIVE ALERTS</h3>
            <span className="text-xs font-mono text-gray-400">{alerts.length}</span>
          </div>
          <div className="divide-y divide-gray-100">
            {alerts.map((alert) => (
              <div key={alert.id} className="px-5 py-4">
                <div className="flex items-start gap-3">
                  <span
                    className={`status-dot mt-1.5 ${
                      alert.severity === 'error' ? 'critical' : 'warning'
                    }`}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-mono text-gray-400">{alert.code}</span>
                    </div>
                    <p className="text-sm text-black mt-0.5">{alert.message}</p>
                    <p className="text-xs font-mono text-gray-400 mt-1">{alert.time}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Upcoming deadlines */}
      <div className="panel">
        <div className="panel-header">
          <h3 className="panel-title">UPCOMING COMPLIANCE DEADLINES</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>OBLIGATION</th>
                <th>CATEGORY</th>
                <th>DUE DATE</th>
                <th>STATUS</th>
              </tr>
            </thead>
            <tbody>
              {upcomingDeadlines.map((item, i) => (
                <tr key={i}>
                  <td className="font-medium text-black">{item.obligation}</td>
                  <td>
                    <span className="text-xs font-mono text-gray-500">{item.category}</span>
                  </td>
                  <td className="font-mono">{item.due}</td>
                  <td>
                    <span className={`badge ${item.statusType === 'warn' ? 'badge-warn' : 'badge-neutral'}`}>
                      {item.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
