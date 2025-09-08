import requests

api_url = "http://127.0.0.1:8000/razer_api/v1/ai_agent/chat"
data = {
    "user_input": "生成一段用java寫數字list排序的程式碼",
    "history": []
}
response = requests.post(api_url, json=data)
print(response.json())