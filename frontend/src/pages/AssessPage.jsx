import { useLocation, useNavigate } from 'react-router-dom'

// หน้าทำ quiz ประเมินระดับ — placeholder ก่อน
// TODO: รับ session + quiz จาก state, render ฟอร์มเลือกตอบ, call /api/assess/submit, redirect ไป /learn
export default function AssessPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const session = location.state?.session

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <h1 className="text-2xl font-bold mb-4">ประเมินระดับ</h1>
      <div className="bg-white rounded-2xl border border-gray-200 p-6">
        <p className="text-gray-600 mb-4">
          หน้านี้จะ render quiz {session?.quiz?.length ?? 0} ข้อ
        </p>
        <pre className="bg-gray-50 rounded p-3 text-xs overflow-auto">
          {JSON.stringify(session, null, 2)}
        </pre>
        <button
          onClick={() => navigate('/learn', { state: { session, level: 'intermediate' } })}
          className="mt-4 bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 rounded-lg"
        >
          (จำลอง) ส่งคำตอบ → ไปหน้าเรียน
        </button>
      </div>
    </div>
  )
}
