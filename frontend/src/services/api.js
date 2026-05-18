import axios from 'axios'
import * as mock from './mockData'

// ถ้า backend ยังไม่เสร็จ ตั้ง VITE_USE_MOCK=true ใน .env เพื่อใช้ mock data
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

// แปลง error จาก backend (ตาม API_CONTRACT.md) ให้เป็น Error object เดียวกัน
client.interceptors.response.use(
  (res) => res,
  (err) => {
    const data = err.response?.data
    const message =
      data?.error?.message ??
      err.message ??
      'เกิดข้อผิดพลาดที่ไม่ทราบสาเหตุ'
    return Promise.reject(new Error(message))
  }
)

// ===== Endpoints ตาม API_CONTRACT.md =====

export async function fetchSubjects() {
  if (USE_MOCK) return mock.subjects
  const { data } = await client.get('/api/subjects')
  return data
}

export async function startAssessment({ subject_id, question }) {
  if (USE_MOCK) return mock.assessmentSession
  const { data } = await client.post('/api/assess', { subject_id, question })
  return data
}

export async function submitAssessment({ session_id, answers }) {
  if (USE_MOCK) return mock.assessmentResult
  const { data } = await client.post('/api/assess/submit', { session_id, answers })
  return data
}

export async function requestExplanation({ session_id, level }) {
  if (USE_MOCK) return mock.explanation
  const { data } = await client.post('/api/explain', { session_id, level })
  return data
}

export async function requestExercise({ session_id, level }) {
  if (USE_MOCK) return mock.exercise
  const { data } = await client.post('/api/exercise', { session_id, level })
  return data
}

export async function submitExercise({ session_id, exercise_id, answer }) {
  if (USE_MOCK) return mock.exerciseResult
  const { data } = await client.post('/api/exercise/submit', {
    session_id,
    exercise_id,
    answer,
  })
  return data
}
