import { useLocation, useNavigate } from 'react-router-dom'

// หน้าอ่านคำอธิบายตามระดับ — placeholder ก่อน
// TODO: call /api/explain ตอน mount, render explanation + examples + key_points, ปุ่มไปหน้าแบบฝึกหัด
export default function LearnPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const { session, level } = location.state ?? {}

  return (
    <div className="max-w-2xl mx-auto px-6 py-12">
      <h1 className="text-2xl font-bold mb-4">เรียนรู้ ({level ?? 'unknown'})</h1>
      <div className="bg-white rounded-2xl border border-gray-200 p-6">
        <p className="text-gray-600 mb-4">หน้านี้จะแสดงคำอธิบายจาก AI ตามระดับ</p>
        <button
          onClick={() => navigate('/exercise', { state: { session, level } })}
          className="mt-4 bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 rounded-lg"
        >
          ทำแบบฝึกหัด
        </button>
      </div>
    </div>
  )
}
