---
title: "FD-03-300__sql-remind"
date: 2026-09-09
id: FD-03-300
type: lecture
tags:
  - FD
  - Week03
  - SQL
---

## 앵커 질문을 SQL로 옮긴다

> [!info] 학습 목표
>
> - 앵커 질문의 조각들을 `WHERE`·`ORDER BY`·`JOIN`으로 하나씩 옮긴다. (`GROUP BY`로 업종 평균까지 보는 것은 심화)
> - SQL 에러의 생김새를 알아보고, 무엇을 확인해야 하는지 안다.
> - 자기가 궁금한 조건 하나를 직접 SQL로 만든다.

---

## 🎯 조건으로 거르기 — WHERE

앵커 질문의 첫 조각은 "매출이 어느 정도 이상인 회사"다. [[FD-03-200__sqlite-open|200]]에서 `SELECT *`로 표 전체를 봤으니, 여기서 새로 등장하는 건 `WHERE` 하나뿐이다.

**§300-1**
```python
# §FD-03-300-1
query = "SELECT code, revenue FROM financials WHERE revenue > 300000 AND year = 2025"
pd.read_sql(query, conn)

# 예상 출력:
#      code  revenue
#    005930  3466200
#    000660  1007720
#    051910   470256
#    010950   367710
#    005380  1797600
#    000270  1209900
```

`SELECT`는 "무엇을 볼지"를 정하고, `WHERE`는 "어느 행만 볼지"를 정한다. `AND`로 조건을 여러 개 이을 수 있다는 것도 여기서 같이 확인한다.

종목코드를 조건에 쓸 때는 따옴표를 반드시 붙인다.

```sql
WHERE code = '005930'
```

숫자로 `WHERE code = 5930`이라고 쓰면 앞의 0 두 개가 사라진 값과 비교하게 되어 원하는 행을 찾지 못한다. `code`는 TEXT 컬럼이라는 걸 항상 기억한다.

## 📐 상위 몇 개만 — ORDER BY · LIMIT

조건에 맞는 회사가 여럿 나왔다. 이 중 매출이 큰 순서로 위에서 몇 개만 보고 싶다면 정렬이 필요하다. Week02에서 이미 `sort_values`와 `nlargest`로 해봤던 바로 그 동작이다 — 이름만 SQL식으로 바뀐다.

**§300-2**
```python
# §FD-03-300-2
query = "SELECT code, revenue FROM financials WHERE year = 2025 ORDER BY revenue DESC LIMIT 5"
pd.read_sql(query, conn)

# 예상 출력:
#      code  revenue
#    005930  3466200
#    005380  1797600
#    000270  1209900
#    000660  1007720
#    051910   470256
```

`ORDER BY revenue DESC`가 매출 큰 순서로 표 전체를 다시 세우고, `LIMIT 5`가 위에서 5개만 자른다. `DESC`를 빼면 반대로 작은 순서가 된다 — 단어 하나로 정렬 방향이 뒤집힌다.

> [!warning] 함정 — LIMIT은 정렬 뒤에 걸린다
> - `ORDER BY` 없이 `LIMIT 5`만 쓰면 "매출이 큰 5개"가 아니라 **DB가 저장된 순서 그대로의 아무 5개**가 나온다.
> - 아래에서 실제로 확인해본다.

**§300-3**
```python
# §FD-03-300-2b
query = "SELECT code, revenue FROM financials WHERE year = 2025 LIMIT 5"
pd.read_sql(query, conn)

# 예상 출력:
#      code  revenue
#    005930  3466200
#    000660  1007720
#    009150    91728
#    051910   470256
#    011170   131100
```

매출 순서가 전혀 아니다 — `ORDER BY` 없는 `LIMIT`은 "정렬된 상위"가 아니라는 것을 기억한다.

## ➕ 없는 열을 만들어 쓴다 — AS · 계산 컬럼

앵커 질문의 "수익성이 좋은"을 숫자로 바꾸려면 계산이 필요하다. 수익성 지표 중 하나인 ROE(자기자본이익률)는 순이익을 자기자본으로 나눈 값이다.

**§300-4**
```python
# §FD-03-300-3
query = """
SELECT code, net_income, equity,
       net_income / equity AS roe_wrong,
       ROUND(net_income * 1.0 / equity, 4) AS roe_right
FROM financials WHERE year = 2025 LIMIT 5
"""
pd.read_sql(query, conn)

# 예상 출력:
#      code  net_income   equity  roe_wrong  roe_right
#    005930      381432  3467567          0       0.11
#    000660      303706  1265440          0       0.24
#    009150        7191   102726          0       0.07
#    051910       27965   559304          0       0.05
#    011170        2867   143361          0       0.02
```

