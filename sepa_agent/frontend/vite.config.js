import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// 👇 Replace this with your actual Codespaces backend URL
// You can find it in the PORTS tab (for port 8000)
const backendUrl = 'https://spooky-crematorium-4jprj6v6j7px35x9p-8000.app.github.dev'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy all API calls starting with /direct-debit to FastAPI backend
      '/direct-debit': {
        target: backendUrl,
        changeOrigin: true,
        secure: false,
      },
      // (optional) if you’ll have more APIs later:
      // '/api': { target: backendUrl, changeOrigin: true, secure: false },
    },
  },
})

