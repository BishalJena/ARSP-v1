import { useState } from 'react'
import type { ReactNode } from 'react'
import { Header } from './layout/Header'
import { Sidebar } from './layout/Sidebar'
import { Footer } from './layout/Footer'

export function DashboardLayout({ children }: { children: ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
      
      <div className="flex flex-1">
        <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        
        <main className="flex-1 container mx-auto px-4 py-8 md:ml-0">
          {children}
        </main>
      </div>
      
      <Footer />
    </div>
  )
}
