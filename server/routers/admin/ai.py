# default

# libraries
from fastapi import APIRouter
import google.generativeai as genai
from core.schemas.admin import (
    # params
    # payload
    PostAIPromtPayload,
    # responses
    # enums
    ResponseStatusEnum,
    AIPromtTypeEnum,
)
from core.conf import settings
# local

router = APIRouter(
    responses={404: {"description": "Not found"}},
)

genai.configure(api_key=settings.GEMINI_AI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


ai_prompt_data_map = {
    AIPromtTypeEnum.TITLE: "Viết lại title trên ngắn gọn chuẩn SEO trong 1 câu",
    AIPromtTypeEnum.DESCRIPTION: "Viết lại description trên ngắn gọn chuẩn SEO trong 1 đoạn văn",
    AIPromtTypeEnum.CONTENT: "Viết lại content trên ngắn gọn chuẩn SEO",
}


@router.post(
    "/ai/post_prompts",
    tags=["Admin-AI"],
    status_code=ResponseStatusEnum.ACCEPTED.value,
)
def ai_post_info_suggestion(payload: PostAIPromtPayload):
    response = model.generate_content(
        f"{payload.context}\n{ai_prompt_data_map[payload.prompt_type]}"
    )
    return {"data": response.text}