`roe_wrong` 열을 보자 — 전부 0이다. `net_income / equity`가 정수끼리 나눗셈이라 소수점 아래가 통째로 버려진 것이다. `net_income * 1.0`처럼 하나를 실수로 만들어주면(`roe_right`) 정상적인 소수값이 나온다. 이 함정은 유도하지 않고 사실만 짚는다 — "정수끼리 나누면 소수가 날아간다."

`AS`는 계산 결과에 붙이는 이름표일 뿐이다. `roe_right`라는 이름은 원래 표에 없던 열이지만, 이렇게 새로 만들어 쓸 수 있다.

앵커 질문의 조각(`WHERE`, `ORDER BY`, `LIMIT`)을 한 쿼리에 모아서, 표 하나로 앵커 질문에 한 걸음 더 가까이 가본다. 새 문법은 없다 — 지금까지 배운 것을 합치기만 한다.

**§300-5**
```python
# §FD-03-300-5
query = "SELECT code, revenue FROM financials WHERE year = 2025 AND revenue > 300000 ORDER BY revenue DESC LIMIT 5"
pd.read_sql(query, conn)

# 예상 출력:
#      code  revenue
#    005930  3466200
#    005380  1797600
#    000270  1209900
#    000660  1007720
#    051910   470256
```

표 하나, 조건 하나, 정렬 하나 — 이 정도가 이번 주 SQL의 실제 그릇이다. 앵커 질문의 나머지 조각인 "업종 평균보다"는 `companies`의 업종 정보까지 있어야 하는데, 그건 아래 심화에서 다룬다.

> [!tip]- 심화 — 업종 평균까지 보려면 (JOIN + GROUP BY)
> 앵커 질문의 "산업 평균보다"를 확인하려면 업종별 평균을 구해야 한다. 이번 질문은 `companies`의 업종(`sector`)과 `financials`의 재무 수치를 같이 봐야 해서, 아래 쿼리에 `JOIN ... ON`이 등장한다 — "두 표가 `code`로 이어져 있다"는 것만 알고 넘어가도 된다.
> ```sql
> SELECT c.name, AVG(f.net_income * 1.0 / f.equity) AS avg_roe
> FROM companies c JOIN financials f ON c.code = f.code
> WHERE f.year = 2025
> GROUP BY c.sector
> ```
> 막히는 이유를 먼저 말해두면 — `GROUP BY c.sector`로 묶고 나면, 한 업종 안에 회사가 여러 개인데 `name`은 회사마다 다르다. "묶은 다음엔 하나로 못 줄이는 값을 그대로 꺼낼 수 없다"는 게 SQL의 원칙이다.
> 여기서 실제로 확인해볼 게 하나 있다. 이 쿼리를 SQLite에서 그대로 돌리면 무슨 일이 벌어질까 — 사실 SQLite는 **에러를 내지 않는다.** 대신 **각 업종에서 아무 회사 이름이나 하나 골라 보여준다.** 전기전자 업종 평균 ROE(0.14) 옆에 `삼성전자`라는 이름이 붙는 식인데, 저건 전기전자 세 회사(삼성전자·SK하이닉스·삼성전기)의 평균이지 삼성전자만의 값이 아니다. **에러가 나면 오히려 안전하다 — 여기서 위험한 건 조용히 틀린 답을 내놓는다는 것이다.** 그래서 묶은 다음에는 **묶은 기준(`c.sector`)과 줄인 값(`AVG`, `COUNT`)만** 꺼내는 것이 안전한 습관이다 — 아래 쿼리가 그 습관을 지킨 버전이다.
> ```sql
> SELECT c.sector, ROUND(AVG(f.net_income * 1.0 / f.equity), 4) AS avg_roe, COUNT(*) AS n
> FROM companies c JOIN financials f ON c.code = f.code
> WHERE f.year = 2025
> GROUP BY c.sector
> ORDER BY avg_roe DESC
> ```
> ```text
> sector  avg_roe  n
> 전기전자   0.1400  3
>  바이오   0.1400  1
>  자동차   0.1150  2
>  서비스   0.0900  1
>   금융   0.0850  2
>   화학   0.0433  3
> ```
> 이제 각 업종의 평균과 회사 수가 정확히 보인다. 전기전자와 바이오 업종의 평균 ROE가 가장 높다.
> - SQLite는 `GROUP BY` 뒤에 묶은 기준이 아닌 열을 꺼내도 에러 없이 아무 값이나 골라 보여준다.
> - 더 엄격한 DB(PostgreSQL 등)는 이 자리에서 바로 에러를 낸다 — 뒤에서 클라우드 DB로 넘어갈 때 다시 만날 이야기다.

