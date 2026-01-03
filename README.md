# 🏢 노티가드 그룹웨어 (NotiGuard Groupware)

> 효성전기 그룹웨어 공지/팝업 알림 + 요약 기능 - Streamlit MVP  
> Hyosung Electric Groupware Notice/Popup + Summary - Streamlit MVP

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)

> **🌐 Production URL**: (TBD)  
> ※ 현재 저장소 기준은 로컬/내부망 실행을 기본으로 합니다.

---

## 📋 프로젝트 개요 (Project Overview)

노티가드 그룹웨어는 **직원 공지 열람률 저하**와 **중요 공지 확인 지연** 문제를 해결하기 위한 사내 MVP입니다.  
관리자는 공지를 등록하고, **중요 공지(팝업)**는 대상(본부/팀)에게 강제 노출되며 직원은 **확인/나중/요약/챗봇 이동**으로 처리합니다.  
또한 공지는 **POTENS.ai API 기반 요약**을 제공하여 직원이 빠르게 핵심을 파악할 수 있도록 돕습니다.

NotiGuard Groupware is an internal MVP designed to improve **notice readership** and **timeliness**.  
Admins register notices and send **important popup notices** to specific targets (department/team). Employees can handle popups via confirm/ignore/summary/chatbot actions. Notice summaries are generated using **POTENS.ai API**.

---

## ✨ 주요 기능 (Key Features)

### 🧑‍💼 관리자 (Admin)
- 📝 **공지 등록/조회**: 일반공지/중요공지 등록, 게시판 리스트/상세 확인
- 🎯 **중요공지 발송 대상 선택**: 본부/팀 단위 선택 및 예약 전송 시간 설정(오전 10시/오후 2시)
- 📎 **첨부파일 업로드**: 이미지/파일 업로드 및 다운로드 제공 (DB 메타 저장 + 디스크 저장)

### 👩‍💻 직원 (Employee)
- 📌 **중요공지 팝업 수신**: 5초 주기로 최신 중요공지 조회 → 미응답 팝업 자동 노출
- ✅ **팝업 처리**:  
  1) 확인함(2차 확인 포함) / 2) 나중에 확인(남은 횟수 차감) / 3) 요약 보기 / 4) 챗봇 이동 로그 기록
- 🧾 **공지 요약**: POTENS.ai로 공지 핵심을 5줄 내 요약 + 해야 할 일 정리
- 🖼️ **팝업 내 이미지 표시**: 공지 첨부 이미지가 있으면 팝업 본문에 함께 렌더링

### 🔐 로그인/권한
- 🔑 **accounts 기반 로그인**: ADMIN / EMPLOYEE 역할 분리
- 🚫 권한 체크 후 페이지 접근 제어 (`st.switch_page`)

---

## 🛠️ 기술 스택 (Tech Stack)

| 카테고리 (Category) | 기술 (Technology) | 비고 (Notes) |
|---|---|---|
| **Language** | Python | 3.10+ |
| **Frontend** | Streamlit | Pages 구조 + `st.dialog` |
| **Database** | SQLite | `groupware.db` |
| **AI Summary** | POTENS.ai API | 공지 요약 |
| **Libraries** | requests, python-dotenv | API/환경변수 |

---

## 📁 프로젝트 구조 (Project Structure)

> ✅ 현재 실제 구조 기준 (POPUP_SERVICE-MAIN)

```text
POPUP_SERVICE-MAIN/
├── app.py                      # 앱 엔트리포인트 (무조건 로그인 페이지로 시작)
├── service.py                  # 비즈니스 로직 (공지/팝업/로그/첨부/로그인)
├── groupware.db                # SQLite DB 파일
├── requirements.txt            # 의존성 목록
├── README.md                   # 이 문서
├── README2.md                  # (옵션) 이전/임시 문서
├── 작동순서.txt                # (옵션) 실행/동작 흐름 메모
├── assets/
│   ├── chatimg_r.png
│   └── chatimg.png
├── core/
│   ├── auth.py                 # 비밀번호 검증 (verify_password)
│   ├── db.py                   # DB 연결/초기화 (get_conn, init_db)
│   ├── layout.py               # 공통 UI/테마/사이드바/탑바
│   └── summary.py              # POTENS 요약 모듈 (summarize_notice)
├── pages/
│   ├── 0_Login.py              # 로그인 모달 페이지 (st.dialog)
│   ├── admin.py                # 관리자 화면 (공지 리스트/상세/글쓰기/대상선택)
│   └── employee.py             # 직원 화면 (팝업 수신/요약/게시판)
├── sql/
│   └── schema.sql              # DB 스키마 (notices, popups, logs, accounts, files)
└── uploads/                    # 첨부 저장 디렉터리 (공지 등록 시 파일 저장)
    └── {postid}_{timestamp}_{filename}
```

