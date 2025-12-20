from google import genai
import json
import time
import os

# --- 配置区 ---
API_KEY = "AIzaSyBYV-I0lwtK18nvOayTt3NyzGw9xLPaMj0"
client = genai.Client(api_key=API_KEY)

def parse_with_new_sdk(raw_text):
    prompt = f"请从标题中提取信息并只返回JSON: '{raw_text}'。格式:{{'artist':'', 'show_name':'', 'city':'', 'type':''}}"
    try:
        # 最新版 SDK 的调用方式
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        # 清理并提取文本
        clean_text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(clean_text)
    except Exception as e:
        print(f"解析出错: {e}")
        return None

def main():
    if not os.path.exists("titles.txt"):
        print("❌ 找不到 titles.txt")
        return

    with open("titles.txt", "r", encoding="utf-8") as f:
        titles = [line.strip() for line in f if line.strip()]

    results = []
    print(f"🤖 使用最新 SDK 开始解析 {len(titles)} 条数据...")

    for t in titles:
        print(f"处理中: {t[:20]}...")
        data = parse_with_new_sdk(t)
        if data:
            print(f"   ✅ 成功: {data['artist']}")
            results.append(data)
        time.sleep(2) # 避开频率限制

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("\n✨ 全部完成！results.json 已生成。")

if __name__ == "__main__":
    main()