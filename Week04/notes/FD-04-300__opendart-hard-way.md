---
title: "FD-04-300__opendart-hard-way"
date: 2026-09-17
id: FD-04-300
type: lecture
tags:
  - FD
  - Week04
  - OpenDART
---

## 🏛️ DART, 그리고 전통적인 방식의 번거로움

> [!info] 학습 목표
>
> - DART와 OpenDART가 무엇인지 설명한다.
> - 인증키를 신청하고 환경변수로 관리하는 과정을 실제로 따라 한다.
> - `requests`로 OpenDART에 GET 요청을 보내 재무제표 JSON을 직접 받아본다.

---

## 🏛️ DART가 뭔가요?

상장기업은 재무제표·사업보고서 같은 공시 자료를 법에 따라 공개해야 한다. 이 자료가 모이는 곳이 금융감독원의 전자공시시스템, **DART(Data Analysis, Retrieval and Transfer System)**다. 사람이 브라우저로 읽는 DART 화면과 별도로, 같은 데이터를 프로그램이 가져갈 수 있게 열어둔 것이 **[OpenDART](https://opendart.fss.or.kr/) API**다.

[[FD-04-200__api-and-http|§200]]에서 "URL에 조건을 붙여 보내면 데이터가 온다"고 했던 그 방식 그대로다. 이제 실제로 인증키를 받아 첫 요청을 보내본다.

---

## 🔑 인증키 신청 — 5단계

> [!warning] 🏠 수업 전 과제
> - OpenDART 회원가입과 인증키 신청(이메일 인증 포함)은 수업 시작 **전에** 미리 끝내 온다 — 이메일 인증이 늦어지면 실습 시간에 키를 못 받아 이후 단계를 하나도 진행할 수 없다.
> - 발급받은 키는 아래 절차대로 `.env`에 미리 저장해 온다.
> - 아직 준비하지 않았다면 아래 ‘실습 환경 준비’ 순서대로 설치한다. 이미 `pyproject.toml`에 등록돼 있으면 다시 추가하지 않는다.

OpenDART는 아무나 바로 부를 수 없다. 먼저 인증키(API key)를 신청해야 한다.

#### 🛠️ 실습 환경 준비 — 처음 하는 학생은 위에서부터 따라 하기

1. **VS Code에서 폴더 열기**: `File → Open Folder`를 누르고 `FD_26` 폴더를 연다. 왼쪽 파일 목록 맨 위에 `pyproject.toml`이 보여야 프로젝트 루트가 맞다.
2. **터미널 열기**: 위쪽 메뉴에서 `Terminal → New Terminal`을 누른다. 터미널은 명령을 입력하는 창이다. 프롬프트에 `FD_26` 폴더가 표시되는지 확인한다.
3. **`uv`와 패키지 준비**: `uv --version`을 실행한다. 버전 번호가 나오면 아래 명령을 한 번 실행한다.
   ```bash
   uv add pandas requests python-dotenv supabase
   ```
   `uv`를 찾을 수 없다는 안내가 나오면 공식 설치 방법을 사용한다. macOS/Linux는 아래 첫 번째 명령, Windows PowerShell은 두 번째 명령을 실행하고 터미널을 닫았다 다시 열어 `uv --version`을 확인한다. [uv 공식 설치 안내](https://docs.astral.sh/uv/getting-started/installation/)
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   ```powershell
   # Windows PowerShell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
4. **노트북 열기와 커널 선택**: Week04 폴더 안의 실습 노트북을 열고 오른쪽 위 `Select Kernel`에서 `FD_26/.venv`를 고른다. 실행 셀에서 파이썬 경로 끝에 `FD_26/.venv`가 보이면 준비가 된 것이다.

> [!tip] 폴더 위치가 헷갈리면
> - `pyproject.toml`은 `uv add`를 실행할 프로젝트의 표지판이다.
> - 터미널에서 파일이 보이지 않으면 VS Code로 `FD_26` 폴더를 다시 열고 새 터미널을 만든다.
> - 폴더를 확인할 때는 macOS/Linux에서 `pwd`, Windows PowerShell에서 `Get-Location`을 쓴다.

![[FD-04-300-dart-01-home.png]]
- OpenDART 메인 화면(`opendart.fss.or.kr`)이다.
- 상단 메뉴에서 **인증키 신청/관리**를 클릭하는 것부터 시작한다.

![[FD-04-300-dart-02-key-menu.png]]
- 인증키 관리로 넘어가는 화면이다.
- 기존 계정이 있으면 로그인하고, 없으면 상단의 **인증키 신청** 메뉴로 이동한다.

![[FD-04-300-dart-03-signup.png]]
- 회원가입 화면이다.
- 약관을 확인한 뒤 계정을 만들어야 인증키를 신청할 수 있다.

![[FD-04-300-dart-04-login-required.png]]
- 인증키 관리 페이지는 로그인이 필요하다.
- 계정을 만든 뒤 이 화면에서 로그인해 인증키를 발급받는다.

![[FD-04-300-dart-05-usage-guide.png]]
- 개발가이드 화면 — **공시정보 > 단일회사 주요계정** 항목이다.
- 여기서 API가 요구하는 요청 경로와 필수 파라미터(`corp_code`, `bsns_year`, `reprt_code` 등)를 확인한다. 다음 단계에서 이 파라미터들이 왜 번거로운지 직접 느껴본다.

> [!warning] ⚠️ 인증키는 코드에 직접 적지 않는다
> - 발급받은 키는 `.env` 같은 환경변수 파일에 넣고, 코드에서는 `os.environ`으로만 읽는다.
> - 이 파일은 절대 커밋하지 않는다 — `.gitignore`에 이미 등록돼 있어야 한다.

---

## 🗂️ 발급받은 키를 `.env` 파일에 담기

발급받은 인증키를 코드에 직접 적지 않으려면, 키를 담을 파일이 먼저 있어야 한다.

- **위치**: `FD_26` 프로젝트 루트(`pyproject.toml`이 있는 바로 그 폴더).
- **파일명**: `.env` — 점(`.`)으로 시작하고 확장자는 없다.
- **내용**: 한 줄, `키이름=값` 형식.
  ```bash
  # .env
  OPENDART_API_KEY=발급받은_인증키_여기에_붙여넣기
  ```
- **VS Code에서 만들기**: 왼쪽 탐색기에서 `FD_26` 루트 폴더를 선택하고 새 파일(New File) 아이콘을 눌러 파일명에 `.env`를 그대로 입력한다.

> [!warning] ⚠️ Windows 탐색기의 `.txt` 함정
> - 파일 탐색기에서 새 텍스트 파일을 만들면 "파일 이름 및 확장자 표시"가 꺼져 있을 때 `.env`가 실제로는 `.env.txt`로 저장된다.
> - VS Code 안에서 직접 파일을 만들면 이 함정을 피한다. 탐색기로 만들었다면 "파일 이름 확장자" 보기를 켜서 실제 이름이 `.env`인지(`.env.txt`가 아닌지) 확인한다.

> [!tip] 💬 export는 필요 없다
> - 노트북(`load_dotenv()`)은 `.env` 파일에서 직접 읽으니 터미널에서 `export`를 따로 실행할 필요가 없다.

---

## 😮‍💨 파라미터의 key/value, 이걸 다 알아야 한다

인증키를 받았다고 바로 끝이 아니다. OpenDART가 요구하는 파라미터를 정확한 이름(key)과 정확한 값(value)으로 채워야 응답이 온다.

- **`crtfc_key`** — 방금 발급받은 인증키.
- **`corp_code`** — 종목코드(`005930`)가 아니라 DART 전용 8자리 고유번호다. 삼성전자는 `00126380`이다. 이 매핑표를 따로 구해야 한다.
- **`bsns_year`** — 사업연도, 예: `2025`.
- **`reprt_code`** — 보고서 종류 코드. 사업보고서는 `11011`이다. 이 다섯 자리 숫자를 외워야 쓸 수 있다.

이름이 틀리거나 하나라도 빠지면 원하는 데이터 대신 오류 메시지가 온다. `corp_code`는 실습 파일 `practice/data/corp_codes_12.csv`에서도 확인할 수 있다. **바로 이 ‘정확한 이름과 값을 알아야 하는 번거로움’이 뒤에서 만날 MCP의 존재 이유다.**

#### 🎯 고통 ①~④ — 지금부터 순서대로 만난다

이제부터 네 가지를 순서대로 겪는다: **① 조립**(주소+파라미터) · **② 찾기**(30여 행 중 원하는 두 줄) · **③ 쉼표**(문자열을 숫자로) · **④ 단위**(원→억원). [[FD-04-400__mcp-natural-language|§400]]에서는 이 네 칸의 왼쪽에 "서버가 대신함 ✓"이 붙는다.

<figure style="margin:16px 0; background:#FAF7F0; border:1px solid #E2E8F0; border-radius:8px; padding:12px;">
  <svg viewBox="0 0 560 220" style="width:100%; max-height:260px; display:block;">
    <rect x="8" y="10" width="70" height="200" fill="none" stroke="#CBD5E1" stroke-width="1.5" stroke-dasharray="4,3" rx="4"/>
    <text x="43" y="115" fill="#94A3B8" font-size="9" text-anchor="middle" transform="rotate(-90 43 115)">§400에서 ✓</text>
    <rect x="90" y="10" width="150" height="44" fill="#0F2747" fill-opacity="0.9" rx="4"/>
    <text x="165" y="37" fill="#fff" font-size="12" text-anchor="middle">① 조립</text>
    <text x="440" y="37" fill="#64748B" font-size="10" text-anchor="middle">…&amp;corp_code=00126380&amp;bsns_year=2025…</text>
    <rect x="90" y="64" width="150" height="44" fill="#0E7C7B" fill-opacity="0.9" rx="4"/>
    <text x="165" y="91" fill="#fff" font-size="12" text-anchor="middle">② 찾기</text>
    <text x="440" y="91" fill="#DC2626" font-size="10" text-anchor="middle">Empty DataFrame</text>
    <rect x="90" y="118" width="150" height="44" fill="#D97706" fill-opacity="0.9" rx="4"/>
    <text x="165" y="145" fill="#fff" font-size="12" text-anchor="middle">③ 쉼표</text>
    <text x="440" y="145" fill="#DC2626" font-size="10" text-anchor="middle">TypeError</text>
    <rect x="90" y="172" width="150" height="44" fill="#16A34A" fill-opacity="0.9" rx="4"/>
    <text x="165" y="199" fill="#fff" font-size="12" text-anchor="middle">④ 단위</text>
    <text x="440" y="199" fill="#64748B" font-size="10" text-anchor="middle">45206805000000 → 452068</text>
  </svg>
  <figcaption style="font-size:11.5px; color:#64748B; margin-top:6px; text-align:center;">
    <em>고통 ①~④가 화면에 남기는 흔적. 왼쪽 여백은 §400에서 "MCP 서버가 대신함 ✓"이 채운다.</em>
  </figcaption>
</figure>

> [!tip]- 그림 읽는 법 — 네 칸이 실제 코드에서 어떻게 나타나는가
> 그림의 네 칸은 추상적인 작업 목록이 아니라, 바로 다음 실습에서 작성할 코드의 네 단계다.
>
> - **① 조립 — 요청 주소와 파라미터를 맞춰 넣기**
>   - 인증키를 브라우저 주소창에 넣지 않는다. 주소창 기록이나 공유 화면에 키가 남을 수 있다.
>   - 코드는 주소와 파라미터를 따로 적고, 키는 `.env`에서 읽어 요청에 담는다.
>     ```python
>     url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
>     params = {
>         "crtfc_key": key,
>         "corp_code": "00126380",  # 삼성전자 DART 고유번호
>         "bsns_year": "2025",
>         "reprt_code": "11011",    # 사업보고서
>     }
>     requests.get(url, params=params)
>     ```
>   - `corp_code`를 종목코드 `005930`으로 쓰거나 `reprt_code`를 빠뜨리면 원하는 응답이 오지 않는다.
>
> - **② 찾기 — 30여 행 중 연결 기준 두 줄 고르기**
>   - 응답에는 여러 계정과 기준이 섞여 있다.
>     ```text
>     fs_div   account_nm          thstrm_amount
>     CFS      당기순이익(손실)       45,206,805,000,000
>     OFS      당기순이익(손실)       ...
>     CFS      자본총계              436,320,300,000,000
>     OFS      자본총계              ...
>     ```
>   - 계정명뿐 아니라 연결 기준인 `CFS`도 확인해야 한다.
>     ```python
>     if row["fs_div"] == "CFS" and row["account_nm"] in targets:
>         targets[row["account_nm"]] = row["thstrm_amount"]
>     ```
>   - 계정명을 잘못 쓰거나 `CFS` 조건을 빼면 `Empty DataFrame`이 나오거나 별도 기준 값을 고를 수 있다.
>
> - **③ 쉼표 — 문자열을 계산 가능한 숫자로 바꾸기**
>   - API의 금액은 숫자처럼 보이지만 실제로는 문자열이다.
>     ```python
>     amount = "45,206,805,000,000"
>     amount = int(amount.replace(",", ""))
>     ```
>   - 쉼표를 제거하지 않고 계산하면 `TypeError`나 `ValueError`가 발생할 수 있다.
>
> - **④ 단위 — 원을 억원으로 바꾸기**
>   - 숫자로 바꾼 뒤에도 값은 원 단위다.
>     ```python
>     amount = 45_206_805_000_000
>     amount_eok = amount / 100_000_000
>     print(f"{amount_eok:,.0f}억원")
>     # 452,068억원
>     ```
>   - `45206805000000 → 452068`은 숫자를 줄이는 것이 아니라 `100,000,000`으로 나눠 원을 억원으로 바꾸는 과정이다.
>
> **한 줄로 연결하면:** 주소를 조립하고 → 원하는 행을 찾고 → 문자열을 숫자로 바꾸고 → 원을 억원으로 바꾼다. §400에서는 MCP 서버가 이 네 단계를 대신 처리한다.


---

## 🧪 첫 요청 — 삼성전자 재무제표 받아보기

파라미터를 다 채우면 `requests`로 GET 요청 하나만 보내면 된다. 노트북을 `FD_26/.venv` 커널로 실행하면 셀에서 `requests`와 `.env`를 사용할 수 있다. 인증키를 브라우저 주소창에 붙여 넣지 않는다.

`requests`는 파이썬에서 HTTP 요청을 보내는 라이브러리, `load_dotenv()`는 `.env` 파일의 값을 환경변수로 읽어오는 함수다 — 둘 다 앞서 `uv add`로 이미 설치해뒀다.

**§300-1**
```python
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("OPENDART_API_KEY")
url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json"
params = {"crtfc_key": key, "corp_code": "00126380", "bsns_year": "2025", "reprt_code": "11011"}
data = None
source = "live"

# happy path: 키가 있으면 같은 GET 요청을 그대로 보낸다.
if key:
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        print("🔴 OpenDART에 연결하지 못했다. 네트워크와 API 주소를 확인한다. (요청 주소는 안전을 위해 숨김)")
    else:
        if data.get("status") != "000":
            print("🔴 OpenDART 응답:", data.get("status"), data.get("message"))
            data = None
else:
    print("🔴 .env에서 OPENDART_API_KEY를 못 찾았다 — FD_26 루트와 파일명을 확인한다.")

# 방어 경로: 키·네트워크·응답에 문제가 있으면 저장된 fixture로 계속한다.
if data is None:
    with open("data/fnlttSinglAcnt_samsung_2025.json", encoding="utf-8") as f:
        data = json.load(f)
    source = "fixture"

print(f"[{source}]", data["status"], data["list"][0]["account_nm"], data["list"][0]["thstrm_amount"])
# 예상 출력([live] = 실제 API 호출 성공): [live] 000 유동자산 247,684,612,000,000
# 예상 출력([fixture] = 저장된 예시, API 호출 성공 아님): [fixture] 000 유동자산 247,684,612,000,000
```

`status`가 `"000"`이면 정상 응답이다. 첫 줄 계정은 `유동자산`, 2025년 12월 말 기준 247조 6,846억 원이다. 코드는 키가 없거나 응답이 비정상이면 스스로 저장된 fixture로 넘어가므로, 인증키를 아직 못 받았어도 이 셀에서 막히지 않는다.

> [!tip]- `[fixture]`가 뜨면
> - 내 키가 아직 정상 작동한 게 아니라는 뜻이다 — `[live]`가 뜰 때까지는 §410의 검증 질문도 같은 문제를 겪는다.
> - 위에서 브라우저로 본 것과 요청 파라미터·응답이 모두 같은 JSON이다.

## 🎯 여러 행 중에서 진짜 필요한 두 숫자만 골라내기

방금 받은 응답에는 계정 하나만 있는 게 아니다. `data["list"]`에는 재무상태표·손익계산서의 여러 계정이, 그것도 **별도(OFS)**와 **연결(CFS)** 두 기준으로 섞여서 들어 있다. 지금 필요한 건 그중 **연결 기준 당기순이익**과 **자본총계** 두 줄뿐이다 — 이 두 값을 뒤에서 [[FD-04-410__mcp-agentic-install|§410]]·[[FD-04-500__load-and-measure|§500]]이 기준값으로 그대로 쓴다.

**주의**: 계정명은 `당기순이익(손실)`로 정확히 일치해야 걸린다 — 괄호까지 포함한 문자열이다.

**§300-2**
```python
# §FD-04-300-2
print("전체 응답 행 수:", len(data["list"]))
# [출력 미검증 — 환경 필요] 계정과목 × 기준(별도/연결) 조합만큼 여러 행이 나온다

targets = {"당기순이익(손실)": None, "자본총계": None}
for row in data["list"]:
    if row["fs_div"] == "CFS" and row["account_nm"] in targets:
        targets[row["account_nm"]] = int(row["thstrm_amount"].replace(",", ""))

net_income_eok = targets["당기순이익(손실)"] / 1e8  # 원 → 억원
equity_eok = targets["자본총계"] / 1e8

print(f"연결 당기순이익: {net_income_eok:,.0f}억원 ({net_income_eok/1e4:.1f}조원)")
print(f"연결 자본총계: {equity_eok:,.0f}억원 ({equity_eok/1e4:.1f}조원)")
# 예상 출력: 연결 당기순이익: 452,068억원 (45.2조원)
# 예상 출력: 연결 자본총계: 4,363,203억원 (436.3조원)
```
- `fs_div`가 `"CFS"`(연결)인 행만 골라야 한다 — 같은 계정명이 `"OFS"`(별도) 기준으로도 따로 들어 있어서, 기준을 안 걸러내면 다른 값을 집게 된다.
- `thstrm_amount`는 콤마가 섞인 **원** 단위 문자열이라 콤마를 지우고 정수로 바꾼 뒤 `1e8`로 나눠야 억원이 된다.

이 두 값(45.2조원·436.3조원)이 이번 주 내내 따라다니는 **기준값**이다. 인증키 발급, 환경변수 등록, 파라미터 이름 암기, 그리고 30여 개 행 중 원하는 두 줄 골라내기까지 — 이 한 번의 요청을 위해 여러 단계를 거쳤다. 같은 회사·연도를 **반복** 조회해야 한다면 이 코드를 함수로 묶어 다시 부르면 된다 — 번거로운 건 매번 새 회사·연도를 **처음** 찾아 조립하는 과정이다. [[FD-04-400__mcp-natural-language|§400]]에서 만날 MCP·자연어는 이 반복을 대신해주는 것이 아니라, 바로 이 "처음 찾고 조립하는" 탐색·검증 과정을 대신해준다.

---

## 🔖 핵심 요약

> [!summary] 🏆 이 노트를 마쳤다면?
>
> - [ ] DART와 OpenDART의 관계를 설명할 수 있다.
> - [ ] 인증키를 신청하고 환경변수로 안전하게 관리할 수 있다.
> - [ ] `corp_code`·`bsns_year`·`reprt_code` 같은 파라미터가 왜 번거로운지 설명할 수 있다.
> - [ ] 응답의 여러 행 중 연결(CFS) 기준 당기순이익·자본총계를 골라내 억원 단위로 변환할 수 있다.
> - [ ] 실습에서: `requests`로 OpenDART에 직접 GET 요청을 보내 삼성전자 재무제표를 받아본다.
