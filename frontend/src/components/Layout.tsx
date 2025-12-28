import { useState } from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAuthStore } from '../store/auth';
import clsx from 'clsx';

const navigation = [
  { name: 'DASHBOARD', href: '/', code: '01' },
  { name: 'NRW', href: '/nrw', code: '02' },
  { name: 'ENERGY', href: '/energy', code: '03' },
  { name: 'COMPLIANCE', href: '/compliance', code: '04' },
  { name: 'DATA', href: '/data', code: '05' },
];

export default function Layout() {
  const location = useLocation();
  const { user, logout } = useAuthStore();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const currentTime = new Date().toLocaleTimeString('en-US', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });

  return (
    <div className="min-h-screen bg-white">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={clsx(
          'fixed inset-y-0 left-0 z-50 w-56 bg-white border-r border-gray-200 transform transition-transform duration-200 lg:translate-x-0',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {/* Logo */}
        <div className="h-14 flex items-center px-5 border-b border-gray-200">
          <span className="font-mono text-sm font-semibold tracking-tight">RWA</span>
          <span className="ml-2 text-xs text-gray-400 font-mono">v2.0</span>
          <button
            className="ml-auto lg:hidden text-gray-400 hover:text-black"
            onClick={() => setSidebarOpen(false)}
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Navigation */}
        <nav className="py-4">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                onClick={() => setSidebarOpen(false)}
                className={clsx(
                  'flex items-center gap-3 px-5 py-2.5 text-xs font-medium transition-colors',
                  isActive
                    ? 'bg-black text-white'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-black'
                )}
              >
                <span className="font-mono text-gray-400 w-5">{item.code}</span>
                <span className="tracking-wider">{item.name}</span>
              </Link>
            );
          })}
        </nav>

        {/* User section */}
        <div className="absolute bottom-0 left-0 right-0 border-t border-gray-200 p-4">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gray-100 flex items-center justify-center text-xs font-mono font-medium text-gray-600">
              {user?.name?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-black truncate">
                {user?.name || 'Operator'}
              </p>
              <p className="text-xs text-gray-400 font-mono truncate">
                {user?.role || 'admin'}
              </p>
            </div>
            <button
              onClick={logout}
              className="p-1.5 text-gray-400 hover:text-black transition-colors"
              title="Logout"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="lg:pl-56">
        {/* Top bar */}
        <header className="sticky top-0 z-30 bg-white border-b border-gray-200">
          <div className="flex items-center gap-4 px-5 h-14">
            <button
              className="lg:hidden p-1.5 -ml-1.5 text-gray-400 hover:text-black"
              onClick={() => setSidebarOpen(true)}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            
            <div className="flex-1">
              <span className="text-xs text-gray-400 uppercase tracking-widest">
                {navigation.find((n) => n.href === location.pathname)?.name || 'DASHBOARD'}
              </span>
            </div>

            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <span className="status-dot healthy" />
                <span className="text-xs font-mono text-gray-500">ONLINE</span>
              </div>
              <div className="h-4 w-px bg-gray-200" />
              <span className="text-xs font-mono text-gray-400 tabular-nums">
                {currentTime}
              </span>
            </div>
          </div>
        </header>

        {/* Page content */}
        <main className="p-5 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
