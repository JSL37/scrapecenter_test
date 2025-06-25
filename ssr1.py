import feapder
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime


class ScrapeCenterSpider(feapder.AirSpider):
    all_results = []
    current_id = 1  # 自增ID计数器

    def start_requests(self):
        os.makedirs("./scrape_out/ssr1", exist_ok=True)
        for page in range(1, 12):
            url = f"https://ssr1.scrape.center/page/{page}"
            yield feapder.Request(url, callback=self.parse)

    def parse(self, request, response):
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="el-card item m-t is-hover-shadow")

        for card in cards:
            self.all_results.append({
                "id": self.current_id,  # 添加自增ID
                "title": card.find("h2", class_="m-b-sm").text.strip(),
                "score": card.find("p", class_="score").text.strip(),
                "categories": [tag.text.strip() for tag in card.find_all("span", class_="category")],
                "cover": card.find("img", class_="cover")["src"]
            })
            self.current_id += 1  # ID递增

    def end_callback(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"./scrape_out/ssr1/{timestamp}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.all_results, f, ensure_ascii=False, indent=2)

        print(f"已爬取 {len(self.all_results)} 条数据，保存至：{output_path}")


if __name__ == "__main__":
    ScrapeCenterSpider().start()
