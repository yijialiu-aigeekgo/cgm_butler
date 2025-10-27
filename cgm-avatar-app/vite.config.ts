import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
  },
  define: {
    'import.meta.env.VITE_TAVUS_API_KEY': JSON.stringify(process.env.VITE_TAVUS_API_KEY || '2baf6b72f7dc4c728132e63193c1dac7'),
    'import.meta.env.VITE_REPLICA_ID': JSON.stringify(process.env.VITE_REPLICA_ID || 'rfe12d8b9597'),
    'import.meta.env.VITE_PERSONA_ID': JSON.stringify(process.env.VITE_PERSONA_ID || 'p4e7a065501a'),
    'import.meta.env.VITE_BACKEND_URL': JSON.stringify(process.env.VITE_BACKEND_URL || 'http://localhost:5000'),
  },
})
