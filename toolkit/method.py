import logging
logging.basicConfig(level=logging.INFO)
import time
import json
import re

def chat_agent(model, tokenizer, user_input: str, history: list):
    logging.info(f"\nchat_agent 輸入:\n{user_input}\n歷史紀錄: {history}")

    history.append({"role": "user", "content": user_input})
    
    start_time = time.time()

    text = tokenizer.apply_chat_template(
        history,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=1024
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    logging.info(f"\n生成:\n{response}\n生成時間: {time.time()-start_time}")
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