## 🔗 두 표를 잇는다 — JOIN

[[FD-03-100__why-database|100]]의 쇼핑몰 그림을 다시 불러온다 — "두 표에 같이 있는 열로 잇는다"고 했다. `companies`와 `financials` 둘 다에 `code` 열이 있으니, 그 열로 잇는다.

![[assets/week03-join-mechanism.svg]]
*왼쪽 `companies`와 오른쪽 `financials`가 같은 `code` 값끼리(굵은 초록 선) 한 행으로 합쳐진다. 옅은 붉은 배경은 `ON`을 지웠을 때 모든 행이 모든 행과 이어지는 모습이다 — 지금 이 그림에서는 존재하지 않는 연결이다.*

**§300-6**
```python
# §FD-03-300-6
query = """
SELECT COUNT(*) AS n_rows
FROM companies c JOIN financials f ON c.code = f.code
"""
pd.read_sql(query, conn)

# 예상 출력:
#    n_rows
#        24
```

`ON c.code = f.code`가 [[FD-03-100__why-database|100]]에서 말한 "같이 있는 열로 잇는다"는 문장을 그대로 코드로 옮긴 것이다. 회사 12개 × 연도 2개(2024·2025)라서 24행이 나온다.

이제 `ON`을 지우고 다시 실행해보자.

**§300-7**
```python
# §FD-03-300-7
query = "SELECT COUNT(*) AS n_rows FROM companies c JOIN financials f"
pd.read_sql(query, conn)

# 예상 출력:
#    n_rows
#       288
```

24행이 아니라 288행이 나온다 (12개 회사 × 24개 재무 행). `ON`이 없으면 SQL은 "어느 행과 어느 행을 짝지어야 할지" 기준이 없어서 **가능한 모든 조합**을 만들어버린다. 에러가 나는 게 아니라 결과가 나온다는 것이 이 함정의 진짜 위험이다 — 숫자만 보면 그럴듯해 보이지만 완전히 다른 질문에 대한 답이다.

## 🚨 에러 읽는 법

지금까지 조용히 넘어갔지만, SQL을 쓰다 보면 이보다 먼저 걸리는 순간이 있다 — 에러 메시지 자체를 읽는 법을 배운 적이 없어서 막히는 순간이다. 파이썬 에러(트레이스백)와는 생김새가 완전히 다르다 — 줄 번호도, 화살표도, 긴 호출 스택도 없이 **한 줄**만 나온다.

| 에러 메시지 | 무엇을 확인할지 |
|---|---|
| `no such table: company` | 표 이름 철자 · 복수형 여부 |
| `no such column: ticker` | 열 이름 철자 · 어느 표에 있는 열인지 |
| `near "SELEC": syntax error` | 키워드 철자 · 쉼표·괄호 짝 |
| `misuse of aggregate function AVG()` | `AVG` 같은 집계 함수를 `GROUP BY` 없이 `WHERE` 조건 자리에 직접 쓰고 있는지 |

한 줄짜리 에러가 오히려 친절하다 — 파이썬 트레이스백처럼 "어디서부터 읽어야 하나"를 고민할 필요가 없다. 대표 넷을 실제로 하나씩 만들어보자.

**§300-8**
```python
# §FD-03-300-8
try:
    pd.read_sql("SELECT * FROM company LIMIT 1", conn)
except Exception as e:
    print(e)

# 예상 출력:
# Execution failed on sql 'SELECT * FROM company LIMIT 1': no such table: company
```

**§300-9**
```python
# §FD-03-300-9
for bad_query in [
    "SELECT ticker FROM companies LIMIT 1",
    "SELEC * FROM companies LIMIT 1",
    "SELECT code FROM financials WHERE AVG(revenue) > 0",
]:
    try:
        pd.read_sql(bad_query, conn)
    except Exception as e:
        print(e)

# 예상 출력:
# Execution failed on sql 'SELECT ticker FROM companies LIMIT 1': no such column: ticker
# Execution failed on sql 'SELEC * FROM companies LIMIT 1': near "SELEC": syntax error
# Execution failed on sql 'SELECT code FROM financials WHERE AVG(revenue) > 0': misuse of aggregate function AVG()
```