---

## 🚀 설치 및 실행 (Installation & Execution)

### 1. 사전 요구사항 (Prerequisites)
- Python 3.10+
- pip

### 2. 프로젝트 클론 (Clone Project)
```bash
git clone https://github.com/hansol418/Popup_Service.git
cd POPUP_SERVICE-MAIN
```

### 3. 가상환경 생성 및 활성화 (Create & Activate Virtual Environment)
```bash
python -m venv venv

# Mac/Linux
source venv/bin/activate

# Windows
# venv\Scripts\activate
```

### 4. 필요 라이브러리 설치 (Install Dependencies)
```bash
pip install -r requirements.txt
```

### 5. 환경 변수 설정 (Environment Configuration)

`.env` 파일을 프로젝트 루트에 생성하고 POTENS 정보를 입력합니다.

```env
POTENS_API_KEY=your_actual_api_key_here
POTENS_API_URL=https://ai.potens.ai/api/chat
RESPONSE_TIMEOUT=30
```

> ⚠️ `POTENS_API_KEY`가 없으면 요약 기능에서 RuntimeError가 발생합니다.

### 6. 애플리케이션 실행 (Run Application)
```bash
streamlit run app.py
```

---

## 📖 사용 방법 (Usage Guide)

### 🔐 로그인 (Login)
- 앱 실행 시 `app.py`가 항상 `pages/0_Login.py`로 이동합니다.
- 로그인 성공 시 role에 따라 페이지가 분기됩니다.
  - ADMIN → `pages/admin.py`
  - EMPLOYEE → `pages/employee.py`

### 🧑‍💼 관리자 모드 (Admin Mode)
1. 좌측 사이드바에서 **게시판 / 글쓰기** 메뉴 사용
2. **글쓰기**
   - 공지 유형(중요/일반), 제목, 내용 입력
   - 첨부파일 업로드 가능 (이미지/파일)
3. **중요 공지 등록 시**
   - 대상 선택 모달이 열림 (본부/팀 선택 + 예약시간 선택)
   - “선택한 대상에게 팝업 발송” 시 popups 테이블에 등록

### 👩‍💻 직원 모드 (Employee Mode)
1. 홈 화면에서 **5초마다 중요공지(팝업) 조회**
2. 중요 공지가 도착하면 `st.dialog` 팝업 자동 노출
3. 팝업에서 처리 방식 선택:
   - **1. 확인함**: 2차 확인 후 확인 처리 로그 기록
   - **2. 나중에 확인**: ignore_remaining 차감 확인 + 로그 기록
   - **3. 요약 보기**: POTENS 요약 모달 표시(중첩 dialog 방지 구조)
   - **4. 챗봇으로 바로가기**: 외부 챗봇 링크 새 탭 열기 + 이동 로그 기록

---

## 🗄️ 데이터베이스 스키마 (Database Schema)

> `sql/schema.sql` 기준 (SQLite)

### notices (공지 게시글)
| 컬럼 | 타입 | 설명 |
|---|---|---|
| post_id | INTEGER (PK) | 공지 ID |
| created_at | INTEGER | epoch ms |
| type | TEXT | '중요' / '일반' |
| title | TEXT | 제목 |
| content | TEXT | 내용 |
| author | TEXT | 작성자 |
| views | INTEGER | 조회수 |

### popups (중요공지 팝업)
| 컬럼 | 타입 | 설명 |
|---|---|---|
| popup_id | INTEGER (PK) | 팝업 ID (post_id와 동일 사용) |
| post_id | INTEGER (FK) | notices 참조 |
| target_departments | TEXT | CSV(본부 목록) |
| target_teams | TEXT | CSV(팀 목록) |
| expected_send_time | TEXT | '오전 10시' / '오후 2시' |
| created_at | INTEGER | 생성 시각 |

