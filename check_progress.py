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
    
    day_of_week = now_kst.weekday() # 0:월, 6:일
    
    # 2. 집계 기준 시간 계산 (지난주 월요일 09:00:00)
    # 오늘이 월요일(0)이면 7일 전, 일요일(6)이면 6일 전
    days_to_subtract = day_of_week if day_of_week != 0 else 7
    start_dt = (now_kst - timedelta(days=days_to_subtract)).replace(hour=9, minute=0, second=0, microsecond=0)
    
    # API 요청을 위한 ISO 포맷 (UTC 기준으로 변환하여 전달하는 것이 가장 정확함)
    since = start_dt.astimezone(timezone.utc).replace(tzinfo=None).isoformat() + "Z"
    
    title = "📢 일요일 중간 점검" if day_of_week == 6 else "🏁 월요일 최종 결과"
    
    table_rows = ""
    for m in MEMBERS:
        count = get_commits_count(m['owner'], m['repo'], since)
        status = "✅ 달성" if count >= 5 else f"❌ 미달 ({count}/5)"
        table_rows += f"| {m['name']} | {count} | {status} |\n"

    # 3. 리드미 템플릿 생성 (한국 시간 표시)
    readme_template = f"""# 🚀 코딩테스트 스터디 현황

이 페이지는 매주 일요일/월요일 오전 9시(KST)에 자동으로 업데이트됩니다.

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
    print(f"SUCCESS: README.md generated at {now_kst}")

if __name__ == "__main__":
    main()