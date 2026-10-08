---
title: "FD-03-500__db-map"
date: 2026-09-09
id: FD-03-500
type: lecture
tags:
  - FD
  - Week03
  - database
---


> [!info] 학습 목표
>
> - 내 PC / 회사 서버 / 클라우드 / 대규모 분석, 각 상황에 어떤 데이터 시스템이 등장하는지 구분한다.
> - SQLite가 실무에서 정확히 어떤 자리를 차지하는지 안다.

---

## 🗺 지도 한 장

지금까지는 노트북 하나, DB 파일 하나로 충분했다. 그런데 이 질문을 던지는 사람이 나 혼자가 아니라 팀 전체이거나, 데이터가 훨씬 커지면 이야기가 달라진다. 상황별로 등장하는 시스템이 다르다.

<figure style="margin:16px 0; background:#FAF7F0; border:1px solid #E2E8F0; border-radius:8px; padding:14px;">
  <svg viewBox="0 0 560 460" style="width:100%; max-height:500px; display:block;">
    <line x1="60" y1="20" x2="60" y2="330" stroke="#64748B" stroke-width="1.5"/>
    <line x1="60" y1="330" x2="530" y2="330" stroke="#64748B" stroke-width="1.5"/>
    <text x="295" y="365" font-size="12" text-anchor="middle" fill="#0F2747">같이 쓰는 사람 수 →</text>
    <text x="30" y="180" font-size="12" text-anchor="middle" fill="#0F2747" transform="rotate(-90 30 180)">데이터 크기 →</text>

    <rect x="80" y="255" width="120" height="65" rx="6" fill="#A7F3D0" stroke="#16A34A"/>
    <text x="140" y="273" font-size="12" text-anchor="middle" fill="#0F2747" font-weight="700">SQLite</text>
    <text x="140" y="288" font-size="9.5" text-anchor="middle" fill="#0F2747">지금 우리가 있는 자리</text>
    <text x="140" y="302" font-size="9" text-anchor="middle" fill="#166534" font-style="italic">언제: 혼자 분석, 파일 하나로 충분할 때</text>

    <rect x="230" y="190" width="140" height="60" rx="6" fill="#E3F2FD" stroke="#0F2747"/>
    <text x="300" y="208" font-size="12" text-anchor="middle" fill="#0F2747" font-weight="700">PostgreSQL·MySQL</text>
    <text x="300" y="223" font-size="9.5" text-anchor="middle" fill="#0F2747">회사 서버</text>
    <text x="300" y="238" font-size="9" text-anchor="middle" fill="#1E3A8A" font-style="italic">언제: 팀이 같이 쓰는 서비스 DB</text>

    <rect x="330" y="82" width="150" height="63" rx="6" fill="#FCD34D" fill-opacity="0.5" stroke="#D97706"/>
    <text x="405" y="100" font-size="12" text-anchor="middle" fill="#0F2747" font-weight="700">Supabase 등</text>
    <text x="405" y="115" font-size="9.5" text-anchor="middle" fill="#0F2747">클라우드 운영</text>
    <text x="405" y="130" font-size="9" text-anchor="middle" fill="#92400E" font-style="italic">언제: 클라우드에서 여럿이 조회·공유</text>

    <rect x="360" y="22" width="150" height="53" rx="6" fill="#FEF2F2" stroke="#DC2626"/>
    <text x="435" y="40" font-size="12" text-anchor="middle" fill="#0F2747" font-weight="700">BigQuery 등</text>
    <text x="435" y="55" font-size="9.5" text-anchor="middle" fill="#0F2747">매우 큰 분석</text>
    <text x="435" y="68" font-size="9" text-anchor="middle" fill="#991B1B" font-style="italic">언제: 수억 행 넘는 대규모 집계</text>

    <path d="M200 275 C 260 250, 320 140, 340 118" stroke="#0F2747" stroke-width="2" stroke-dasharray="4,3" fill="none" marker-end="url(#arrowDB)"/>
    <defs>
      <marker id="arrowDB" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
        <path d="M0,0 L8,4 L0,8 Z" fill="#0F2747"/>
      </marker>
    </defs>

    <rect x="70" y="350" width="470" height="98" rx="8" fill="#FFFFFF" stroke="#16A34A" stroke-width="1.5"/>
    <text x="90" y="372" font-size="12" font-weight="700" fill="#0F2747">📌 SQLite의 자리를 정확히</text>
    <text x="90" y="393" font-size="10.5" fill="#0F2747">🗄️ 파이프라인의 중심 저장소가 아니라 <tspan font-weight="700">개인 분석용 캐시</tspan>다.</text>
    <text x="90" y="411" font-size="10.5" fill="#0F2747">🔒 여러 명이 동시에 쓰면 파일이 <tspan font-weight="700">통째로 잠긴다</tspan> — 한 명이 쓰는 동안 다른 사람은 기다린다.</text>
    <text x="90" y="429" font-size="10.5" fill="#0F2747">👁 분석가가 받는 DB 계정은 실무에서도 대부분 <tspan font-weight="700">읽기 전용</tspan>이다 — 수업이라서가 아니다.</text>
  </svg>
  <figcaption style="font-size:11.5px; color:#64748B; margin-top:6px; text-align:center;">
    <em>왼쪽 아래(SQLite)에서 오른쪽 위로 갈수록 같이 쓰는 사람과 데이터 크기가 늘어난다. 점선 화살표는 다음 노트가 다루는 SQLite → Supabase 이동이다. 아래 카드는 SQLite 칸에 대한 실무 주의사항이다.</em>
  </figcaption>
</figure>

전달할 메시지는 한 가지뿐이다 — **회사는 이 중 하나만 골라 쓰지 않는다.** 목적·규모·사용자 수·업무에 따라 여러 시스템을 함께 쓰는 것이 보통이다. 지금 이 표를 왜, 어떻게 나누는지(OLTP/OLAP 같은 이름)는 여기서 다루지 않는다 — 상황별로 무엇이 등장하는지 감을 잡는 것으로 충분하다.

"회사도 이렇게 SQLite로 운영한다"고 오해한 채로 나가면, 나중에 다시 배워야 한다 — 위 카드 세 줄이 그 오해를 미리 막아둔 것이다.

## 🎬 참고영상 (선택)

> [!tip]- 데이터베이스 선택 가이드
> [데이터베이스 선택 가이드](https://youtu.be/GxhMuz7N6T4) — 오늘 다룬 네 칸 말고도 더 많은 선택지가 있다. 영상 전체를 다시 설명하지는 않으니, 궁금하면 개별적으로 시청한다.

실습에서는 별도 코드가 없다 — 다음 노트에서 SQLite와 클라우드 DB 사이의 타입 경계를 직접 코드로 확인한다. 같은 쿼리를 클라우드에서 그대로 재실행하는 것은 클라우드 프로젝트·테이블·읽기 전용 계정이 아직 준비되지 않아 이후 별도 실습으로 미뤄둔다.

---

## 🔖 핵심 요약

> [!summary] 🏆 이 노트를 마쳤다면?
>
> - [ ] 내 PC·회사 서버·클라우드·대규모 분석 각각에 어떤 시스템이 등장하는지 구분할 수 있다.
> - [ ] "회사는 하나만 쓰지 않는다"는 원칙을 설명할 수 있다.
> - [ ] SQLite가 실무에서 개인 분석 캐시라는 것과, 분석가 계정이 대체로 읽기 전용이라는 것을 안다.
