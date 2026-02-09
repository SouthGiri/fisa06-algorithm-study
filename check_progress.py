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
    params = {"since": since} # since부터 현재까지의 커밋을 가져옴
    headers = {"Authorization": f"token {os.environ.get('GH_TOKEN')}"}
    
    response = requests.get(url, params=params, headers=headers)
    return len(response.json()) if response.status_code == 200 else 0

def main():
    now = datetime.now()
    day_of_week = now.weekday() # 0:월, 6:일
    
    # [핵심 로직] 이번 주 월요일 오전 9시 계산
    # 실행 시점이 월요일(0)이면 7일 전이 아니라 '오늘'이 기준이 되도록 처리
    days_to_subtract = day_of_week if day_of_week != 0 else 7
    start_dt = (now - timedelta(days=days_to_subtract)).replace(hour=9, minute=0, second=0, microsecond=0)
    
    # 일요일 실행 시 월요일 09:00 ~ 일요일 09:00 (중간점검)
    # 월요일 실행 시 지난주 월요일 09:00 ~ 현재 월요일 09:00 (최종결과)
    since = start_dt.isoformat()
    
    title = "📢 [일요일 중간 점검]" if day_of_week == 6 else "🏁 [월요일 최종 결과]"
    report = f"*{title}*\n"
    report += f"📅 집계 시작: {start_dt.strftime('%m/%d %H:%M')} ~ 현재까지\n\n"
    
    for m in MEMBERS:
        count = get_commits_count(m['owner'], m['repo'], since)
        status = "✅ 달성" if count >= 5 else f"❌ 미달 ({count}/5)"
        report += f"• *{m['name']}*: {status}\n"

    # Slack 전송
    slack_url = os.environ.get('SLACK_WEBHOOK_URL')
    if slack_url:
        requests.post(slack_url, json={"text": report})
    
    print(report)

if __name__ == "__main__":
    main()