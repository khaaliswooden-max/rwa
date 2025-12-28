import { useState } from 'react';

// Mock data
const mockSummary = {
  total_obligations: 24,
  completed: 18,
  pending: 4,
  overdue: 2,
  compliance_score: 85,
};

const mockObligations = [
  {
    id: 'obl-001',
    title: 'Monthly Coliform Sampling',
    category: 'Monitoring',
    regulation: 'EPA SDWA 40 CFR 141.21',
    due_date: '2025-01-15',
    status: 'pending',
    responsible: 'Operator',
  },
  {
    id: 'obl-002',
    title: 'Monthly Operating Report',
    category: 'Reporting',
    regulation: 'State Regulation',
    due_date: '2025-01-28',
    status: 'pending',
    responsible: 'Operator',
  },
  {
    id: 'obl-003',
    title: 'Backflow Prevention Testing',
    category: 'Operational',
    regulation: 'State Plumbing Code',
    due_date: '2024-12-31',
    status: 'overdue',
    responsible: 'Contractor',
  },
  {
    id: 'obl-004',
    title: 'Quarterly DBP Sampling',
    category: 'Monitoring',
    regulation: 'EPA SDWA 40 CFR 141.132',
    due_date: '2025-02-15',
    status: 'pending',
    responsible: 'Operator',
  },
  {
    id: 'obl-005',
    title: 'Daily Chlorine Checks',
    category: 'Monitoring',
    regulation: 'EPA SDWA 40 CFR 141.72',
    due_date: '2025-01-10',
    status: 'completed',
    responsible: 'Operator',
  },
];

const reportTypes = [
  { type: 'CCR', name: 'Consumer Confidence Report', frequency: 'Annual' },
  { type: 'MOR', name: 'Monthly Operating Report', frequency: 'Monthly' },
  { type: 'SAMPLING', name: 'Sampling Summary', frequency: 'As needed' },
];

export default function CompliancePage() {
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [showReportModal, setShowReportModal] = useState(false);

  const filteredObligations =
    statusFilter === 'all'
      ? mockObligations
      : mockObligations.filter((o) => o.status === statusFilter);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <span className="badge badge-ok">COMPLETED</span>;
      case 'pending':
        return <span className="badge badge-warn">PENDING</span>;
      case 'overdue':
        return <span className="badge badge-error">OVERDUE</span>;
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-black tracking-tight">Compliance</h1>
          <p className="text-sm text-gray-500 mt-1">
            Track regulatory obligations and manage reporting
          </p>
        </div>
        <button
          onClick={() => setShowReportModal(true)}
          className="btn btn-primary"
        >
          GENERATE REPORT
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-gray-200">
        <div className="metric-card">
          <div className="metric-value">{mockSummary.compliance_score}</div>
          <div className="metric-label">COMPLIANCE SCORE</div>
          <div className="w-full bg-gray-200 h-1 mt-3">
            <div
              className="bg-black h-1"
              style={{ width: `${mockSummary.compliance_score}%` }}
            />
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-value text-green-600">{mockSummary.completed}</div>
          <div className="metric-label">COMPLETED</div>
        </div>
        <div className="metric-card">
          <div className="metric-value text-amber-600">{mockSummary.pending}</div>
          <div className="metric-label">PENDING</div>
        </div>
        <div className="metric-card">
          <div className="metric-value text-red-600">{mockSummary.overdue}</div>
          <div className="metric-label">OVERDUE</div>
        </div>
      </div>

      {/* Obligations Table */}
      <div className="panel">
        <div className="panel-header flex items-center justify-between">
          <h3 className="panel-title">OBLIGATIONS</h3>
          <div className="flex gap-1">
            {['all', 'pending', 'overdue', 'completed'].map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`px-3 py-1.5 text-xs font-medium transition-colors ${
                  statusFilter === status
                    ? 'bg-black text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {status.toUpperCase()}
              </button>
            ))}
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>OBLIGATION</th>
                <th>CATEGORY</th>
                <th>REGULATION</th>
                <th>DUE DATE</th>
                <th>STATUS</th>
                <th>ACTION</th>
              </tr>
            </thead>
            <tbody>
              {filteredObligations.map((obligation) => (
                <tr key={obligation.id}>
                  <td>
                    <div className="font-medium text-black">{obligation.title}</div>
                    <div className="text-xs text-gray-500 font-mono mt-0.5">
                      {obligation.responsible}
                    </div>
                  </td>
                  <td>
                    <span className="text-xs font-mono text-gray-500 uppercase">
                      {obligation.category}
                    </span>
                  </td>
                  <td className="text-xs text-gray-500 font-mono">{obligation.regulation}</td>
                  <td className="font-mono">{new Date(obligation.due_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }).toUpperCase()}</td>
                  <td>{getStatusBadge(obligation.status)}</td>
                  <td>
                    {obligation.status !== 'completed' && (
                      <button className="text-xs text-black hover:underline font-medium">
                        MARK COMPLETE
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Calendar View */}
      <div className="panel">
        <div className="panel-header">
          <h3 className="panel-title">UPCOMING DEADLINES</h3>
        </div>
        <div className="divide-y divide-gray-100">
          {mockObligations
            .filter((o) => o.status !== 'completed')
            .sort((a, b) => new Date(a.due_date).getTime() - new Date(b.due_date).getTime())
            .slice(0, 5)
            .map((obligation) => {
              const dueDate = new Date(obligation.due_date);
              const today = new Date();
              const daysUntil = Math.ceil(
                (dueDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24)
              );
              const isOverdue = daysUntil < 0;

              return (
                <div
                  key={obligation.id}
                  className={`flex items-center justify-between px-5 py-4 ${
                    isOverdue ? 'bg-red-50' : ''
                  }`}
                >
                  <div>
                    <div className="font-medium text-black text-sm">{obligation.title}</div>
                    <div className="text-xs text-gray-500 uppercase tracking-wider mt-0.5">
                      {obligation.category}
                    </div>
                  </div>
                  <div className="text-right">
                    <div
                      className={`text-sm font-mono font-medium ${
                        isOverdue ? 'text-red-600' : 'text-gray-600'
                      }`}
                    >
                      {isOverdue
                        ? `${Math.abs(daysUntil)}D OVERDUE`
                        : `${daysUntil}D LEFT`}
                    </div>
                    <div className="text-xs text-gray-400 font-mono">
                      {dueDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }).toUpperCase()}
                    </div>
                  </div>
                </div>
              );
            })}
        </div>
      </div>

      {/* Report Generation Modal */}
      {showReportModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div
            className="absolute inset-0 bg-black/20"
            onClick={() => setShowReportModal(false)}
          />
          <div className="relative bg-white border border-gray-200 p-6 max-w-md w-full mx-4">
            <h3 className="text-sm uppercase tracking-wider text-gray-500 mb-4">
              GENERATE REPORT
            </h3>
            <div className="space-y-2">
              {reportTypes.map((report) => (
                <button
                  key={report.type}
                  className="w-full p-4 text-left border border-gray-200 hover:border-black hover:bg-gray-50 transition-colors"
                >
                  <div className="font-medium text-black text-sm">{report.name}</div>
                  <div className="text-xs text-gray-500 font-mono mt-0.5">{report.frequency}</div>
                </button>
              ))}
            </div>
            <button
              onClick={() => setShowReportModal(false)}
              className="mt-4 w-full py-2 text-xs text-gray-500 hover:text-black transition-colors"
            >
              CANCEL
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
