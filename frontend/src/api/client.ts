import axios from 'axios';
import { useAuthStore } from '../store/auth';

const API_BASE_URL = '/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API functions
export const api = {
  // Health
  health: () => apiClient.get('/health'),

  // NRW
  nrw: {
    getSummary: (periodDays = 30) =>
      apiClient.get(`/nrw/summary?period_days=${periodDays}`),
    calculateWaterBalance: (data: unknown) =>
      apiClient.post('/nrw/water-balance', data),
    analyzeMNF: (data: unknown) => apiClient.post('/nrw/mnf-analysis', data),
    analyzeLeakIndicators: (data: unknown) =>
      apiClient.post('/nrw/leak-indicators', data),
  },

  // Energy
  energy: {
    getSummary: (periodDays = 30) =>
      apiClient.get(`/energy/summary?period_days=${periodDays}`),
    getPumps: () => apiClient.get('/energy/pumps'),
    optimizeSchedule: (data: unknown) =>
      apiClient.post('/energy/optimize-schedule', data),
    analyzeEfficiency: (data: unknown) =>
      apiClient.post('/energy/efficiency-analysis', data),
  },

  // Compliance
  compliance: {
    getSummary: () => apiClient.get('/compliance/summary'),
    getObligations: (params?: Record<string, string>) =>
      apiClient.get('/compliance/obligations', { params }),
    createObligation: (data: unknown) =>
      apiClient.post('/compliance/obligations', data),
    updateObligation: (id: string, data: unknown) =>
      apiClient.patch(`/compliance/obligations/${id}`, data),
    getRiskAssessment: () => apiClient.post('/compliance/risk-assessment', {}),
    getReportTypes: () => apiClient.get('/compliance/reports/types'),
    generateReport: (data: unknown) =>
      apiClient.post('/compliance/reports/generate', data),
  },

  // Data Ingestion
  data: {
    getStatus: () => apiClient.get('/data/status'),
    getSources: () => apiClient.get('/data/sources'),
    submitReading: (data: unknown) =>
      apiClient.post('/data/manual-reading', data),
    submitBatch: (data: unknown) =>
      apiClient.post('/data/manual-readings/batch', data),
    getHistory: (limit = 20) =>
      apiClient.get(`/data/history?limit=${limit}`),
  },
};

