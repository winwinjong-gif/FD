---
title: "FD-04-410__mcp-agentic-install"
date: 2026-09-18
id: FD-04-410
type: lecture
tags:
  - FD
  - Week04
  - MCP
---

## 💡 왜 MCP를 설치할까?

§300에서는 내가 OpenDART API 주소와 조건을 준비해 재무제표를 받았다. MCP를 연결하면 이번에는 AI 에이전트에게 자연어로 물어보고, 에이전트가 OpenDART 조회 도구를 불러온다.

수집 방법은 달라져도 확인할 숫자는 같다. §300에서 직접 받은 당기순이익 45.2조 원과 비교하면 에이전트가 자료를 제대로 가져왔는지 확인할 수 있다.

---

## 🔌 MCP는 무엇을 연결할까?

MCP는 AI 앱이 바깥의 도구를 부를 때 사용하는 연결 방식이다. `opendart-mcp`는 AI 앱과 OpenDART API 사이에서 요청을 전달한다.

```mermaid
flowchart LR
    S[학생의 자연어 질문] --> A[AI 앱]
    A --> M[OpenDART MCP 도구]
    M --> D[OpenDART 자료]
    D --> M --> A --> S
```

이 연결의 역할은 OpenDART에서 자료를 가져오는 데까지다. 받은 자료를 SQLite나 Supabase에 저장하는 단계는 다음 실습에서 따로 한다.

---

## 🧰 준비물 — `uv`/`uvx`와 인증키

`opendart-mcp`는 `uvx`(uv가 설치하는 실행기)로 매번 새로 받아 실행한다. 설치돼 있는지 먼저 확인한다.

```bash
uv --version
```

버전 번호가 안 나오면 OS에 맞는 공식 설치 명령을 실행한 뒤 터미널을 새로 연다 — §300에서 이미 설치했다면 이 단계는 건너뛴다.