### employees (직원)
| 컬럼 | 타입 | 설명 |
|---|---|---|
| employee_id | TEXT (PK) | 사번 |
| name | TEXT | 이름 |
| department | TEXT | 본부 |
| team | TEXT | 팀 |
| ignore_remaining | INTEGER | 나중에 확인 가능 횟수 |

### popup_logs (팝업 처리 로그)
| 컬럼 | 타입 | 설명 |
|---|---|---|
| id | INTEGER (PK) | 로그 ID |
| employee_id | TEXT | 직원 |
| popup_id | INTEGER | 팝업 |
| action | TEXT | '확인함'/'확인하지 않음'/'챗봇이동' |
| confirmed | TEXT | 2차확인 값 등 |

### accounts (로그인 계정)
| 컬럼 | 타입 | 설명 |
|---|---|---|
| login_id | TEXT (PK) | 로그인 ID |
| password_hash | TEXT | 해시 비밀번호 |
| role | TEXT | 'ADMIN'/'EMPLOYEE' |
| employee_id | TEXT | 직원 계정 연결 (ADMIN은 NULL) |

### notice_files (첨부파일)
| 컬럼 | 타입 | 설명 |
|---|---|---|
| file_id | INTEGER (PK) | 파일 ID |
| post_id | INTEGER (FK) | 공지 연결 |
| filename | TEXT | 원본 파일명 |
| mime_type | TEXT | MIME |
| file_path | TEXT | uploads 경로 |
| file_size | INTEGER | 파일 크기 |
| uploaded_at | INTEGER | 업로드 시각 |

---

## 🤖 공지 요약 (POTENS.ai Summary)

`core/summary.py`에서 공지 요약 프롬프트를 생성하고 POTENS API로 요청합니다.

- 요약 규칙:
  - 5줄 이내 핵심 요약
  - 일정/마감/대상/필수 행동이 있으면 마지막에 “해야 할 일”로 정리
  - 문의/내선 등 단순 연락 문구는 제외
  - 첨부 이미지가 본문과 연관되면 관련 내용도 포함

---

## 🧪 테스트 (Testing)

### 1) 관리자 테스트 시나리오
- 일반 공지 등록 → 게시판 리스트/상세 확인
- 중요 공지 등록 → 대상 선택 모달 → 팝업 생성 확인
- 첨부 이미지 업로드 → employee 팝업에서 이미지 표시 확인

### 2) 직원 테스트 시나리오
- 홈 화면에서 팝업 자동 노출 확인(5초 polling)
- “확인함” → 로그 기록 + 팝업 닫힘
- “나중에 확인” → ignore_remaining 차감 확인
- “요약 보기” → 요약 모달 단독 오픈(중첩 방지) 확인

---

## 🚢 배포 (Deployment)

현재 저장소는 **로컬/내부망 실행**을 기본으로 합니다.  
배포 환경(Railway, etc.)을 사용할 경우 아래 항목이 필요합니다.

- 환경 변수:
  - `POTENS_API_KEY`
  - `POTENS_API_URL`
  - `RESPONSE_TIMEOUT`
- Streamlit 실행 커맨드:
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

## 🐛 문제 해결 (Troubleshooting)

### 요약 기능 오류
- `POTENS_API_KEY` 미설정 시 RuntimeError 발생  
→ `.env` 또는 배포 환경변수 확인 필요

### 첨부 이미지가 팝업에 안 보임
- 첨부는 `uploads/`에 저장되며 DB에는 file_path로 기록됩니다.
- 파일이 실제로 존재하는지 확인하세요.

### 팝업이 중복으로 열리거나 dialog 오류 발생
- Streamlit은 dialog 중첩이 제한되므로,
  요약 dialog는 **state로 트리거 후 dialog 밖에서 단독 호출** 구조로 구성되어 있습니다.

---

## 👥 Contributors
- **개발 (Development)**: 효성전기 프로젝트 팀
- **기획 (Planning)**: 효성전기 IT팀

---

## 📄 라이선스 (License)
이 프로젝트는 내부 MVP 프로젝트입니다.  
This project is an internal MVP project.

---

**Version**: v1.0 MVP  
**Last Updated**: 2026-01-02
"# Popup_Service" 
