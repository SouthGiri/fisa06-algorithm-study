import requests
import os
from datetime import datetime, timedelta, timezone

# 스터디원 정보
MEMBERS = [
    {"name": "유채린", "owner": "yuchael", "repo": "baekjoon"},
    {"name": "채윤지", "owner": "Hayden-yoonji", "repo": "coding_test"},
    {"name": "조성은", "owner": "Seongeun-Jo", "repo": "Baekjoon_Python"},
    {"name": "전진우", "owner": "jjwoori123-lang", "repo": "BaekjoonHub"},
    {"name": "민채영", "owner": "chaeng16", "repo": "algorithm"},
    {"name": "김태완", "owner": "codml", "repo": "CodingTestForPythonAndSQL"},
    {"name": "이남길", "owner": "SouthGiri", "repo": "Algorithm_Practice"}
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
    # 1. 한국 시간(KST) 설정
    kst = timezone(timedelta(hours=9))
    now_kst = datetime.now(timezone.utc).astimezone(kst)
    
    day_of_week = now_kst.weekday() # 0:월, 1:화, ..., 6:일
    
    # 2. [집계 기준] 이번 주 월요일 오전 9시 계산
    # 오늘이 월요일(0) 오전 9시 이후라면 오늘 09:00이 기준, 
    # 그 외에는 지난 월요일 09:00이 기준이 되도록 설정
    # (매일 9시 정각 실행 기준, '지난 월요일 09:00'부터의 누적치를 보여줌)
    days_to_subtract = day_of_week if day_of_week != 0 else 7
    start_dt = (now_kst - timedelta(days=days_to_subtract)).replace(hour=9, minute=0, second=0, microsecond=0)
    
    # API 요청용 ISO 포맷 (UTC 00:00Z로 변환하여 누락 방지)
    since = start_dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # 제목 결정
    if day_of_week == 0: title = "🏁 월요일 최종 결과 (및 새 주 시작)"
    elif day_of_week == 6: title = "📢 일요일 중간 점검"
    else: title = f"📅 {now_kst.strftime('%A')} 현황 점검"

    table_rows = ""
    for m in MEMBERS:
        count = get_commits_count(m['owner'], m['repo'], since)
        status = "✅ 달성" if count >= 5 else f"❌ 미달 ({count}/5)"
        repo_url = f"https://github.com/{m['owner']}/{m['repo']}"
        name_link = f"[{m['name']}]({repo_url})"
        table_rows += f"| {name_link} | {count} | {status} |\n"

    # 3. README 생성
    readme_template = f"""# 🚀 코딩테스트 스터디 현황

이 페이지는 매일 오전 9시(KST)에 자동으로 업데이트됩니다.

## 📊 진행 상황 ({title})
- **집계 기간**: {start_dt.strftime('%m/%d 09:00')} ~ **현재**: {now_kst.strftime('%m/%d 09:00')}

| 이름 | 커밋 수 | 상태 |
| :--- | :---: | :---: |
{table_rows}
---
최근 업데이트: {now_kst.strftime('%Y-%m-%d %H:%M:%S')} (KST)
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_template)
    print(f"SUCCESS: Daily README.md generated at {now_kst}")

if __name__ == "__main__":
    main()