import { describe, it, expect, vi } from 'vitest';

// Mock the auth store for testing
vi.mock('./store/auth', () => ({
  useAuthStore: vi.fn((selector) => {
    const state = { isAuthenticated: false, user: null, login: vi.fn(), logout: vi.fn() };
    return selector ? selector(state) : state;
  }),
}));

describe('App', () => {
  it('should be importable', async () => {
    // Basic smoke test - ensure App can be imported without errors
    const AppModule = await import('./App');
    expect(AppModule.default).toBeDefined();
  });

  it('should export a function component', async () => {
    const AppModule = await import('./App');
    expect(typeof AppModule.default).toBe('function');
  });
});

describe('Environment', () => {
  it('should run in test environment', () => {
    expect(import.meta.env.MODE).toBe('test');
  });
});
