import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { MyRuntimeProvider } from './MyRuntimeProvider.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MyRuntimeProvider>
      <App />
    </MyRuntimeProvider>
  </StrictMode>,
)
