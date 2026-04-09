import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime

def get_keirin_data():
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"}
    today = datetime.now().strftime("%Y%m%d")
    master_data = {}

    try:
        # 1. 開催場リストを取得
        base_url = f"https://keirin.netkeiba.com/db/program/?date={today}"
        res = requests.get(base_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, "html.parser")
        
        # 開催場を探す
        stadium_links = soup.select(".RaceList_DataList li a")
        
        if not stadium_links:
            # 開催が見つからない場合のテスト用
            master_data["開催なし(テスト)"] = {str(r): [{"id": i, "s": 90.0, "n": f"テスト選手{i}"} for i in range(1, 10)] for r in range(1, 13)}
        else:
            for link in stadium_links:
                name = link.text.strip().replace(" ", "").replace("\n", "")
                href = link.get("href")
                bankid = re.search(r"bankid=(\d+)", href).group(1)
                
                print(f"【{name}】を取得中...")
                stadium_races = {}
                
                # とりあえず1R〜12Rまで回す
                for r in range(1, 13):
                    race_url = f"https://keirin.netkeiba.com/db/shusso/?bankid={bankid}&race_no={r}"
                    r_res = requests.get(race_url, headers=headers, timeout=10)
                    r_soup = BeautifulSoup(r_res.content, "html.parser")
                    
                    players = []
                    rows = r_soup.select(".PlayerList_Row")
                    for idx, row in enumerate(rows, 1):
                        p_name_tag = row.select_one(".PlayerName")
                        p_score_tag = row.select_one(".Score")
                        
                        if p_name_tag:
                            name_text = p_name_tag.text.strip()
                            score_val = 0.0
                            if p_score_tag:
                                score_match = re.search(r"\d+\.\d+", p_score_tag.text)
                                if score_match:
                                    score_val = float(score_match.group())
                            
                            players.append({"id": idx, "s": score_val, "n": name_text})
                    
                    if players:
                        stadium_races[str(r)] = players
                    time.sleep(0.2) # 少しだけ待機
                
                master_data[name] = stadium_races

    except Exception as e:
        print(f"エラーが発生したよ: {e}")
        # エラー時のバックアップデータ
        master_data["エラー復旧中"] = {str(r): [{"id": i, "s": 0.0, "n": "再読み込みしてね"} for i in range(1, 10)] for r in range(1, 13)}

    # 保存
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_keirin_data()
