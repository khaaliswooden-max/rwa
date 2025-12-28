import { useState } from 'react';
import {
  CheckCircleIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  DocumentTextIcon,
  CalendarIcon,
} from '@heroicons/react/24/outline';

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
        return (
          <span className="flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full bg-emerald-100 text-emerald-700">
            <CheckCircleIcon className="w-3 h-3" />
            Completed
          </span>
        );
      case 'pending':
        return (
          <span className="flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full bg-amber-100 text-amber-700">
            <ClockIcon className="w-3 h-3" />
            Pending
          </span>
        );
      case 'overdue':
        return (
          <span className="flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full bg-red-100 text-red-700">
            <ExclamationTriangleIcon className="w-3 h-3" />
            Overdue
          </span>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Compliance</h1>
          <p className="text-slate-500 mt-1">
            Track regulatory obligations and manage reporting
          </p>
        </div>
        <button
          onClick={() => setShowReportModal(true)}
          className="px-4 py-2 bg-water-600 text-white rounded-lg text-sm font-medium hover:bg-water-700 transition-colors flex items-center gap-2"
        >
          <DocumentTextIcon className="w-5 h-5" />
          Generate Report
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="metric-card">
          <div className="metric-value">{mockSummary.compliance_score}</div>
          <div className="metric-label">Compliance Score</div>
          <div className="w-full bg-slate-200 rounded-full h-2 mt-2">
            <div
              className="bg-emerald-500 h-2 rounded-full"
              style={{ width: `${mockSummary.compliance_score}%` }}
            />
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-value text-emerald-600">{mockSummary.completed}</div>
          <div className="metric-label">Completed</div>
        </div>
        <div className="metric-card">
          <div className="metric-value text-amber-600">{mockSummary.pending}</div>
          <div className="metric-label">Pending</div>
        </div>
        <div className="metric-card">
          <div className="metric-value text-red-600">{mockSummary.overdue}</div>
          <div className="metric-label">Overdue</div>
        </div>
      </div>

      {/* Obligations Table */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200">
        <div className="p-4 border-b border-slate-200 flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-900">Obligations</h3>
          <div className="flex gap-2">
            {['all', 'pending', 'overdue', 'completed'].map((status) => (
              <button
                key={status}
                onClick={() => setStatusFilter(status)}
                className={`px-3 py-1.5 text-sm rounded-lg transition-colors ${
                  statusFilter === status
                    ? 'bg-water-600 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {status.charAt(0).toUpperCase() + status.slice(1)}
              </button>
            ))}
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="data-table">
            <thead>
              <tr>
                <th>Obligation</th>
                <th>Category</th>
                <th>Regulation</th>
                <th>Due Date</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredObligations.map((obligation) => (
                <tr key={obligation.id}>
                  <td>
                    <div className="font-medium">{obligation.title}</div>
                    <div className="text-xs text-slate-500">
                      {obligation.responsible}
                    </div>
                  </td>
                  <td>{obligation.category}</td>
                  <td className="text-xs text-slate-500">{obligation.regulation}</td>
                  <td>{new Date(obligation.due_date).toLocaleDateString()}</td>
                  <td>{getStatusBadge(obligation.status)}</td>
                  <td>
                    {obligation.status !== 'completed' && (
                      <button className="text-sm text-water-600 hover:text-water-700 font-medium">
                        Mark Complete
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
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <div className="flex items-center gap-2 mb-4">
          <CalendarIcon className="w-5 h-5 text-slate-400" />
          <h3 className="text-lg font-semibold text-slate-900">Upcoming Deadlines</h3>
        </div>
        <div className="space-y-3">
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
                  className={`flex items-center justify-between p-3 rounded-lg ${
                    isOverdue ? 'bg-red-50' : 'bg-slate-50'
                  }`}
                >
                  <div>
                    <div className="font-medium text-slate-900">{obligation.title}</div>
                    <div className="text-sm text-slate-500">{obligation.category}</div>
                  </div>
                  <div className="text-right">
                    <div
                      className={`text-sm font-medium ${
                        isOverdue ? 'text-red-600' : 'text-slate-600'
                      }`}
                    >
                      {isOverdue
                        ? `${Math.abs(daysUntil)} days overdue`
                        : `${daysUntil} days left`}
                    </div>
                    <div className="text-xs text-slate-400">
                      {dueDate.toLocaleDateString()}
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
            className="absolute inset-0 bg-slate-900/50"
            onClick={() => setShowReportModal(false)}
          />
          <div className="relative bg-white rounded-xl shadow-xl p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">
              Generate Report
            </h3>
            <div className="space-y-3">
              {reportTypes.map((report) => (
                <button
                  key={report.type}
                  className="w-full p-4 text-left rounded-lg border border-slate-200 hover:border-water-500 hover:bg-water-50 transition-colors"
                >
                  <div className="font-medium text-slate-900">{report.name}</div>
                  <div className="text-sm text-slate-500">{report.frequency}</div>
                </button>
              ))}
            </div>
            <button
              onClick={() => setShowReportModal(false)}
              className="mt-4 w-full py-2 text-sm text-slate-600 hover:text-slate-900"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

