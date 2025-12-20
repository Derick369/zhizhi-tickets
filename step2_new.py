import os
import json
import re
from google import genai

def parse_titles():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("未找到 API Key")
        return
        
    client = genai.Client(api_key=api_key)
    
    if not os.path.exists("titles.txt"):
        print("未找到 titles.txt")
        return
        
    with open("titles.txt", "r", encoding="utf-8") as f:
        all_titles = f.read()

    prompt = f"""
    你是一个演出数据转换器。请将下列标题转换为 JSON 数组。
    要求：
    1. 字段：artist, show_name, city, type
    2. 只输出 JSON 数组本身，严禁任何开头语或结尾说明。
    
    标题列表：
    {all_titles}
    """

    print("🚀 正在向 AI 发起请求...")
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt
        )
        
        raw_text = response.text.strip()
        
        # 核心修复：用正则提取被 [ ] 包裹的部分，防止 AI 多嘴
        json_match = re.search(r'\[.*\]', raw_text, re.DOTALL)
        if json_match:
            clean_json = json_match.group(0)
            final_data = json.loads(clean_json)
        else:
            # 备选方案：尝试去掉 Markdown 标签
            clean_json = raw_text.replace("```json", "").replace("```", "").strip()
            final_data = json.loads(clean_json)
        
        with open("results.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ 自动化解析成功！共存入 {len(final_data)} 条情报。")

    except Exception as e:
        print(f"❌ 解析严重出错: {e}")
        # 如果彻底失败，保留一个空数组，防止网页报错
        with open("results.json", "w", encoding="utf-8") as f:
            json.dump([], f)

if __name__ == "__main__":
    parse_titles()
