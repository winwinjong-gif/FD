---
title: "FD-03-200__sqlite-open"
date: 2026-09-09
id: FD-03-200
type: lecture
tags:
  - FD
  - Week03
  - sqlite
---

## 그 표들은 이미 한 파일 안에 있다

> [!info] 학습 목표
>
> - 제공된 SQLite DB를 파이썬에서 열고, 어떤 표가 들어 있는지 눈으로 확인한다.
> - 실행 환경(커널)이 올바른지 한 줄로 점검한다.

---

## 🧪 시작 전에 한 줄

본격적으로 들어가기 전에 확인할 게 딱 하나 있다. 이번 주 진짜 위험한 지점은 패키지를 설치했는지가 아니라 **VS Code가 어떤 파이썬을 쓰고 있는지**다. 커널을 잘못 고르면 `pandas`가 없다는 에러부터 만나게 된다.

**§200-1**
```python
# §FD-03-200-1
import sys
print(sys.executable)

# 예상 출력:
# (자기 프로젝트 경로)/FD_26/.venv/bin/python3
```

이 경로 끝이 `FD_26/.venv/bin/python3`로 찍히면 통과다. 다른 경로가 찍히면 VS Code 오른쪽 위(또는 커맨드 팔레트 "Python: Select Interpreter")에서 커널을 바꾼다. 이번 주 실행·패키지 추가는 전부 이 `FD_26` 프로젝트에서 한다 — 필요한 패키지가 있으면 여기서 `uv add`로 더한다.

아래 네 칸은 본격적으로 시작하기 전 자기 화면과 대조해볼 체크카드다.

<figure style="margin:16px 0; background:#FAF7F0; border:1px solid #E2E8F0; border-radius:8px; padding:14px;">
  <div style="display:grid; grid-template-columns:repeat(4, 1fr); gap:10px;">
    <div style="background:#fff; border:1px solid #CBD5E1; border-radius:8px; padding:10px; text-align:center;">
      <div style="font-size:11px; color:#64748B;">① 파이썬 위치</div>
      <div style="font-size:10.5px; font-family:monospace; color:#0F2747; margin-top:6px;">.../FD_26/.venv/bin/python3</div>
    </div>
    <div style="background:#fff; border:1px solid #CBD5E1; border-radius:8px; padding:10px; text-align:center;">
      <div style="font-size:11px; color:#64748B;">② pandas</div>
      <div style="font-size:10.5px; font-family:monospace; color:#0F2747; margin-top:6px;">import pandas → 에러 없음</div>
    </div>
    <div style="background:#fff; border:1px solid #CBD5E1; border-radius:8px; padding:10px; text-align:center;">
      <div style="font-size:11px; color:#64748B;">③ DB 파일</div>
      <div style="font-size:10.5px; font-family:monospace; color:#0F2747; margin-top:6px;">data/market_data.db 존재</div>
    </div>
    <div style="background:#fff; border:1px solid #CBD5E1; border-radius:8px; padding:10px; text-align:center;">
      <div style="font-size:11px; color:#64748B;">④ 첫 쿼리</div>
      <div style="font-size:10.5px; font-family:monospace; color:#0F2747; margin-top:6px;">3개 표 이름 출력</div>
    </div>
  </div>
</figure>
*네 칸 중 어느 하나라도 자기 화면과 다르게 나오면, 그 칸이 걸린 지점이다. 뒤로 갈수록 앞 칸이 통과했다는 전제 위에 있다.*

## 🔌 DB 파일을 연다

`sqlite3`는 파이썬을 설치할 때 이미 같이 들어 있다. 별도로 설치할 것도, 별도 서버를 띄울 것도 없다 — `import sqlite3` 한 줄이면 끝난다. 이 사실이 이번 주 내내 쓸 배경이다.

**§200-2**
```python
# §FD-03-200-2
import sqlite3

conn = sqlite3.connect('data/market_data.db')
```

`connect`에 파일 경로를 주면 그 파일을 연다. 만약 그 이름의 파일이 없었다면 이 자리에서 새로 만들어지는데, 오늘은 이미 만들어진 파일을 여는 것이다.

문법보다 먼저 확인할 것은 **이 안에 뭐가 들어 있는가**다.

파이썬과 DB를 잇는 핵심 다리가 바로 `pd.read_sql`이다 — SQL 질의 문자열을 DB에 던져 결과를 지난주(Week 02)에 익힌 pandas DataFrame으로 즉시 받아온다.

**§200-3**
```python
# §FD-03-200-3
import pandas as pd

pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)

# 예상 출력:
#          name
#     companies
#    financials
#       returns
```

세 개의 표가 보인다 — `companies`(기업 정보), `financials`(재무정보), `returns`(수익률). [[FD-03-100__why-database|100]]에서 말한 그 세 표가 실제로 이 파일 하나 안에 들어 있다.

**§200-4**
```python
# §FD-03-200-4
pd.read_sql("SELECT * FROM companies LIMIT 5", conn)

# 예상 출력:
#      code       name sector market
#    005930     삼성전자   전기전자  KOSPI
#    000660   SK하이닉스   전기전자  KOSPI
#    009150     삼성전기   전기전자  KOSPI
#    051910      LG화학     화학  KOSPI
#    011170    롯데케미칼     화학  KOSPI
```

`LIMIT 5`는 "결과 중 앞의 5행만 보여줘"라는 뜻이다. 표 전체를 다 보지 않아도 어떤 열이 있는지 감을 잡기에는 충분하다. `code` 열이 `'005930'`처럼 문자열로 저장돼 있는 것도 확인해둔다 — 숫자로 저장하면 앞의 0이 사라진다.

