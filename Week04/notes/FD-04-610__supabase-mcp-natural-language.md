---
title: "FD-04-610__supabase-mcp-natural-language"
date: 2026-09-25
id: FD-04-610
type: lecture
tags:
  - FD
  - Week04
  - supabase
  - MCP
---

## ☁️ 내 Supabase에 내 데이터 표를 만들려면?

Week03에는 수업 프로젝트의 표를 읽었다. 이번에는 학생마다 자기 Supabase 프로젝트를 준비해, OpenDART에서 받은 삼성전자 자료를 직접 넣는다. SQL을 직접 쓰거나, MCP로 연결한 에이전트에게 자연어로 부탁할 수 있다.

> [!info] 학습 목표
>
> - 자기 Supabase 프로젝트의 URL과 키를 FD_26 `.env`에 저장한다.
> - 프로젝트 범위를 제한한 Supabase MCP를 연결한다.
> - 자연어로 `financials` 표를 만들고 OpenDART 자료를 INSERT한 뒤, 같은 값을 쓰는 Python SDK 코드를 실행해 본다.

> [!info] 앞뒤 순서
> - §300에서 OpenDART 키와 응답을 준비한다.
> - §410에서 OpenDART MCP를 연결한다.
> - **이 절에서** Supabase 프로젝트와 자연어 SQL을 마친다.
> - 마지막으로 §600 설명을 보고 §900 노트북에서 SDK를 실행한다.
> - 이 절을 끝내면 §600/§900으로 한 번만 이동하면 된다.

> [!warning] `[live]` 응답이 있어야 하는 경로
> - §300 결과가 `[live]`일 때만 이 절의 Supabase MCP → §900 SDK 경로를 진행한다.
> - `[fixture]`는 오프라인 수업용 대체 자료이며 실제 OpenDART API 응답이 아니다.
> - `[fixture]`만 있다면 [[FD-04-800__mcp-load-and-measure-student|§800 SQLite 실습]]을 마치고, 실제 응답을 받은 뒤 이 §610으로 돌아온다.
> - `[fixture]`를 실제 OpenDART 결과인 것처럼 Supabase에 넣지 않는다.

## 🪪 프로젝트를 준비하고 키를 보관한다

