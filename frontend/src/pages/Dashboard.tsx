import { Link } from 'react-router-dom';
import {
  BeakerIcon,
  BoltIcon,
  ClipboardDocumentCheckIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/outline';

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

function MetricCard({
  title,
  value,
  unit,
  trend,
  trendLabel,
  icon: Icon,
  color,
  href,
}: {
  title: string;
  value: string | number;
  unit?: string;
  trend?: number;
  trendLabel?: string;
  icon: React.ElementType;
  color: string;
  href: string;
}) {
  const isPositiveTrend = trend !== undefined && trend > 0;
  const trendColor =
    title === 'Energy Cost'
      ? trend && trend < 0
        ? 'text-emerald-600'
        : 'text-red-600'
      : trend && trend < 0
        ? 'text-emerald-600'
        : 'text-red-600';

  return (
    <Link to={href} className="metric-card card-hover group">
      <div className="flex items-start justify-between mb-4">
        <div
          className={`w-12 h-12 rounded-xl ${color} flex items-center justify-center`}
        >
          <Icon className="w-6 h-6 text-white" />
        </div>
        <span className="text-xs font-medium text-slate-400 group-hover:text-water-600 transition-colors">
          View details →
        </span>
      </div>
      <div className="metric-value">
        {value}
        {unit && <span className="text-lg font-normal text-slate-400 ml-1">{unit}</span>}
      </div>
      <div className="metric-label">{title}</div>
      {trend !== undefined && (
        <div className={`metric-trend ${trendColor}`}>
          {isPositiveTrend ? (
            <ArrowTrendingUpIcon className="w-4 h-4" />
          ) : (
            <ArrowTrendingDownIcon className="w-4 h-4" />
          )}
          <span>
            {Math.abs(trend)}% {trendLabel || 'vs last month'}
          </span>
        </div>
      )}
    </Link>
  );
}

function AlertCard({
  title,
  description,
  severity,
  time,
}: {
  title: string;
  description: string;
  severity: 'warning' | 'critical';
  time: string;
}) {
  return (
    <div
      className={`p-4 rounded-lg border-l-4 ${
        severity === 'critical'
          ? 'bg-red-50 border-red-500'
          : 'bg-amber-50 border-amber-500'
      }`}
    >
      <div className="flex items-start gap-3">
        <ExclamationTriangleIcon
          className={`w-5 h-5 flex-shrink-0 ${
            severity === 'critical' ? 'text-red-500' : 'text-amber-500'
          }`}
        />
        <div className="flex-1 min-w-0">
          <h4 className="font-medium text-slate-900">{title}</h4>
          <p className="text-sm text-slate-600 mt-0.5">{description}</p>
          <p className="text-xs text-slate-400 mt-2">{time}</p>
        </div>
      </div>
    </div>
  );
}

export default function Dashboard() {
  return (
    <div className="space-y-8">
      {/* Welcome section */}
      <div className="bg-gradient-to-r from-water-600 to-water-700 rounded-2xl p-6 lg:p-8 text-white">
        <h1 className="text-2xl lg:text-3xl font-bold mb-2">
          Good morning, Operator! 👋
        </h1>
        <p className="text-water-100">
          Here's what's happening with your water system today.
        </p>
      </div>

      {/* Key metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <MetricCard
          title="Non-Revenue Water"
          value={mockData.nrw.percentage}
          unit="%"
          trend={mockData.nrw.trend}
          icon={BeakerIcon}
          color="bg-water-500"
          href="/nrw"
        />
        <MetricCard
          title="Energy Cost"
          value={`$${mockData.energy.cost.toLocaleString()}`}
          trend={mockData.energy.trend}
          trendLabel="savings"
          icon={BoltIcon}
          color="bg-amber-500"
          href="/energy"
        />
        <MetricCard
          title="Compliance Score"
          value={mockData.compliance.score}
          unit="/100"
          icon={ClipboardDocumentCheckIcon}
          color="bg-emerald-500"
          href="/compliance"
        />
      </div>

      {/* Quick stats and alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick stats */}
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">
            System Overview
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-slate-50 rounded-lg">
              <div className="text-2xl font-bold text-slate-900">850</div>
              <div className="text-sm text-slate-500">Connections</div>
            </div>
            <div className="text-center p-4 bg-slate-50 rounded-lg">
              <div className="text-2xl font-bold text-slate-900">175K</div>
              <div className="text-sm text-slate-500">Gal/Day Avg</div>
            </div>
            <div className="text-center p-4 bg-slate-50 rounded-lg">
              <div className="text-2xl font-bold text-emerald-600">2</div>
              <div className="text-sm text-slate-500">Pumps Online</div>
            </div>
            <div className="text-center p-4 bg-slate-50 rounded-lg">
              <div className="text-2xl font-bold text-slate-900">72%</div>
              <div className="text-sm text-slate-500">Tank Level</div>
            </div>
          </div>

          {/* Mini chart placeholder */}
          <div className="mt-6 h-48 bg-slate-50 rounded-lg flex items-center justify-center">
            <p className="text-slate-400">Production Trend Chart</p>
          </div>
        </div>

        {/* Alerts */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">
            Active Alerts
          </h3>
          <div className="space-y-4">
            <AlertCard
              title="2 Overdue Obligations"
              description="Backflow testing and quarterly report need attention"
              severity="critical"
              time="Due 15 days ago"
            />
            <AlertCard
              title="High MNF Detected"
              description="Night flow 15% above baseline in Zone A"
              severity="warning"
              time="Detected 2 hours ago"
            />
            <AlertCard
              title="Pump Efficiency Low"
              description="PUMP-002 operating at 65% efficiency"
              severity="warning"
              time="Ongoing"
            />
          </div>
        </div>
      </div>

      {/* Upcoming deadlines */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">
          Upcoming Compliance Deadlines
        </h3>
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>Obligation</th>
                <th>Category</th>
                <th>Due Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="font-medium">Monthly Coliform Sampling</td>
                <td>Monitoring</td>
                <td>Jan 15, 2025</td>
                <td>
                  <span className="px-2 py-1 text-xs font-medium rounded-full bg-amber-100 text-amber-700">
                    Due in 5 days
                  </span>
                </td>
              </tr>
              <tr>
                <td className="font-medium">Monthly Operating Report</td>
                <td>Reporting</td>
                <td>Jan 28, 2025</td>
                <td>
                  <span className="px-2 py-1 text-xs font-medium rounded-full bg-slate-100 text-slate-600">
                    Due in 18 days
                  </span>
                </td>
              </tr>
              <tr>
                <td className="font-medium">Quarterly DBP Sampling</td>
                <td>Monitoring</td>
                <td>Feb 15, 2025</td>
                <td>
                  <span className="px-2 py-1 text-xs font-medium rounded-full bg-slate-100 text-slate-600">
                    Due in 36 days
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

