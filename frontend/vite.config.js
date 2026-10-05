import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// In development, /api calls are proxied to the local FastAPI server, so the
// frontend always talks to a relative /api path (same as behind Nginx in production).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://127.0.0.1:8000',
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: { charts: ['recharts'] },
      },
    },
  },
})
