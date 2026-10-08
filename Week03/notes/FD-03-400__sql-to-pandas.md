---
title: "FD-03-400__sql-to-pandas"
date: 2026-09-09
id: FD-03-400
type: lecture
tags:
  - FD
  - Week03
  - pandas
---

## 🤝 SQL과 pandas의 완벽한 분업: 데이터 분석 파이프라인

> [!info] 학습 목표
>
> - SQL로 가볍게 정제한 쿼리 결과를 DataFrame으로 바통 터치받는다.
> - SQL의 몫(DB 레벨의 고속 필터링·조인)과 pandas의 몫(시계열·통계·시각화)을 명확히 구분한다.
> - Week 02의 분석 기법을 연결하여 2025년 최적의 투자 후보 리포트를 완성한다.

---

## 📝 파이프라인의 완성: 복합 쿼리를 파이썬에 얹는다

앞선 [[FD-03-300__sql-remind|300]]에서는 앵커 질문의 조각들(`WHERE`, `ORDER BY`, `LIMIT` 등)을 하나씩 확인했다.
이제 SQL로 받은 표를 파이썬 분석 파이프라인으로 그대로 이어 붙인다. 표 하나만 있어도 이 흐름을 보이는 데는 충분하다.

**§400-1**
```python
# §FD-03-400-1
query = "SELECT * FROM financials WHERE year = 2025"
df = pd.read_sql(query, conn)
df.head()

# 예상 출력:
#      code  year  revenue  operating_profit  net_income  equity
#    005930  2025  3466200            499015      381432 3467567
#    000660  2025  1007720            364837      303706 1265440
#    009150  2025    91728              8991        7191  102726
#    051910  2025   470256             32577       27965  559304
#    011170  2025   131100              3851        2867  143361
```

**이것이 바로 금융 데이터 실무의 황금 분업 구조입니다.**
- **SQL의 몫:** 수백만 행의 원천 데이터 중 필요한 행과 열만 DB 엔진에서 0.001초 만에 깎아냅니다.
- **pandas의 몫:** DB가 가볍게 추려준 최정예 DataFrame을 받아 Week 02에서 손에 익힌 통계(`describe`), 결측치 처리, 차트 시각화로 이어갑니다.

주의할 습관 하나 — 쿼리 안에 값을 f-string으로 직접 끼워 넣지 않는다.

**§400-2**
```python
# 지양
code = "005930"
query = f"SELECT * FROM companies WHERE code = '{code}'"
```

이유는 이번 주 범위 밖이지만(외부 값이 SQL 문자열에 그대로 섞이면 생기는 위험이 있다), 습관은 지금 잡아두는 편이 나중에 고치는 것보다 훨씬 싸다.

## 🔍 받아서 이어 한다

DB에서 받은 `df`는 CSV로 읽은 `df`와 똑같은 DataFrame이다. [[FD-02-300__dataframe|Week02 300]]에서 했던 것을 그대로 다시 쓸 수 있다.

**§400-3**
```python
# §FD-03-400-2
df.info()

# 예상 출력:
# <class 'pandas.DataFrame'>
# RangeIndex: 12 entries, 0 to 11
# Data columns (total 6 columns):
#  #   Column            Non-Null Count  Dtype
# ---  ------            --------------  -----
#  0   code              12 non-null     str
#  1   year              12 non-null     int64
#  2   revenue           12 non-null     int64
#  3   operating_profit  12 non-null     int64
#  4   net_income        12 non-null     int64
#  5   equity            12 non-null     int64
```

**§400-4**
```python
# §FD-03-400-3
df.describe()

# 예상 출력:
#          year       revenue  operating_profit     net_income        equity
# count    12.0  1.200000e+01         12.000000      12.000000  1.200000e+01
# mean   2025.0  7.646127e+05     127129.000000  101621.500000  8.639101e+05
# std       0.0  1.009713e+06     172346.711145  135898.425683  1.086309e+06
# min    2025.0  5.474000e+04       3851.000000    2867.000000  5.085700e+04
# 25%    2025.0  1.277500e+05      15432.250000   12886.500000  1.590495e+05
# 50%    2025.0  3.028200e+05      27474.000000   23390.000000  3.391780e+05
# 75%    2025.0  1.058265e+06     230214.250000  180609.000000  1.227859e+06
# max    2025.0  3.466200e+06     499015.000000  381432.000000  3.467567e+06
```

