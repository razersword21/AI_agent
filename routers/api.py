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
import logging
logging.basicConfig(level=logging.INFO)


if __name__ == 'routers.api':
    TAG_MODEL_VERSION = 'v1'
    router = APIRouter(prefix='/v1/ai_agent', tags=[TAG_MODEL_VERSION])
    lock = Lock()
    EXECUTOR = concurrent.futures.ThreadPoolExecutor()
    load_dotenv()

    model_name = os.environ.get('MODEL_NAME')
    logging.info(f'model_name: {model_name}')
    # MODEL = AutoModelForCausalLM.from_pretrained(
    #     model_name,
    #     dtype="auto",
    #     device_map="auto"
    # ).eval()
    # logging.info(f'CUDA available: {torch.cuda.is_available()}')
    # logging.info(f'Model device: {MODEL.device}')
    # TOKENIZER = AutoTokenizer.from_pretrained(model_name, use_default_system_prompt=False)

# @router.post('/chat', responses={
#     200: {'model': Chat_response},
#     400: {'model': HTTPErrorResult},
#     500: {'model': HTTPErrorResult},
# })
# @catch_error
# async def chat_model_endp(request: Chat_request):
#     event_loop = get_event_loop()
#     async with lock:
#         generate_result, history = await event_loop.run_in_executor(None, chat_agent, MODEL, TOKENIZER, request.user_input, request.history)
#     return Chat_response(generate_text=generate_result, history=history)

@router.get('/test', responses={
    200: {'model': HTTPSuccessResult}
    })
@catch_error
async def test():
    logging.info('test endpoint called')
    return HTTPSuccessResult(message='test')