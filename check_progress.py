import requests
import os
from datetime import datetime, timedelta

# 스터디원 정보
MEMBERS = [
    {"name": "yuchael", "owner": "yuchael", "repo": "baekjoon"},
    {"name": "Hayden-yoonji", "owner": "Hayden-yoonji", "repo": "coding_test"},
    {"name": "Seongeun-Jo", "owner": "Seongeun-Jo", "repo": "Baekjoon_Python"},
    {"name": "jjwoori", "owner": "jjwoori123-lang", "repo": "BaekjoonHub"},
    {"name": "chaeng16", "owner": "chaeng16", "repo": "algorithm"},
    {"name": "codml", "owner": "codml", "repo": "CodingTestForPythonAndSQL"},
    {"name": "SouthGiri", "owner": "SouthGiri", "repo": "Algorithm_Practice"}
]

def get_commits_count(owner, repo, since):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"since": since}
    headers = {"Authorization": f"token {os.environ.get('GH_TOKEN')}"}
    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return len(response.json())
    except:
        pass
    return 0

def main():
    now = datetime.now()
    day_of_week = now.weekday()
    
    # 집계 기준 시간 (가장 최근 지난 월요일 오전 9시)
    days_to_subtract = day_of_week if day_of_week != 0 else 7
    start_dt = (now - timedelta(days=days_to_subtract)).replace(hour=9, minute=0, second=0, microsecond=0)
    since = start_dt.isoformat()
    
    title = "📢 일요일 중간 점검" if day_of_week == 6 else "🏁 월요일 최종 결과"
    
    table_rows = ""
    for m in MEMBERS:
        count = get_commits_count(m['owner'], m['repo'], since)
        status = "✅ 달성" if count >= 5 else f"❌ 미달 ({count}/5)"
        table_rows += f"| {m['name']} | {count} | {status} |\n"

    # 리드미 전체 뼈대 덮어쓰기
    readme_template = f"""# 🚀 코딩테스트 스터디 현황

이 페이지는 매주 일요일/월요일 오전 9시(KST)에 자동으로 업데이트됩니다.

## 📊 진행 상황 ({title})
- **집계 기간**: {start_dt.strftime('%m/%d 09:00')} ~ **현재**: {now.strftime('%m/%d 09:00')}

| 이름 | 커밋 수 | 상태 |
| :--- | :---: | :---: |
{table_rows}
---
최근 업데이트: {now.strftime('%Y-%m-%d %H:%M:%S')} (KST)
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_template)
    print("SUCCESS: README.md generated.")

if __name__ == "__main__":
    main()