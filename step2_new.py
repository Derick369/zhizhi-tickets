import os
import json
import requests
import re

def parse_titles():
    # 获取智谱 API Key
    api_key = os.getenv("ZHIPU_API_KEY")
    # 智谱的标准 API 调用地址
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    if not os.path.exists("titles.txt"):
        print("未找到 titles.txt")
        return
        
    with open("titles.txt", "r", encoding="utf-8") as f:
        all_titles = f.read()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "glm-4-flash", # 使用性价比最高的 flash 模型
        "messages": [
            {
                "role": "system", 
                "content": "你是一个演出数据专家。请将标题解析为 JSON 数组。只需返回 JSON 数组，严禁任何开头或说明文字。"
            },
            {
                "role": "user", 
                "content": f"字段：artist, show_name, city, type。标题如下：\n{all_titles}"
            }
        ],
        "temperature": 0.1 # 降低随机性，让格式更稳
    }

    print("🚀 智谱 AI 正在为您处理数据...")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        res_json = response.json()
        
        # 提取 AI 的文本内容
        content = res_json['choices'][0]['message']['content'].strip()
        
        # 清洗掉可能出现的 Markdown 标签
        clean_json = re.sub(r'```json|```', '', content).strip()
        final_data = json.loads(clean_json)
        
        with open("results.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
            
        print(f"✅ 自动化成功！已存入 {len(final_data)} 条最新演出。")

    except Exception as e:
        print(f"❌ 解析出错: {e}")
        if 'res_json' in locals(): print(f"API 返回原始数据: {res_json}")

if __name__ == "__main__":
    parse_titles()
