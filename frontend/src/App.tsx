import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/auth';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import NRWPage from './pages/NRWPage';
import EnergyPage from './pages/EnergyPage';
import CompliancePage from './pages/CompliancePage';
import DataPage from './pages/DataPage';
import LoginPage from './pages/LoginPage';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<Dashboard />} />
        <Route path="nrw" element={<NRWPage />} />
        <Route path="energy" element={<EnergyPage />} />
        <Route path="compliance" element={<CompliancePage />} />
        <Route path="data" element={<DataPage />} />
      </Route>
    </Routes>
  );
}

export default App;

