import os
from fastapi import APIRouter, Response, status, Request, HTTPException
from asyncio import get_event_loop, Lock
import concurrent.futures
from toolkit.lib import *
from toolkit.method import *
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re
from dotenv import load_dotenv

if __name__ == 'routers.api':
    TAG_MODEL_VERSION = 'v1'
    router = APIRouter(prefix='/v1/ai_agent', tags=[TAG_MODEL_VERSION])
    lock = Lock()
    EXECUTOR = concurrent.futures.ThreadPoolExecutor()
    load_dotenv()

    model_name = os.environ.get('MODEL_NAME')
    print(model_name)
    MODEL = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    ).eval()
    print(torch.cuda.is_available())
    print(MODEL.device)
    TOKENIZER = AutoTokenizer.from_pretrained(model_name, use_default_system_prompt=False)
    SYSTEM_PROMPT = """<人物資訊>{person_information}</人物資訊>你是一位人物角色，人物背景資料參考"人物資訊"，根據該人物的"人物資訊"決定所有想法、行為和講話方式。"""

@router.post('/chat', responses={
    200: {'model': Chat_response},
    400: {'model': HTTPErrorResult},
    500: {'model': HTTPErrorResult},
})
@catch_error
async def chat_model_endp(request: Chat_request):
    event_loop = get_event_loop()
    async with lock:
        generate_result, history = await event_loop.run_in_executor(None, chat_agent, MODEL, TOKENIZER, request.user_input, request.history)
    return Chat_response(generate_text=generate_result, history=history)