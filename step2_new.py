import os
import json
import time
from google import genai

def parse_titles():
    # 从 GitHub Secrets 获取 API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("错误: 未找到 API_KEY")
        return

    # 初始化客户端，明确指定使用 gemini-1.5-flash
    client = genai.Client(api_key=api_key)
    
    # 读取 step1 生成的标题
    if not os.path.exists("titles.txt"):
        print("错误: titles.txt 不存在")
        return
        
    with open("titles.txt", "r", encoding="utf-8") as f:
        titles = f.readlines()

    results = []
    
    prompt_template = """
    你是一个专业的演出数据分析师。请从下方的政务公告标题中提取信息，返回 JSON 格式。
    格式要求：[{"artist": "艺人名", "show_name": "演出名称", "city": "城市", "type": "演唱会/音乐会/音乐节/戏剧/舞蹈"}]
    
    标题："{title}"
    """

    for title in titles:
        title = title.strip()
        if not title: continue
        
        print(f"正在解析: {title[:20]}...")
        try:
            # 使用最稳妥的 generateContent 方式
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt_template.format(title=title)
            )
            
            # 提取 JSON 文本
            raw_text = response.text.strip()
            # 去掉 AI 可能返回的 ```json 标签
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(raw_text)
            if isinstance(data, list):
                results.extend(data)
            else:
                results.append(data)
                
            time.sleep(1) # 避免触发频率限制
            
        except Exception as e:
            print(f"解析出错: {e}")

    # 保存结果
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"解析完成，成功存入 {len(results)} 条数据。")

if __name__ == "__main__":
    parse_titles()