> [!warning] core는 노트북 경로
> - `.db` 파일을 VS Code 탐색기에서 그냥 더블클릭하면 사람이 읽을 수 없는 바이너리 화면이 열린다 — 여기서 막혀 당황하는 것이 가장 흔한 실수다.
> - **연결해서 여는 방법은 이 코드뿐이다** — `sqlite3.connect` + `pd.read_sql`.
> - 표로 훑어만 보고 싶으면 확장 프로그램도 있지만(아래 접힌 블록), 그건 참고용 보기 도구일 뿐 실습 어느 것도 거기에 의존하지 않는다.

## 🏗 파이썬 ↔ DB 왕복 티켓: 넣기(`to_sql`)와 꺼내기(`read_sql`)

파이썬과 데이터베이스를 오가는 길은 딱 두 가지뿐이다:

1. **꺼낼 때 (DB ➔ DataFrame)**: `pd.read_sql(query, conn)`
2. **넣을 때 (DataFrame ➔ DB)**: `df.to_sql('표이름', conn, if_exists='append')`

학생이 분석할 3개 표(`market_data.db`)는 이미 적재되어 있지만, 새로운 데이터를 내 DB에 누적할 때는 `to_sql`을 쓴다. 아래 예시는 실습 폴더에 제공된 교수 시연용 고정 CSV 한 장을 사용한다.

CSV의 `daily_return`은 Week02에서 이미 계산해 둔 값이다. 이번 시연에서는 수익률을 다시 계산하지 않고 `code`·`date`·`close`·`daily_return` 네 열을 함께 `append`한다. 이번 주에 확인할 것은 수익률 산식이 아니라 새 거래일을 DB에 누적하고 같은 거래일을 다시 넣지 않는 흐름이기 때문이다. 제공 CSV에서는 12개 종목의 새 종가가 직전 저장 종가 대비 상승·하락으로 섞여 있고, `daily_return`은 각 종목의 `round((close-prev_close)/prev_close, 6)` 계산값을 그대로 보존한다.

**§200-5**
```python
# §FD-03-200-5
# 새로 들어온 데이터를 내 DB 표에 덧붙여 적재하는 방법
returns_new = pd.read_csv('data/새로_들어온_거래일.csv')
loaded = pd.read_sql("SELECT code FROM returns WHERE date = ?", conn,
                     params=[returns_new["date"].iloc[0]])
if loaded.empty:
    returns_new.to_sql('returns', conn, if_exists='append', index=False)
    print(f"{len(returns_new)}행 적재 (daily_return 포함)")
else:
    print("이 거래일은 이미 적재됨 (daily_return도 중복 적재하지 않음)")
```

실제 실행에서는 첫 번째 실행에서 `12행 적재 (daily_return 포함)`, 같은 셀을 다시 실행하면 `이 거래일은 이미 적재됨 (daily_return도 중복 적재하지 않음)`이 출력된다. `daily_return`의 계산을 이 셀에 넣지 않은 것은 Week02의 결과를 이어 받아 저장하는 장면을 보여주고, Week03의 새 초점을 `append`와 중복 방지에 남겨두기 위해서다.

강의 시작 전 초기화가 필요하면 practice 폴더에서 `sqlite3 data/market_data.db "DELETE FROM returns WHERE date = '2026-06-25';"` 한 번 실행한다(이번 거래일의 `returns` 행만 지운다).

여기서 눈여겨볼 핵심 옵션은 `if_exists='append'`다:
- `append` (덧붙이기): 기존 데이터는 안전하게 보존하고, 새 행만 뒤에 착착 누적한다 — [[FD-03-100__why-database|100]]에서 배운 "한 번 쌓아두고 매일 새로 생긴 것만 덧붙인다"는 핀테크 아키텍처의 핵심 코드다.
- `replace` (덮어쓰기): 표 전체를 통째로 지우고 새로 만든다 — 표를 **처음 생성할 때 딱 한 번**만 쓰는 위험한 옵션이며, 평소에 쓰면 과거 10년 치 데이터가 0.1초 만에 날아간다.

> [!tip]- VS Code에서 표로 보기 (선택)
> 확장 프로그램을 설치하면 `.db` 파일을 표 형태로 열어볼 수 있다. 다만 이번 주 어느 실습도 이 방법에 의존하지 않는다 — 확장 이름과 macOS/Windows 설치 차이는 별도로 안내될 예정이다.

실습에서는 이 노트의 흐름을 그대로 반복한다 — 환경 진단 한 줄 → DB 연결 → 표 목록 확인 → `LIMIT 5`로 한 표 들여다보기.

---

## 🔖 핵심 요약

> [!summary] 🏆 이 노트를 마쳤다면?
>
> - [ ] `import sys; print(sys.executable)`로 자기 커널이 올바른지 확인할 수 있다.
> - [ ] `sqlite3.connect`로 제공된 DB 파일을 열 수 있다.
> - [ ] `sqlite_master`로 표 목록을 확인하고, `LIMIT`으로 한 표의 앞부분을 볼 수 있다.
> - [ ] `to_sql`의 `append`와 `replace`가 서로 다른 상황에서 쓰인다는 것을 설명할 수 있다.
> - [ ] 실습에서: 환경 진단 → DB 연결 → 표 목록 → `LIMIT 5` 순서를 직접 실행한다.
