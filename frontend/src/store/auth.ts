import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  setTokens: (accessToken: string) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,

      login: async (email: string, _password: string) => {
        // Mock login - replace with actual API call
        // In production: const response = await api.post('/auth/login', { email, password });

        // Simulate API delay
        await new Promise((resolve) => setTimeout(resolve, 500));

        // Mock successful login
        const mockUser: User = {
          id: '1',
          email: email,
          name: 'Water Operator',
          role: 'operator',
        };

        const mockToken = 'mock-jwt-token-' + Date.now();

        set({
          user: mockUser,
          accessToken: mockToken,
          isAuthenticated: true,
        });
      },

      logout: () => {
        set({
          user: null,
          accessToken: null,
          isAuthenticated: false,
        });
      },

      setTokens: (accessToken: string) => {
        set({ accessToken, isAuthenticated: true });
      },
    }),
    {
      name: 'rwa-auth',
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

