import requests
from bs4 import BeautifulSoup
import json

def get_keirin_data():
    # 例：松山競輪（場コード：71）の今日のデータを想定
    # ※実際にはKEIRIN.JPなどのURLを指定する
    url = "https://example.com/keirin/today" 
    
    # ここでネットからデータを取ってくる（スクレイピング）
    # 今はテスト用に、自動生成するロジックだけ書いておくね
    players = []
    for i in range(1, 10):
        players.append({
            "id": i,
            "s": 90.0 + i,  # ここに実際の競走得点が入る
            "n": f"選手 {i}" # ここに実際の名前が入る
        })
    
    # データをJSONファイルとして保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=2)
    
    print("data.jsonを更新しました！")

if __name__ == "__main__":
    get_keirin_data()
