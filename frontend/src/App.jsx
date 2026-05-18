import { Routes, Route, Link } from 'react-router-dom'
import HomePage from './pages/HomePage'
import AssessPage from './pages/AssessPage'
import LearnPage from './pages/LearnPage'
import ExercisePage from './pages/ExercisePage'

// Layout หลักของแอป — มี header + nav + content ด้านล่าง
function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="text-xl font-semibold text-brand-700">
            AI Tutor
          </Link>
          <nav className="text-sm text-gray-600">
            <span className="hidden sm:inline">CS460 — Artificial Intelligence</span>
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/assess" element={<AssessPage />} />
          <Route path="/learn" element={<LearnPage />} />
          <Route path="/exercise" element={<ExercisePage />} />
        </Routes>
      </main>

      <footer className="border-t border-gray-200 bg-white">
        <div className="max-w-5xl mx-auto px-6 py-3 text-xs text-gray-500 text-center">
          CS460 Project — มหาวิทยาลัยกรุงเทพ
        </div>
      </footer>
    </div>
  )
}

export default App
