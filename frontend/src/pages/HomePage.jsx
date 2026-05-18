import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchSubjects, startAssessment } from '../services/api'

// หน้าแรก — เลือกวิชา + พิมพ์คำถาม → เริ่ม assessment
export default function HomePage() {
  const navigate = useNavigate()
  const [subjects, setSubjects] = useState([])
  const [subjectId, setSubjectId] = useState('')
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  // โหลดรายชื่อวิชาตอน mount
  useEffect(() => {
    fetchSubjects()
      .then((data) => {
        setSubjects(data.subjects)
        if (data.subjects.length > 0) setSubjectId(data.subjects[0].id)
      })
      .catch((err) => setError(err.message))
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    if (!subjectId || !question.trim()) return
    setLoading(true)
    setError(null)
    try {
      const data = await startAssessment({ subject_id: subjectId, question })
      // ส่ง session + quiz ต่อไปยังหน้า AssessPage ผ่าน state
      navigate('/assess', { state: { session: data, subjectId, question } })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold text-gray-900 mb-3">
          เริ่มเรียนกับ AI Tutor
        </h1>
        <p className="text-gray-600">
          เลือกวิชาและพิมพ์คำถามที่ไม่เข้าใจ — AI จะประเมินระดับและสอนให้พอดีกับคุณ
        </p>
      </div>

      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 space-y-5"
      >
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            วิชา
          </label>
          <select
            value={subjectId}
            onChange={(e) => setSubjectId(e.target.value)}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
            disabled={subjects.length === 0}
          >
            {subjects.length === 0 && <option>กำลังโหลด...</option>}
            {subjects.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            คำถาม / หัวข้อที่อยากเรียน
          </label>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="เช่น อธิบาย A* search algorithm หน่อย"
            rows={4}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent resize-none"
          />
        </div>

        {error && (
          <div className="rounded-lg bg-red-50 border border-red-200 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="w-full bg-brand-600 hover:bg-brand-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-medium py-2.5 rounded-lg transition-colors"
        >
          {loading ? 'กำลังเริ่ม...' : 'เริ่มเรียน'}
        </button>
      </form>
    </div>
  )
}