> [!tip]- 🍎 macOS/Linux — `uv` 설치
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```
> 설치 뒤 새 터미널을 열고 `uv --version`으로 확인한다.

> [!tip]- 🪟 Windows(PowerShell) — `uv` 설치
> ```powershell
> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
> ```
> 설치 뒤 PowerShell을 새로 열고 `uv --version`으로 확인한다.

`OPENDART_API_KEY`는 §300에서 이미 `FD_26/.env`에 저장했다. MCP 등록 명령 중 일부는 터미널의 환경변수로도 값을 읽으므로, 아래처럼 현재 셸에도 같은 값을 실어둔다. 두 경우 모두 키 값 자체는 이 문서에 적지 않고, 학생이 자기 값으로 채운다.

> [!tip]- 🍎 macOS/Linux(zsh) — 환경변수로 내보내기
> ```bash
> export OPENDART_API_KEY=$(grep OPENDART_API_KEY .env | cut -d '=' -f2)
> ```
> `FD_26` 루트에서 실행한다. `[ -n "$OPENDART_API_KEY" ] && echo 설정됨`으로 값이 채워졌는지만 확인한다 — 키 값 자체를 출력·캡처·공유하지 않는다.

> [!tip]- 🪟 Windows(PowerShell) — 환경변수로 내보내기
> ```powershell
> $env:OPENDART_API_KEY = (Select-String -Path .env -Pattern "OPENDART_API_KEY=(.*)").Matches.Groups[1].Value
> ```
> `FD_26` 루트에서 실행한다. `if ($env:OPENDART_API_KEY) { "설정됨" }`으로 값이 채워졌는지만 확인한다 — 키 값 자체를 출력·캡처·공유하지 않는다.

> [!warning] ⚠️ 반드시 `mcp<2`로 고정한다
> - `opendart-mcp` 0.1.0은 `from mcp.server.fastmcp import FastMCP`로 임포트하는데, 이 경로는 `mcp` 2.x부터 사라졌다.
> - 그래서 실행 명령은 항상 `uvx --with "mcp<2" opendart-mcp` 형태를 쓴다.
> - `mcp<2`를 빼면 임포트 단계에서 바로 실패한다.

---

## 🗣️ 런타임 등록 — 쓰는 환경 하나만 고른다

학생은 아래 넷 중 **자신이 실제로 쓰는 런타임 하나**만 펼쳐서 따라 한다. 모든 등록은 `FD_26` 프로젝트 범위로 한정하고, 사용자 전체 설정은 건드리지 않는다.

**Claude Code**

```bash
claude mcp add opendart -e OPENDART_API_KEY=$OPENDART_API_KEY -- uvx --with "mcp<2" opendart-mcp
```
`FD_26` 폴더에서 실행하면 그 프로젝트 범위로 등록된다. `claude mcp list`로 `opendart`가 보이면 등록이 끝난 것이다.

> [!tip]- 🪟 Antigravity (`~/.gemini/settings.json`)
> `FD_26/.gemini/settings.json`(없으면 새로 생성)에 아래 블록을 추가한다.
> ```json
> {
>   "mcpServers": {
>     "opendart": {
>       "command": "uvx",
>       "args": ["--with", "mcp<2", "opendart-mcp"],
>       "env": { "OPENDART_API_KEY": "발급받은_인증키" }
>     }
>   }
> }
> ```
> `env`의 값은 실제 키 문자열로 직접 채우고, 이 파일을 커밋하지 않는다.

> [!tip]- 🤖 Codex (`~/.codex/config.toml` 또는 `codex mcp add`)
> 명령 한 줄로 등록한다.
> ```bash
> codex mcp add opendart -- uvx --with "mcp<2" opendart-mcp
> ```
> 또는 `FD_26/.codex/config.toml`에 직접 추가한다.
> ```toml
> [mcp_servers.opendart]
> command = "uvx"
> args = ["--with", "mcp<2", "opendart-mcp"]
> env = { OPENDART_API_KEY = "발급받은_인증키" }
> ```

> [!tip]- 💻 Copilot (`.vscode/mcp.json`)
> `FD_26/.vscode/mcp.json`(없으면 새로 생성)에 추가한다.
> ```json
> {
>   "servers": {
>     "opendart": {
>       "command": "uvx",
>       "args": ["--with", "mcp<2", "opendart-mcp"],
>       "env": { "OPENDART_API_KEY": "발급받은_인증키" }
>     }
>   }
> }
> ```
> VS Code에서 이 파일을 열면 서버 시작 버튼이 뜬다. 시작 후 Copilot Chat의 도구 목록에서 `opendart`가 보이는지 확인한다.

등록이 어렵거나 형식이 안 맞으면, 이 문서를 통째로 자기 에이전트에게 주고 "이 문서대로 설치해줘, 지금 내가 쓰는 환경에 맞게"라고 요청해도 된다 — 위 넷은 그 요청이 결국 만들어낼 결과물이다.

---

## ✅ 연결 결과를 확인한다

등록한 런타임의 대화창에 아래 문장을 보낸다.

```text
삼성전자(corp_code 00126380)의 2025년 사업보고서 연결 재무제표에서 당기순이익을 알려줘.
```

- 도구 목록에 OpenDART 조회 도구(`opendart`)가 나타나는가?
- 답이 §300에서 직접 확인한 당기순이익 **45.2조 원**과 같은가?

둘 다 맞으면 연결이 끝났다. 오류 화면에 키가 나타나면 캡처하거나 공유하지 않는다.

> [!warning] 막히는 세 가지 원인
> - **`uvx`를 못 찾는다**: 위 uv 설치가 끝났는지, 새 터미널을 열었는지 확인한다.
> - **키가 비어 있다는 오류**: `OPENDART_API_KEY`를 환경변수로 내보냈는지, 런타임 설정의 `env` 값이 실제 키로 채워졌는지 확인한다 — `.env` 파일을 읽는 것이 아니라 각 설정이 직접 값을 받는다.
> - **`ImportError: mcp.server.fastmcp`**: 실행 명령에 `--with "mcp<2"`가 빠진 것이다. 위 명령을 그대로 다시 쓴다.

---

## 🔖 핵심 요약

> [!summary] 🏆 이 노트를 마쳤다면?
>
> - [ ] MCP가 AI 앱과 OpenDART 조회 도구를 연결하는 역할임을 설명
> - [ ] 프롬프트를 보내 OpenDART MCP 설치를 요청
> - [ ] 도구 목록과 §300 기준값으로 연결 결과를 확인

이제 [[FD-04-500__load-and-measure|§500]]에서 자연어로 받은 값을 SQLite에 적재하고 재무지표를 계산한다.
