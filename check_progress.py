import requests
import os
from datetime import datetime, timedelta

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
    response = requests.get(url, params=params, headers=headers)
    return len(response.json()) if response.status_code == 200 else 0

def main():
    now = datetime.now()
    day_of_week = now.weekday()
    
    days_to_subtract = day_of_week if day_of_week != 0 else 7
    start_dt = (now - timedelta(days=days_to_subtract)).replace(hour=9, minute=0, second=0, microsecond=0)
    since = start_dt.isoformat()
    
    title = "📢 일요일 중간 점검" if day_of_week == 6 else "🏁 월요일 최종 결과"
    
    # README에 기록할 내용 생성
    new_report = f"## 📊 스터디 진행 현황 ({title})\n"
    new_report += f"- **집계 시작**: {start_dt.strftime('%m/%d 09:00')} ~ **현재**: {now.strftime('%m/%d 09:00')}\n\n"
    new_report += "| 이름 | 커밋 수 | 상태 |\n| :--- | :---: | :---: |\n"
    
    for m in MEMBERS:
        count = get_commits_count(m['owner'], m['repo'], since)
        status = "✅ 달성" if count >= 5 else f"❌ 미달 ({count}/5)"
        new_report += f"| {m['name']} | {count} | {status} |\n"
    
    # README 업데이트 로직
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # 표시자(Placeholder)를 기준으로 내용 교체
    start_marker = ""
    end_marker = ""
    
    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[1]
        new_content = f"{before}{start_marker}\n\n{new_report}\n{end_marker}{after}"
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README updated successfully!")
    else:
        print("Error: Markers not found in README.md")

if __name__ == "__main__":
    main()