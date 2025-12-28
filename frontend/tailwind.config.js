/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Minimalist monochrome palette
        panel: {
          bg: '#ffffff',
          border: '#e0e0e0',
          hover: '#f5f5f5',
        },
        // Functional colors only - minimal
        status: {
          ok: '#22c55e',
          warn: '#f59e0b',
          error: '#ef4444',
        },
      },
      fontFamily: {
        mono: ['"IBM Plex Mono"', '"SF Mono"', 'Consolas', 'monospace'],
        sans: ['"IBM Plex Sans"', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'display': ['3.5rem', { lineHeight: '1', letterSpacing: '-0.02em' }],
        'data': ['1.75rem', { lineHeight: '1.2', letterSpacing: '-0.01em' }],
        'label': ['0.6875rem', { lineHeight: '1.4', letterSpacing: '0.05em' }],
      },
      borderRadius: {
        'none': '0',
        'sm': '2px',
        DEFAULT: '2px',
      },
      boxShadow: {
        'none': 'none',
      },
    },
  },
  plugins: [],
};
