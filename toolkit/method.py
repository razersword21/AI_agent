import logging
logging.basicConfig(level=logging.INFO)
import time
import json
import re
import copy
import torch

def chat_agent(model, tokenizer, user_input: str, history: list):
    logging.info(f"\nchat_agent 輸入:\n{user_input}\n歷史紀錄: {history}")

    system_history = copy.deepcopy(history)
    if (len(system_history) > 0):
        system_history.insert(0, {"role": "system", "content": "所有回應都必須用繁體中文回答，且思考鍊的內容盡量精簡。"})

    history.append({"role": "user", "content": user_input})
    system_history.append({"role": "user", "content": user_input})

    start_time = time.time()

    text = tokenizer.apply_chat_template(
        system_history,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    with torch.no_grad():
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=100
        )

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
    logging.info(f"\n=== 生成內容 ===\n{response}\n生成時間: {time.time()-start_time}")
    history.append({"role": "assistant", "content": response})
    return response, history

# debug 用
import sys
def print_colored(text, color, end='\n'):
    colors = {
        '紅色': '\x1b[31m',
        '綠色': '\x1b[32m',
        '黃色': '\x1b[33m',
        '藍色': '\x1b[34m',
        '紫色': '\x1b[35m',
        '青色': '\x1b[36m'
    }
    reset = '\x1b[0m'
    sys.stdout.write(colors.get(color, '') + text + reset + end)