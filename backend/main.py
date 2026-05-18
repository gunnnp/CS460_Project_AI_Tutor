"""
FastAPI entry point — AI Tutor backend
ทุก endpoint อ้างอิงตาม API_CONTRACT.md
ตอนนี้ return mock data ก่อน เพื่อให้ frontend developer ทำงานคู่กันได้
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from app.models.schemas import (
    SubjectsResponse,
    AssessRequest,
    AssessResponse,
    AssessSubmitRequest,
    AssessSubmitResponse,
    ExplainRequest,
    ExplainResponse,
    ExerciseRequest,
    ExerciseResponse,
    ExerciseSubmitRequest,
    ExerciseSubmitResponse,
    ErrorResponse,
)

load_dotenv()

app = FastAPI(
    title="AI Tutor API",
    description="Backend สำหรับ AI Tutor (CS460 Project)",
    version="0.1.0",
)

# CORS — อนุญาตให้ frontend (Vite dev server) เรียก API ได้
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== Error handler — แปลงทุก HTTPException เป็น format ของ API_CONTRACT.md =====
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    code_map = {
        400: "VALIDATION_ERROR",
        404: "NOT_FOUND",
        429: "RATE_LIMIT",
        500: "INTERNAL_ERROR",
        502: "LLM_ERROR",
    }
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code_map.get(exc.status_code, "INTERNAL_ERROR"),
                "message": str(exc.detail),
                "details": None,
            }
        },
    )


# ===== Health check =====
@app.get("/")
async def root():
    return {"status": "ok", "service": "AI Tutor API", "version": "0.1.0"}


# ===== 1. GET /api/subjects =====
@app.get("/api/subjects", response_model=SubjectsResponse)
async def get_subjects():
    """ดึงรายชื่อวิชาที่รองรับ"""
    return {
        "subjects": [
            {
                "id": "cs101",
                "name": "Introduction to Computer Science",
                "description": "พื้นฐาน programming, data structure เบื้องต้น",
            },
            {
                "id": "cs460",
                "name": "Artificial Intelligence",
                "description": "Search, Logic, ML, Neural Networks",
            },
            {
                "id": "cs350",
                "name": "Database Systems",
                "description": "SQL, ER diagram, normalization, transaction",
            },
        ]
    }


# ===== 2. POST /api/assess =====
@app.post("/api/assess", response_model=AssessResponse)
async def create_assessment(body: AssessRequest):
    """สร้าง quiz ประเมินระดับ — ตอนนี้ return mock data"""
    # TODO: เรียก LLM ออก quiz จริง ตาม subject_id + question
    return {
        "session_id": "sess_mock_001",
        "quiz": [
            {
                "id": "q1",
                "question": "Search algorithm ใดที่ใช้ heuristic?",
                "choices": ["BFS", "DFS", "A*", "Random"],
                "type": "multiple_choice",
            },
            {
                "id": "q2",
                "question": "Heuristic ที่ admissible หมายถึงอะไร?",
                "choices": [
                    "ประเมินค่าจริงเกินไป",
                    "ไม่ประเมินค่าเกินจริง",
                    "ใช้ memory น้อย",
                    "เร็วที่สุด",
                ],
                "type": "multiple_choice",
            },
        ],
    }


# ===== 3. POST /api/assess/submit =====
@app.post("/api/assess/submit", response_model=AssessSubmitResponse)
async def submit_assessment(body: AssessSubmitRequest):
    """ส่งคำตอบ quiz → ระบบประเมินระดับ"""
    # TODO: ตรวจคำตอบจริง + ให้ LLM ประเมินระดับ
    return {
        "session_id": body.session_id,
        "level": "intermediate",
        "score": 2,
        "total": 2,
        "reasoning": "ตอบถูกทั้งสองข้อ แสดงว่าเข้าใจพื้นฐานแล้ว",
    }


# ===== 4. POST /api/explain =====
@app.post("/api/explain", response_model=ExplainResponse)
async def request_explanation(body: ExplainRequest):
    """ขอคำอธิบายตามระดับ"""
    # TODO: เรียก LLM ผ่าน Prompt 3 ชั้น (Base + Subject + Level)
    return {
        "session_id": body.session_id,
        "explanation": (
            "A* คือ search algorithm ที่ใช้ f(n) = g(n) + h(n) ..."
        ),
        "examples": [
            {
                "title": "หา route ที่สั้นที่สุด",
                "content": "สมมติแผนที่มี 5 จุด...",
            }
        ],
        "key_points": [
            "g(n) = cost จากจุดเริ่มต้นถึง n",
            "h(n) = heuristic estimate จาก n ถึง goal",
            "ต้องใช้ admissible heuristic จึง optimal",
        ],
    }


# ===== 5. POST /api/exercise =====
@app.post("/api/exercise", response_model=ExerciseResponse)
async def request_exercise(body: ExerciseRequest):
    """ขอแบบฝึกหัด 1 ข้อ"""
    # TODO: เรียก LLM สร้างแบบฝึกหัดตามระดับ
    return {
        "session_id": body.session_id,
        "exercise_id": "ex_mock_001",
        "question": (
            "ถ้า heuristic h(n) ประเมินค่าเกินจริง A* "
            "จะยังหา optimal path ได้ไหม? เพราะอะไร?"
        ),
        "type": "short_answer",
        "hint": "ลองคิดถึงนิยาม admissible heuristic",
    }


# ===== 6. POST /api/exercise/submit =====
@app.post("/api/exercise/submit", response_model=ExerciseSubmitResponse)
async def submit_exercise(body: ExerciseSubmitRequest):
    """ส่งคำตอบแบบฝึกหัด → ตรวจ + feedback + next_action"""
    # TODO: เรียก LLM ตรวจคำตอบ + ให้คะแนน + ตัดสินใจ pass/retry
    return {
        "session_id": body.session_id,
        "exercise_id": body.exercise_id,
        "correct": True,
        "score": 8,
        "max_score": 10,
        "feedback": "อธิบายเหตุผลได้ดี ครบถ้วน แต่ขาดตัวอย่างประกอบ",
        "next_action": "pass",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