거의 항상 "이름을 잘못 썼거나, 순서를 잘못 썼거나" 둘 중 하나다. 이 표는 실습 노트북 맨 위에도 그대로 올라간다 — 막혔을 때 손이 먼저 가는 자리에 있어야 쓸모가 있다.

## ✍️ mini mission 3개

이제 배운 조각들을 이어서 앵커 질문에 실제로 답해본다.

> [!tip]- 심화 — 미션 1: 특정 업종에서 매출 상위 5개 회사
> `companies`와 `financials`를 `code`로 이어야 회사 이름과 매출을 한 번에 볼 수 있다. `WHERE`로 업종을 고르고, `ORDER BY ... DESC LIMIT 5`로 상위 5개를 자른다.
> ```sql
> SELECT c.name, f.revenue
> FROM companies c JOIN financials f ON c.code = f.code
> WHERE c.sector = '전기전자' AND f.year = 2025
> ORDER BY f.revenue DESC LIMIT 5
> ```
> ```text
> name       revenue
> 삼성전자    3466200
> SK하이닉스  1007720
> 삼성전기      91728
> ```
> 전기전자 업종은 회사가 셋뿐이라 다섯 개를 채우지 못했다 — 이 표가 답할 수 있는 만큼만 나온 것이지 쿼리가 틀린 게 아니다.

> [!tip]- 심화 — 미션 2: 업종별 평균 수익성과 회사 수
> 위 GROUP BY 절 심화에서 쓴 쿼리와 똑같은 모양이다. 묶은 기준(`sector`)과 집계값(`AVG`, `COUNT`)만 고른다.
> ```sql
> SELECT c.sector, ROUND(AVG(f.net_income * 1.0 / f.equity), 4) AS avg_roe, COUNT(*) AS n
> FROM companies c JOIN financials f ON c.code = f.code
> WHERE f.year = 2025 GROUP BY c.sector
> ```
> ```text
> sector  avg_roe  n
> 금융    0.0850   2
> 바이오  0.1400   1
> 서비스  0.0900   1
> 자동차  0.1150   2
> 전기전자 0.1400  3
> 화학    0.0433   3
> ```

**미션 3 — 자유 조건**

`companies`와 `financials`를 이어서, **자기가 궁금한 조건 하나**를 `WHERE`에 직접 넣어본다. "ROE가 0.1보다 큰 회사는?"이어도 좋고, "이름에 특정 글자가 들어간 회사는?"이어도 좋다.

앞의 두 미션(심화)은 시킨 대로 풀면 답이 나온다. 세 번째가 이 노트의 진짜 착지점이다 — 자기가 직접 만든 조건 하나가 있어야, "오늘 뭐 했어?"라는 질문에 "이런 질문도 SQL로 물어봤다"고 말할 거리가 생긴다.

## 📚 더 있는 것들 (자료만)

subquery, CTE(공통 테이블 표현식), window function, 3개 이상 표의 JOIN, transaction, index, 정규화 — 이름만 짚고 넘어간다. 이런 주제는 데이터베이스 과목이 제대로 다룬다. 지금 몰라도 이번 주 학습목표에는 지장이 없다.

실습에서는 SQL remind 드릴과 함께 위 미션 3(자유 조건)을 반드시 다시 풀어본다 — 미션 1·2(심화)는 시간을 보고 선택한다.

---

## 🔖 핵심 요약

> [!summary] 🏆 이 노트를 마쳤다면?
>
> - [ ] `WHERE`로 조건에 맞는 행만, `ORDER BY`/`LIMIT`으로 상위 몇 개만 고를 수 있다.
> - [ ] 정수 나눗셈이 소수점을 버린다는 것과, `* 1.0`으로 피하는 방법을 설명할 수 있다.
> - [ ] `JOIN ... ON`이 왜 필요한지, `ON`을 지우면 행 수가 왜 폭발하는지 설명할 수 있다.
> - [ ] SQL 에러 메시지 4종을 보고 무엇을 확인해야 할지 안다.
> - [ ] 실습에서: 미션 3(자유 조건)을 직접 SQL로 풀어본다. (미션 1·2, `GROUP BY` 뒤 임의값 반환은 심화)
