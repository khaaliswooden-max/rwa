import { useState } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';
import {
  CloudArrowUpIcon,
  ClockIcon,
  CheckCircleIcon,
  PlusIcon,
} from '@heroicons/react/24/outline';

// Mock data
const mockSources = [
  {
    id: 'src-001',
    type: 'manual',
    name: 'Manual Entry',
    enabled: true,
    status: 'active',
    last_data: '2025-01-10T10:30:00Z',
  },
  {
    id: 'src-002',
    type: 'scada',
    name: 'Well House SCADA',
    enabled: true,
    status: 'connected',
    last_data: '2025-01-10T10:30:00Z',
  },
];

const mockHistory = [
  {
    id: 'ing-001',
    source: 'SCADA',
    timestamp: '2025-01-10T10:30:00Z',
    records: 48,
    status: 'success',
  },
  {
    id: 'ing-002',
    source: 'Manual Entry',
    timestamp: '2025-01-10T09:15:00Z',
    records: 1,
    status: 'success',
  },
  {
    id: 'ing-003',
    source: 'CSV Upload',
    timestamp: '2025-01-09T14:00:00Z',
    records: 850,
    status: 'success',
  },
];

interface MeterReadingForm {
  meter_id: string;
  reading_value: number;
  reading_type: string;
  notes: string;
}

export default function DataPage() {
  const [showEntryForm, setShowEntryForm] = useState(false);
  const { register, handleSubmit, reset } = useForm<MeterReadingForm>();

  const onSubmit = async (data: MeterReadingForm) => {
    // Mock submission
    console.log('Submitting:', data);
    toast.success('Reading submitted successfully');
    reset();
    setShowEntryForm(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Data Management</h1>
          <p className="text-slate-500 mt-1">
            Manage data sources and manual entry
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowEntryForm(true)}
            className="px-4 py-2 bg-water-600 text-white rounded-lg text-sm font-medium hover:bg-water-700 transition-colors flex items-center gap-2"
          >
            <PlusIcon className="w-5 h-5" />
            Manual Entry
          </button>
          <button className="px-4 py-2 bg-white border border-slate-300 text-slate-700 rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors flex items-center gap-2">
            <CloudArrowUpIcon className="w-5 h-5" />
            Upload CSV
          </button>
        </div>
      </div>

      {/* Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="metric-card">
          <div className="flex items-center gap-2 mb-2">
            <span className="status-dot healthy" />
            <span className="text-sm font-medium text-emerald-600">System Online</span>
          </div>
          <div className="metric-value">2</div>
          <div className="metric-label">Active Data Sources</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">1,450</div>
          <div className="metric-label">Records Today</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">0</div>
          <div className="metric-label">Errors (24h)</div>
        </div>
      </div>

      {/* Data Sources */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Data Sources</h3>
        <div className="space-y-4">
          {mockSources.map((source) => (
            <div
              key={source.id}
              className="flex items-center justify-between p-4 bg-slate-50 rounded-lg"
            >
              <div className="flex items-center gap-4">
                <div
                  className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    source.type === 'scada'
                      ? 'bg-water-100 text-water-600'
                      : 'bg-amber-100 text-amber-600'
                  }`}
                >
                  {source.type === 'scada' ? '📡' : '✏️'}
                </div>
                <div>
                  <div className="font-medium text-slate-900">{source.name}</div>
                  <div className="text-sm text-slate-500">
                    Last data:{' '}
                    {new Date(source.last_data).toLocaleString()}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <span
                  className={`flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium ${
                    source.status === 'connected' || source.status === 'active'
                      ? 'bg-emerald-100 text-emerald-700'
                      : 'bg-slate-100 text-slate-600'
                  }`}
                >
                  <span
                    className={`w-2 h-2 rounded-full ${
                      source.status === 'connected' || source.status === 'active'
                        ? 'bg-emerald-500'
                        : 'bg-slate-400'
                    }`}
                  />
                  {source.status}
                </span>
                <button className="text-sm text-water-600 hover:text-water-700 font-medium">
                  Configure
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Ingestion History */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">
          Recent Data Imports
        </h3>
        <div className="space-y-3">
          {mockHistory.map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between p-3 bg-slate-50 rounded-lg"
            >
              <div className="flex items-center gap-3">
                <CheckCircleIcon className="w-5 h-5 text-emerald-500" />
                <div>
                  <div className="font-medium text-slate-900">{item.source}</div>
                  <div className="text-sm text-slate-500">
                    {item.records} records imported
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-500">
                <ClockIcon className="w-4 h-4" />
                {new Date(item.timestamp).toLocaleString()}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Data Freshness */}
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Data Freshness</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-emerald-50 rounded-lg">
            <div className="text-sm text-emerald-600 font-medium">
              Production Meters
            </div>
            <div className="text-lg font-bold text-emerald-700 mt-1">
              5 minutes ago
            </div>
            <div className="text-xs text-slate-500 mt-1">Real-time via SCADA</div>
          </div>
          <div className="p-4 bg-amber-50 rounded-lg">
            <div className="text-sm text-amber-600 font-medium">Customer Meters</div>
            <div className="text-lg font-bold text-amber-700 mt-1">Monthly</div>
            <div className="text-xs text-slate-500 mt-1">Due in 15 days</div>
          </div>
          <div className="p-4 bg-water-50 rounded-lg">
            <div className="text-sm text-water-600 font-medium">Energy Data</div>
            <div className="text-lg font-bold text-water-700 mt-1">Daily</div>
            <div className="text-xs text-slate-500 mt-1">Updated this morning</div>
          </div>
        </div>
      </div>

      {/* Manual Entry Modal */}
      {showEntryForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div
            className="absolute inset-0 bg-slate-900/50"
            onClick={() => setShowEntryForm(false)}
          />
          <div className="relative bg-white rounded-xl shadow-xl p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">
              Manual Meter Reading
            </h3>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Meter ID
                </label>
                <input
                  {...register('meter_id', { required: true })}
                  type="text"
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-water-500 focus:border-water-500"
                  placeholder="e.g., PROD-001"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Reading Value
                </label>
                <input
                  {...register('reading_value', { required: true })}
                  type="number"
                  step="0.01"
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-water-500 focus:border-water-500"
                  placeholder="e.g., 175250.00"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Meter Type
                </label>
                <select
                  {...register('reading_type')}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-water-500 focus:border-water-500"
                >
                  <option value="production">Production</option>
                  <option value="distribution">Distribution</option>
                  <option value="customer">Customer</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Notes (optional)
                </label>
                <textarea
                  {...register('notes')}
                  rows={2}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-water-500 focus:border-water-500"
                  placeholder="Any additional notes..."
                />
              </div>
              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowEntryForm(false)}
                  className="flex-1 py-2 text-sm text-slate-600 hover:text-slate-900 border border-slate-300 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2 text-sm text-white bg-water-600 hover:bg-water-700 rounded-lg font-medium"
                >
                  Submit Reading
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

