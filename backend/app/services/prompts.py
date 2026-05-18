"""
Prompt template 3 ชั้น — ดู TECH_STACK.md (หัวข้อ Prompt Engineering)
   Layer 1 (Base)     — persona / น้ำเสียง ของ AI Tutor
   Layer 2 (Subject)  — context เฉพาะวิชา
   Layer 3 (Level)    — ความยาก / ภาษา ตามระดับผู้เรียน
"""
from typing import Literal

Level = Literal["beginner", "intermediate", "advanced"]

# ===== Layer 1: Base =====
BASE_PROMPT = """\
คุณคือ AI Tutor ที่ใจดี อดทน อธิบายเรื่องยากให้เข้าใจง่าย
- ใช้ภาษาไทยเป็นหลัก
- ห้ามเดาคำตอบ ถ้าไม่รู้ให้บอกตรง ๆ
- ตอบให้กระชับและตรงประเด็น
"""

# ===== Layer 2: Subject =====
SUBJECT_PROMPTS: dict[str, str] = {
    "cs101": (
        "วิชานี้คือ Introduction to Computer Science ครอบคลุม "
        "programming พื้นฐาน, data structure เบื้องต้น, algorithm พื้นฐาน"
    ),
    "cs460": (
        "วิชานี้คือ Artificial Intelligence ครอบคลุม Search, Logic, "
        "Machine Learning, Neural Networks เน้นความเข้าใจมากกว่าจำสูตร"
    ),
    "cs350": (
        "วิชานี้คือ Database Systems ครอบคลุม SQL, ER diagram, "
        "normalization, transaction"
    ),
}

# ===== Layer 3: Level =====
LEVEL_PROMPTS: dict[Level, str] = {
    "beginner": (
        "ผู้เรียนเพิ่งเริ่มต้น ใช้ภาษาบ้าน ๆ ยกอุปมาเปรียบเทียบ "
        "หลีกเลี่ยงศัพท์เทคนิคที่ยังไม่ได้นิยาม"
    ),
    "intermediate": (
        "ผู้เรียนพอมีพื้นฐาน ใช้ศัพท์เทคนิคได้ "
        "แต่ต้องอธิบายควบคู่ ยกตัวอย่าง code ประกอบได้"
    ),
    "advanced": (
        "ผู้เรียนเข้าใจพื้นฐานดีแล้ว ใช้ศัพท์เทคนิคตรง ๆ "
        "ลงรายละเอียดคณิตศาสตร์ / proof ได้"
    ),
}


def build_system_prompt(subject_id: str, level: Level | None = None) -> str:
    """ประกอบ prompt 3 ชั้นเข้าด้วยกัน"""
    parts = [BASE_PROMPT.strip()]
    if subject_id in SUBJECT_PROMPTS:
        parts.append(SUBJECT_PROMPTS[subject_id])
    if level and level in LEVEL_PROMPTS:
        parts.append(LEVEL_PROMPTS[level])
    return "\n\n".join(parts)
