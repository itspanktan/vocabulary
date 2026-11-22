import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Overridable so the Docker Compose frontend container can reach the backend
// container by service name instead of localhost.
const apiProxyTarget = process.env.VITE_API_PROXY_TARGET || 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    proxy: {
      // Backend routes live at /words, not /api/words -- strip the prefix.
      '/api': {
        target: apiProxyTarget,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
  },
})