[supabase.com](https://supabase.com)에 가입하고 로그인한다. 화면에서 `New project`를 눌러 개인 연습용 프로젝트를 만든다. 프로젝트를 만든 뒤 다음 순서로 값을 찾는다.

> [!info] 대시보드에서 순서대로 찾아 옮겨 적는다
> | 값 | 어디서 찾나 | 어디에 쓰나 |
> |---|---|---|
> | OpenDART API 키 | OpenDART 인증키 발급 페이지 | FD_26 환경변수 파일의 `OPENDART_API_KEY`; OpenDART API/MCP 요청 |
> | Supabase 프로젝트 URL | 대시보드 `Connect` | FD_26 환경변수 파일의 `SUPABASE_URL`; Python SDK |
> | 프로젝트 ref | 프로젝트 URL에서 `.supabase.co` 앞부분 | Supabase MCP 주소의 `project_ref` |
> | Supabase publishable key | `Project Settings → API Keys` | FD_26 환경변수 파일의 `SUPABASE_PUBLISHABLE_KEY`; 로컬 Python SDK |
> | Supabase secret key | `Project Settings → API Keys` | 백엔드 전용 — 이 실습의 로컬 코드에는 쓰지 않는다 |
> | OAuth 로그인 | MCP 연결 중 브라우저에서 직접 로그인 | MCP 연결 승인; `.env`에 저장하지 않음 |

1. **프로젝트 URL**: 프로젝트 대시보드에서 `Connect`를 누르고 `Project URL`을 복사한다. 주소는 `https://<project-ref>.supabase.co` 모양이다. 여기서 `<project-ref>`는 주소에서 `.supabase.co` 앞에 있는 프로젝트 고유 글자다. MCP 주소에 넣을 때도 이 글자만 사용한다.
2. **Publishable API key**: 왼쪽 아래 `Project Settings`(톱니바퀴) → `API Keys`를 연다. `sb_publishable_...` 형식의 publishable key를 생성하거나 복사한다. Supabase 공식 안내도 프로젝트 URL은 `Connect` 창에서, 키는 `Settings → API Keys`에서 찾도록 안내한다. [Supabase API 키 안내](https://supabase.com/docs/guides/getting-started/api-keys)
3. **FD_26에 저장**: `FD_26` 루트의 환경변수 파일에 변수 이름과 자기 값 두 줄을 적는다. 이 파일을 채팅·캡처·Git에 올리지 않는다.

예를 들어 안내용 주소 `https://demo-project-123.supabase.co`의 project ref는 `demo-project-123`이다. 이 예시는 읽는 연습용이므로 실제 설정에는 자기 프로젝트에서 복사한 주소를 쓴다.

![[FD-04-600-supabase-signup.png]]
*가입 화면 예시다. 프로젝트 URL·고유 ID·API 키 화면은 Mark의 로그인 후 캡처하기로 해 현재 교재에 넣지 않았다.*

`sb_publishable_...` 키는 각 요청이 `financials` 표에서 할 수 있는 일을 뒤에서 만드는 RLS(Row Level Security) 정책이 정한다. 이번 실습은 로컬 Python SDK도 이 키만으로 실행한다. `sb_secret_...` 키는 RLS를 우회하는 백엔드 전용 키라서 클라이언트·학생 노트북 코드에는 넣지 않는다 — 이번 실습에서는 발급하거나 쓰지 않는다.

FD_26 루트의 `.env`에 아래 변수 이름을 추가하고, 각자 발급한 값을 직접 넣는다. 실제 값은 노트·노트북·화면 캡처에 옮기지 않는다.

```text
SUPABASE_URL=https://<내 프로젝트 ref>.supabase.co
SUPABASE_PUBLISHABLE_KEY=<내 프로젝트 publishable key>
```

`sb_publishable_...` 키도 Git·채팅·화면 캡처에는 남기지 않는다 — 값 자체보다, 이 키와 프로젝트 URL을 아는 사람이면 누구나 RLS 정책이 열어 둔 범위까지 접근할 수 있기 때문이다. [Supabase 키 보안 안내](https://supabase.com/docs/guides/database/secure-data)

## 🗣️ Supabase MCP를 프로젝트에 연결한다

Supabase 원격 MCP는 브라우저 OAuth로 로그인하므로 MCP 연결용 개인 토큰(PAT)이나 secret API key를 직접 설정하지 않는다. 연결 주소에 자기 프로젝트 ref를 넣어 접근 범위를 제한하고 `database` 도구만 켠다. 공식 문서는 `project_ref`가 프로젝트 접근 범위를 좁히고, `features`가 사용할 도구 묶음을 고른다고 설명한다. [Supabase MCP 설정](https://supabase.com/docs/guides/ai-tools/mcp)

> [!warning] 두 로그인은 서로 다른 목적이다
> - 브라우저 OAuth는 MCP 에이전트가 Supabase 계정에 연결할 때 쓴다.
> - 환경변수 파일의 publishable key는 내 컴퓨터에서 Python SDK가 쓸 때만 쓴다.
> - secret key는 RLS를 우회하는 백엔드 전용 키라서 이번 실습의 어느 설정에도 넣지 않는다.
> - 한쪽의 키를 다른 쪽 설정에 복사하지 않는다.

내 노트북을 꺼도 데이터가 살아 있어야 한다. 그래서 각자 인터넷 위에 안전한 저장소(Supabase)를 하나씩 만들었다. 이제 AI 비서에게 그 저장소로 가는 전용 통로를 열어 준다 — 내 `FD_26` 프로젝트 하나에만 열리는 좁은 통로다.

> [!tip]- 📋 에이전트에게 보낼 연결 요청 (클릭해서 펼치기)
> “현재 공식 문서를 확인한 뒤 Supabase 공식 원격 MCP를 이 `FD_26` 프로젝트에만 연결해줘. 서버 URL은 `https://mcp.supabase.com/mcp?project_ref=<내 project-ref>&features=database`야. 먼저 수정할 설정 파일의 전체 경로와 변경 내용을 보여줘. 프로젝트 범위 설정이 불가능하면 사용자 전체 설정을 바꾸지 말고 멈춰. OAuth 로그인 화면을 열어주면 내가 직접 로그인하고, PAT나 secret key는 설정 파일·대화·출력에 적지 마. 연결된 뒤에는 내 프로젝트의 표 목록을 조회해 실제 연결을 확인하고, SQL을 실행할 때는 먼저 SQL을 보여줘.”

로그인 권한을 확인할 때 자기 프로젝트만 연결됐는지 본다. 표 생성과 데이터 쓰기는 변경 작업이므로, 에이전트가 보여주는 SQL을 읽은 뒤 실행을 승인한다. 프로젝트 범위를 지정하지 않은 연결은 계정의 다른 프로젝트까지 보일 수 있다.

## 🧾 자연어로 표를 만들고 OpenDART 값을 넣는다

먼저 [[FD-04-410__mcp-agentic-install|§410]]에서 연결한 `opendart-mcp`가 동작하는지 확인한다. 이제 연결한 통로로 AI 비서에게 실제 심부름을 시킨다 — OpenDART에서 받은 값을 내 저장소의 표에 넣어 달라고 부탁하는 것이다. 아래처럼 요청하면 에이전트가 OpenDART 자료를 받고, Supabase MCP로 표를 만들고 행을 쓴다. 한 번 받은 자료를 사람이 CSV로 저장하거나 SQLite에서 다시 꺼낼 필요가 없다.

> [!tip]- 📋 학생이 보낼 요청 (클릭해서 펼치기)
> “OpenDART에서 삼성전자(corp_code `00126380`)의 2025년 사업보고서 연결(CFS) 재무제표 중 매출액·영업이익·당기순이익·자본총계를 받아 억원 단위로 정리해줘. 내 프로젝트 범위로 연결된 Supabase MCP에 `financials` 표가 없으면 `code`(text), `year`(integer), `revenue`, `operating_profit`, `net_income`, `equity`(bigint) 열과 `(code, year)` 기본키를 갖도록 만들어줘. 실행할 SQL을 먼저 보여준 뒤 내가 승인하면 이 네 값을 한 행으로 INSERT하고, 같은 조건으로 SELECT해서 결과를 알려줘. API 키와 Supabase 키는 출력하지 마.”

아래 SQL은 에이전트가 제시할 내용의 **확인 기준**이다. 실제로 실행할 SQL을 다시 복사하라는 뜻은 아니다. 열 이름·자료형·기본키와 네 재무 값이 맞는지 살핀 뒤 실행을 승인한다.

```sql
CREATE TABLE public.financials (
    code text NOT NULL,
    year integer NOT NULL,
    revenue bigint,
    operating_profit bigint,
    net_income bigint,
    equity bigint,
    PRIMARY KEY (code, year)
);

INSERT INTO public.financials
    (code, year, revenue, operating_profit, net_income, equity)
VALUES
    ('005930', 2025, 3336059, 436010, 452068, 4363203);

SELECT code, year, net_income, equity
FROM public.financials
WHERE code = '005930' AND year = 2025;
```

마지막 `SELECT`의 예상 모양은 다음과 같다. 에이전트의 결과와 종목·연도, 당기순이익·자본총계를 비교한다.

| code | year | net_income | equity |
|---|---:|---:|---:|
| 005930 | 2025 | 452068 | 4363203 |

처음 `INSERT`할 때는 해당 종목·연도 행이 아직 없어야 한다. 에이전트가 먼저 테이블 존재 여부를 확인하게 하고, 없을 때만 표를 만들고 SQL을 먼저 보여준 뒤 진행한다. MCP로 넣은 행은 같은 프로젝트에서 [[FD-04-600__cloud-supabase|§600]] SDK 실습의 `upsert`와 조회로 확인한다. SDK 셀은 재실행해도 기본키 때문에 행이 늘지 않는다. 이미 행이 있다는 오류가 나면 INSERT를 반복하지 말고 SELECT로 기존 값을 확인한다.

## 🔒 이 표는 누가 읽고 쓸 수 있나 — RLS 정책

방금 만든 `financials` 표는 기본값으로는 아무 요청도 거부한다. §600의 로컬 SDK가 publishable key로 읽고 쓰려면, "이 키로 온 요청은 이 표에서 무엇을 할 수 있다"는 규칙이 따로 있어야 한다. 이 규칙을 RLS(Row Level Security) 정책이라 부른다. 12살에게 설명하면: 이 표에 자물쇠를 걸어 두고, publishable key를 가진 요청이 열 수 있는 문(읽기·쓰기)을 하나씩 정해 주는 것이다.

에이전트에게 아래 SQL을 실행해 달라고 요청한다 — 표를 만들 때와 같은 방식으로, 실행 전 SQL을 먼저 확인한다.

```sql
alter table public.financials enable row level security;
create policy "read practice data" on public.financials
  for select to anon using (true);
create policy "insert practice data" on public.financials
  for insert to anon with check (true);
create policy "update practice data" on public.financials
  for update to anon using (true) with check (true); -- upsert 충돌 갱신용
```

`to anon`은 publishable key로 오는 요청을 가리킨다. 세 정책 모두 조건이 `true`이므로, 각자의 연습 프로젝트에서는 자유롭게 읽고 쓰도록 열어 둔 것이다 — 개인 연습 프로젝트이므로 이것이 가장 단순한 정책이다.

> [!warning] `true`로 여는 정책의 경계
> - "내가 만든 프로젝트니까 나만 쓸 수 있다"는 뜻이 아니다.
> - 그 프로젝트의 URL과 publishable key를 아는 사람이면 누구나 읽고 쓸 수 있다는 뜻이다.
> - 이번 실습은 각자의 개인 연습 프로젝트 범위를 벗어나지 않으므로 괜찮지만, URL과 키를 공개 저장소나 채팅에 올리지 않는다.

## 💻 자연어 명령에서 실행 가능한 코드로

에이전트에게 자연어 요청을 하면 SQL을 대신 만들고 실행할 수 있지만, 대화만으로는 다음 실행을 위한 수집 코드가 노트북에 남지 않는다. 그래서 방금 다룬 삼성전자 2025년 자료를 Python SDK 코드로 한 번 더 적재한다. 같은 종목·연도와 계정 값을 두 방식으로 확인하는 것은 앞에서 배운 내용을 복기하고, 자연어로 SQL을 시킨 경험을 다시 실행 가능한 코드로 옮기는 단계다. 결과가 같은 행을 가리키는지 비교한다.

> [!tip]- 💬 SDK 코드 요청 (클릭해서 펼치기)
> “방금 OpenDART에서 받은 네 계정 값을 사용해, FD_26 `.env`의 `SUPABASE_URL`과 `SUPABASE_PUBLISHABLE_KEY`를 읽고 `supabase-py`로 `financials`에 upsert하는 짧은 Python 코드를 만들어줘. 비밀값을 출력하지 말고, `code`와 `year`를 충돌 기준으로 써서 재실행해도 안전하게 해줘. 코드를 노트북 `FD-04-900`의 해당 셀에 붙여 실행할 수 있게 보여줘.”

이 코드를 [[FD-04-600__cloud-supabase|§600]]에서 실행하면 OpenDART API 응답에서 Supabase까지 가는 재현 가능한 코드가 남는다. 자연어 SQL과 Python SDK는 서로 다른 자료 예제가 아니라, 같은 `financials` 행을 다루는 두 작업 방식이다.

---

## 🔖 핵심 요약

> [!summary] 🏆 이 노트를 마쳤다면?
>
> - [ ] 개인 Supabase 프로젝트의 URL·publishable key를 FD_26 `.env`에 저장한다.
> - [ ] 프로젝트 범위를 지정해 Supabase MCP를 OAuth로 연결한다.
> - [ ] 자연어 요청으로 표 생성·INSERT·SELECT를 수행하고 SQL을 확인한다.
> - [ ] `financials`에 anon SELECT·INSERT·UPDATE RLS 정책을 추가하고, `true` 정책의 접근 범위를 이해한다.
> - [ ] 같은 행을 SDK 코드로 다시 적재해 실행 가능한 경로를 남긴다.
