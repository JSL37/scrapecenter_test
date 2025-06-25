import requests
import time

def fetch_news(page=0, limit=50):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Referer": "https://spa4.scrape.center/"
    }
    url = "https://spa4.scrape.center/api/news/"
    params = {
        "limit": str(limit),
        "offset": str(page * limit)
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except Exception as e:
        print(f"获取第 {page + 1} 页数据时出错：{str(e)}")
        return None

def main():
    page = 0
    limit = 500
    total_items = 0
    
    while True:
        print(f"\n正在获取第 {page + 1} 页数据...")
        data = fetch_news(page, limit)
        
        if not data:
            break
            
        results = data.get("results", [])
        total_count = data.get("count", 0)
        
        # 如果这一页的数据少于50条，说明是最后一页
        if len(results) < limit:
            print(f"已到达最后一页，本页共 {len(results)} 条数据")
        
        # 打印当前页的数据
        for item in results:
            title = item.get("title", "")
            link = item.get("url", "")
            print(f"第{total_items}条数据：标题：{title}\n链接：{link}\n")
            total_items += 1
        
        # 判断是否继续获取下一页
        if len(results) < limit:
            break
            
        page += 1
        # 添加适当的延迟，避免请求过快
        time.sleep(1)
    
    print(f"\n数据获取完成！")
    print(f"总页数：{page + 1}")
    print(f"总数据条数：{total_items}")
    print(f"API返回的总数据量：{total_count}")

if __name__ == "__main__":
    main()

# print(response.text)
# print(response)