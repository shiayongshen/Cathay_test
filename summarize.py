import os
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-05-01-preview"
)


def summarize_combined_text(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-global",  
            messages=[
                {"role": "system", "content": "你是一個專業的文本摘要助手。"},
                {"role": "user", "content": f"以下是多個文件的合併內容，請生成摘要：\n{text}"}
            ],
            max_tokens=2000, 
            temperature=1  
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"摘要時出錯：{e}")
        return None

def summarize_all_txt_files():
    current_folder = os.getcwd()  
    txt_files = [f for f in os.listdir(current_folder) if f.endswith('.txt')]
    
    combined_text = ""
    for file_name in txt_files:
        file_path = os.path.join(current_folder, file_name)
        
        try:
            # 讀取檔案內容並附加到 combined_text
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                combined_text += f"\n\n### 文件: {file_name} ###\n{content}"
        except Exception as e:
            print(f"讀取檔案 {file_name} 時出錯：{e}")
    
    # 呼叫摘要函式
    if combined_text.strip():
        summary = summarize_combined_text(combined_text)
        
        if summary:
            summary_file_path = os.path.join(current_folder, "summary.txt")
            try:
                with open(summary_file_path, "w", encoding="utf-8") as summary_file:
                    summary_file.write(summary)
                print(f"摘要已完成並存檔：{summary_file_path}")
            except Exception as e:
                print(f"寫入摘要檔案時出錯：{e}")
        else:
            print("無法生成摘要。")
    else:
        print("未找到有效的文本內容。")
if __name__ == "__main__":
    summarize_all_txt_files()