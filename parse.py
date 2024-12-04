import requests
from bs4 import BeautifulSoup

# 目標網址
url = ["https://www.ithome.com.tw/news/152373",'https://www.ithome.com.tw/news/159391']
for i in url:
# 發送 HTTP 請求
    response = requests.get(i)
    if response.status_code == 200:
        # 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 提取標題，優先選擇 <h1 class="page-header">，然後是 <title>
        title = soup.find("h1", class_="page-header")
        if title:
            title_text = title.get_text(strip=True)
        else:
            title_text = soup.title.get_text(strip=True)
        
        # 替換不適合作為檔名的字元
        title_text = title_text.replace("/", "_").replace("\\", "_")
        
        # 找到內文的 div
        content_div = soup.find("div", class_="field field-name-body field-type-text-with-summary field-label-hidden")
        
        if content_div:
            # 提取內文
            paragraphs = content_div.find_all("p")  # 找到所有段落
            content = "\n".join(p.get_text(strip=True) for p in paragraphs)  # 合併所有段落文字
            
            # 將內容存成以標題命名的 txt 檔案
            file_path = f"{title_text}.txt"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            
            print(f"內文已成功存檔：{file_path}")
        else:
            print("未找到內文")
    else:
        print(f"無法訪問網站，狀態碼：{response.status_code}")
