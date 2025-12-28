import { useState } from 'react';
import { useForm } from 'react-hook-form';
import toast from 'react-hot-toast';

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
    console.log('Submitting:', data);
    toast.success('Reading submitted');
    reset();
    setShowEntryForm(false);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl font-semibold text-black tracking-tight">Data Management</h1>
          <p className="text-sm text-gray-500 mt-1">
            Manage data sources and manual entry
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setShowEntryForm(true)}
            className="btn btn-primary"
          >
            + MANUAL ENTRY
          </button>
          <button className="btn btn-secondary">
            ↑ UPLOAD CSV
          </button>
        </div>
      </div>

      {/* Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-px bg-gray-200">
        <div className="metric-card">
          <div className="flex items-center gap-2 mb-2">
            <span className="status-dot healthy" />
            <span className="text-xs uppercase tracking-wider text-green-600">SYSTEM ONLINE</span>
          </div>
          <div className="metric-value">2</div>
          <div className="metric-label">ACTIVE SOURCES</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">1,450</div>
          <div className="metric-label">RECORDS TODAY</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">0</div>
          <div className="metric-label">ERRORS (24H)</div>
        </div>
      </div>

      {/* Data Sources */}
      <div className="panel">
        <div className="panel-header">
          <h3 className="panel-title">DATA SOURCES</h3>
        </div>
        <div className="divide-y divide-gray-100">
          {mockSources.map((source) => (
            <div
              key={source.id}
              className="flex items-center justify-between px-5 py-4"
            >
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 border border-gray-200 flex items-center justify-center text-sm font-mono">
                  {source.type === 'scada' ? '📡' : '✏️'}
                </div>
                <div>
                  <div className="font-medium text-black text-sm">{source.name}</div>
                  <div className="text-xs text-gray-500 font-mono">
                    Last: {new Date(source.last_data).toLocaleTimeString('en-US', { hour12: false })}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <span
                  className={`badge ${
                    source.status === 'connected' || source.status === 'active'
                      ? 'badge-ok'
                      : 'badge-neutral'
                  }`}
                >
                  {source.status.toUpperCase()}
                </span>
                <button className="text-xs text-black hover:underline font-medium">
                  CONFIGURE
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Ingestion History */}
      <div className="panel">
        <div className="panel-header">
          <h3 className="panel-title">RECENT DATA IMPORTS</h3>
        </div>
        <div className="divide-y divide-gray-100">
          {mockHistory.map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between px-5 py-4"
            >
              <div className="flex items-center gap-3">
                <span className="status-dot healthy" />
                <div>
                  <div className="font-medium text-black text-sm">{item.source}</div>
                  <div className="text-xs text-gray-500 font-mono">
                    {item.records} records
                  </div>
                </div>
              </div>
              <div className="text-xs text-gray-400 font-mono">
                {new Date(item.timestamp).toLocaleString('en-US', { 
                  hour12: false, 
                  month: 'short', 
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                }).toUpperCase()}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Data Freshness */}
      <div className="panel">
        <div className="panel-header">
          <h3 className="panel-title">DATA FRESHNESS</h3>
        </div>
        <div className="panel-body">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 border border-green-200 bg-green-50">
              <div className="text-xs uppercase tracking-wider text-green-600">PRODUCTION METERS</div>
              <div className="text-lg font-mono font-semibold text-green-700 mt-1">5 MIN AGO</div>
              <div className="text-xs font-mono text-gray-500 mt-2">Real-time via SCADA</div>
            </div>
            <div className="p-4 border border-amber-200 bg-amber-50">
              <div className="text-xs uppercase tracking-wider text-amber-600">CUSTOMER METERS</div>
              <div className="text-lg font-mono font-semibold text-amber-700 mt-1">MONTHLY</div>
              <div className="text-xs font-mono text-gray-500 mt-2">Due in 15 days</div>
            </div>
            <div className="p-4 border border-gray-200">
              <div className="text-xs uppercase tracking-wider text-gray-600">ENERGY DATA</div>
              <div className="text-lg font-mono font-semibold text-black mt-1">DAILY</div>
              <div className="text-xs font-mono text-gray-500 mt-2">Updated this morning</div>
            </div>
          </div>
        </div>
      </div>

      {/* Manual Entry Modal */}
      {showEntryForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div
            className="absolute inset-0 bg-black/20"
            onClick={() => setShowEntryForm(false)}
          />
          <div className="relative bg-white border border-gray-200 p-6 max-w-md w-full mx-4">
            <h3 className="text-sm uppercase tracking-wider text-gray-500 mb-4">
              MANUAL METER READING
            </h3>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-xs uppercase tracking-wider text-gray-500 mb-2">
                  METER ID
                </label>
                <input
                  {...register('meter_id', { required: true })}
                  type="text"
                  className="input"
                  placeholder="e.g., PROD-001"
                />
              </div>
              <div>
                <label className="block text-xs uppercase tracking-wider text-gray-500 mb-2">
                  READING VALUE
                </label>
                <input
                  {...register('reading_value', { required: true })}
                  type="number"
                  step="0.01"
                  className="input"
                  placeholder="e.g., 175250.00"
                />
              </div>
              <div>
                <label className="block text-xs uppercase tracking-wider text-gray-500 mb-2">
                  METER TYPE
                </label>
                <select {...register('reading_type')} className="input">
                  <option value="production">Production</option>
                  <option value="distribution">Distribution</option>
                  <option value="customer">Customer</option>
                </select>
              </div>
              <div>
                <label className="block text-xs uppercase tracking-wider text-gray-500 mb-2">
                  NOTES (OPTIONAL)
                </label>
                <textarea
                  {...register('notes')}
                  rows={2}
                  className="input"
                  placeholder="Additional notes..."
                />
              </div>
              <div className="flex gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowEntryForm(false)}
                  className="btn btn-secondary flex-1"
                >
                  CANCEL
                </button>
                <button type="submit" className="btn btn-primary flex-1">
                  SUBMIT
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
