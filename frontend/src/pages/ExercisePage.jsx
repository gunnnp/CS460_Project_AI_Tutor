import { useLocation, useNavigate } from 'react-router-dom'

// หน้าทำแบบฝึกหัด + รับ feedback — placeholder ก่อน
// TODO: call /api/exercise, render question, รับคำตอบ, call /api/exercise/submit
// ตาม next_action: "pass" → กลับหน้าแรก, "retry" → /assess
export default function ExercisePage() {
  const location = useLocation()
  const navigate = useNavigate()
  const { session, level } = location.state ?? {}

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <h1 className="text-2xl font-bold mb-4">แบบฝึกหัด ({level ?? 'unknown'})</h1>
      <div className="bg-white rounded-2xl border border-gray-200 p-6">
        <p className="text-gray-600 mb-4">หน้านี้จะแสดงโจทย์ + ช่องตอบ + ผลตรวจ</p>
        <div className="flex gap-2">
          <button
            onClick={() => navigate('/')}
            className="bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 rounded-lg"
          >
            (จำลอง) ผ่าน → กลับหน้าแรก
          </button>
          <button
            onClick={() => navigate('/assess', { state: { session } })}
            className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-lg"
          >
            (จำลอง) ไม่ผ่าน → ประเมินใหม่
          </button>
        </div>
      </div>
    </div>
  )
}
