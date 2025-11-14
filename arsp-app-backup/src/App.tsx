import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ProtectedRoute } from './components/ProtectedRoute'
import { DashboardLayout } from './components/DashboardLayout'
import { ConsentDialog } from './components/ConsentDialog'
import { Dashboard } from './pages/Dashboard'
import { Topics } from './pages/Topics'
import { Literature } from './pages/Literature'
import { Plagiarism } from './pages/Plagiarism'
import { Journals } from './pages/Journals'

function App() {
  return (
    <BrowserRouter>
      <ProtectedRoute>
        <ConsentDialog />
        <DashboardLayout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/topics" element={<Topics />} />
            <Route path="/literature" element={<Literature />} />
            <Route path="/plagiarism" element={<Plagiarism />} />
            <Route path="/journals" element={<Journals />} />
          </Routes>
        </DashboardLayout>
      </ProtectedRoute>
    </BrowserRouter>
  )
}

export default App
