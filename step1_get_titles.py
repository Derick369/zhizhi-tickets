import requests
from bs4 import BeautifulSoup
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_data_and_print():
    url = "https://whly.gd.gov.cn/audit_newspjggg/index.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    print("--- 正在抓取，请稍候 ---")
    session = requests.Session()
    session.trust_env = False
    
    try:
        resp = session.get(url, headers=headers, verify=False, timeout=15)
        resp.encoding = resp.apparent_encoding
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.find_all("a", title=True)

        print("\n👇 请复制下方虚线内的内容并发送给我：")
        print("-" * 30)
        
        count = 0
        with open("titles.txt", "w", encoding="utf-8") as f:
            for a in items:
                title = a['title'].strip()
                if "演出" in title or "演唱会" in title:
                    print(title) # 这一行会在屏幕上显示
                    f.write(title + "\n")
                    count += 1
        
        print("-" * 30)
        print(f"\n抓取完成！总计 {count} 条。")
        print(f"当前文件夹路径: {os.getcwd()}") # 告诉你文件到底存哪了

    except Exception as e:
        print(f"❌ 出错了: {e}")

if __name__ == "__main__":
    get_data_and_print()