# 用python實作一個簡單的AI 聊天機器人api

## 使用方式 (port須設定兩邊相同)
- 前端使用vue 3 + vite
    - 需要安裝node.js
    - 使用npm install 安裝相關套件
    - 使用npm run dev 啟動
- 後端使用python + fastapi
    - 需要安裝python 3.10
    - 使用pip install -r requirements.txt 安裝相關套件
    - 使用uvicorn main:app --reload 啟動

## 功能
- 使用者輸入文字，AI回傳文字
- 目前使用的AI模型為deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B 較擅長數學及程式推理相關問題

# Podman
- build image
    ```bash
    podman build --pull=never -t testagent:latest . --log-level=debug
    ```
pull=never表示不會從docker hub下載image
- run container
    ```bash
    podman run --rm -e MODEL_NAME=Qwen/Qwen3-0.6B -p 8080:8080 testagent:latest
    ```

## Test
```bash
 curl http://localhost:8080/razer_api/v1/ai_agent/test
```