조건 필터와 정렬도 Week02에서 쓰던 그대로다.

**§400-5**
```python
# §FD-03-400-4
df[df['revenue'] > 500000].sort_values('revenue', ascending=False)

# 예상 출력:
#      code  year  revenue  operating_profit  net_income   equity
#    005930  2025  3466200            499015      381432  3467567
#    005380  2025  1797600            304402      248457  2484568
#    000270  2025  1209900            205485      157993  1215332
#    000660  2025  1007720            364837      303706  1265440
```

같은 표를 이번엔 파일이 아니라 DB에서 받았을 뿐, 그 다음부터는 Week02와 완전히 같은 작업이다 — 매출이 큰 회사들을 지금 손에 쥔 셈이다.

이번 주의 요점이 바로 여기다 — **SQL로 필요한 만큼만 줄이고, 그 다음 가공은 pandas 쪽이 더 편하다.**

> [!tip]- 심화 — 업종(sector)까지 다시 보려면
> 지금 `df`에는 `sector`가 없다 — `financials` 한 표만 받았기 때문이다. 업종별로 비교하려면 [[FD-03-300__sql-remind|300]]의 심화처럼 `companies`와 다시 이어야 한다.
> ```sql
> SELECT c.name, c.sector, f.revenue, ROUND(f.net_income * 1.0 / f.equity, 4) AS roe
> FROM companies c
> JOIN financials f ON c.code = f.code
> WHERE f.year = 2025
> ```
> ```text
>     name sector  revenue   roe
>   삼성전자 전기전자  3466200  0.11
> SK하이닉스 전기전자  1007720  0.24
>   삼성전기 전기전자    91728  0.07
>    LG화학   화학   470256  0.05
>  롯데케미칼   화학   131100  0.02
> ```
> 이 표를 다시 손에 쥐면, `df.groupby('sector')['roe'].mean().round(4)` 한 줄로 [[FD-03-300__sql-remind|300]]의 심화에서 SQL `GROUP BY`로 얻은 것과 완전히 같은 업종별 평균을 pandas만으로 다시 만들 수 있다 — SQL이 표를 줄여주고 난 다음부터는, 몇 번이고 새로 쿼리를 던지지 않고 pandas 쪽에서 자유롭게 다시 요약할 수 있다는 뜻이다.

## ⚖️ 어디까지 SQL로, 어디부터 pandas로

원칙은 한 줄로 정리된다.

==**줄이는 일은 SQL이, 주무르는 일은 pandas가.**==

```mermaid
flowchart LR
  A["DB에 있는 전부"] -->|"pd.read_sql<br/>(줄이기)"| B["내 손 안의 표<br/>(주무르기)"]

  style A fill:#4A90D9,color:#fff
  style B fill:#27AE60,color:#fff
```
*화살표 위에는 "줄이기", 오른쪽 상자 안에는 "주무르기"라고 적혀 있다 — SQL과 pandas의 경계선이 어디인지가 이 배치만으로 보인다.*

전체 데이터가 수백만 행이라면, 그중 필요한 500행을 골라내는 일은 SQL이 빠르다. 이미 걸러진 500행을 가지고 그림을 그리거나 계산을 이어가는 일은 pandas가 편하다. `WHERE`로 조건을 걸어 표를 줄인 다음, 그 결과를 `pd.read_sql`로 받아 pandas로 주무르는 지금까지의 흐름이 정확히 이 경계선을 지킨 것이다.

실습에서는 `pd.read_sql`로 표를 받아 Week02 수준의 필터·정렬을 직접 이어서 해본다 — 업종별 그룹 요약은 심화다.

---

## 🔖 핵심 요약

> [!summary] 🏆 이 노트를 마쳤다면?
>
> - [ ] SQL 쿼리를 문자열로 만들어 `pd.read_sql`로 DataFrame에 담을 수 있다.
> - [ ] DB에서 받은 표에 `head`·`info`·`describe`·필터·정렬을 그대로 적용할 수 있다.
> - [ ] "줄이는 일은 SQL, 주무르는 일은 pandas"라는 기준으로 어디까지가 자기 몫인지 구분할 수 있다.
> - [ ] 실습에서: `pd.read_sql`로 표를 받아 필터·정렬로 이어서 확인한다. (업종별 pandas `groupby`는 심화)
