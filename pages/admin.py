# STREAMLIT/pages/admin.py
import streamlit as st
from datetime import datetime
import service
from core.layout import (
    apply_portal_theme,
    render_topbar,
    info_card,
    app_links_card,
    portal_sidebar,
    render_floating_widget,
)

st.set_page_config(page_title="Admin", layout="wide")

# 로그인 체크
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("role", None)

if (not st.session_state.logged_in) or (st.session_state.role != "ADMIN"):
    st.switch_page("pages/0_Login.py")

def fmt_dt(ms: int) -> str:
    if not ms:
        return ""
    dt = datetime.fromtimestamp(ms / 1000.0)
    return dt.strftime("%Y-%m-%d %H:%M")


# -------------------------
# 상태값
# -------------------------
st.session_state.setdefault("admin_menu", "홈")
st.session_state.setdefault("selected_post_id", None)
st.session_state.setdefault("last_saved_post", None)

# [추가] 상세 진입 1회만 조회수 증가용
st.session_state.setdefault("last_viewed_post_id", None)

# 팝업 대상 선택 모달 상태
st.session_state.setdefault("open_target_dialog", False)
st.session_state.setdefault("target_selected_departments", set())
st.session_state.setdefault("target_selected_teams", set())

# 예약 전송 시간(라디오) 상태값
st.session_state.setdefault("popup_expected_send_time", "오전 10시")

apply_portal_theme(hide_pages_sidebar_nav=True, hide_sidebar=False, active_menu=st.session_state.admin_menu)
render_floating_widget(img_path="assets/chatimg_r.png", href="https://notiguard-production.up.railway.app/")

DEPARTMENTS = [
    "미래전략실",
    "기술고문실",
    "감사팀",
    "비서팀",
    "연구개발본부",
    "운영본부",
    "경영관리본부",
]
TEAMS_BY_DEPT = {
    "연구개발본부": ["연구1팀", "연구2팀", "신사업팀", "연구지원팀", "특수모터팀"],
    "운영본부": ["PM팀", "글로벌영업팀", "생산팀", "구매팀", "생산기술팀", "품질팀"],
    "경영관리본부": ["경영관리팀", "재경팀", "인사팀", "정보화팀"],
}


# -------------------------
# 유틸
# -------------------------
def reset_targets():
    st.session_state.target_selected_departments = set()
    st.session_state.target_selected_teams = set()

    # 위젯 상태도 같이 초기화(경고 방지 + 다음 오픈 시 깨끗하게)
    for dept in DEPARTMENTS:
        k = f"dlg_dept_{dept}"
        if k in st.session_state:
            del st.session_state[k]
    for dept, teams in TEAMS_BY_DEPT.items():
        for t in teams:
            k = f"dlg_team_{dept}_{t}"
            if k in st.session_state:
                del st.session_state[k]


def select_all_targets():
    """
    중요 공지일 때, 대상 선택 모달을 '전체 선택' 상태로 시작
    - set + 위젯 session_state를 같은 소스로 맞춤 (value= 미사용)
    """
    st.session_state.target_selected_departments = set(DEPARTMENTS)

    all_teams = []
    for dept, teams in TEAMS_BY_DEPT.items():
        for t in teams:
            all_teams.append(t)
            st.session_state[f"dlg_team_{dept}_{t}"] = True  # ✅ 위젯 상태 직접 세팅

    st.session_state.target_selected_teams = set(all_teams)

    for dept in DEPARTMENTS:
        st.session_state[f"dlg_dept_{dept}"] = True  # ✅ 위젯 상태 직접 세팅


def apply_dept_autoselect(dept: str, checked: bool):
    """
        본부 체크/해제 시:
      - target_selected_teams set 업데이트
      - 팀 체크박스(st.session_state) 값까지 강제 동기화
    """
    teams = TEAMS_BY_DEPT.get(dept, [])
    for t in teams:
        team_key = f"dlg_team_{dept}_{t}"
        st.session_state[team_key] = bool(checked)  # ✅ 위젯 상태 동기화
        if checked:
            st.session_state.target_selected_teams.add(t)
        else:
            st.session_state.target_selected_teams.discard(t)


# -------------------------
# 팝업 대상 선택 모달
# -------------------------
@st.dialog("팝업 발송 대상 선택", width="large")
def target_dialog():
    # 예약 전송 시간 기본값
    st.session_state.setdefault("popup_expected_send_time", "오전 10시")

    # 헤더 라인 오른쪽 라디오 (CSS/디자인 수정 없음)
    h1, h2 = st.columns([3.2, 1.8], gap="small")
    with h1:
        st.markdown("### 예약 전송 시간 선택")
    with h2:
        st.radio(
            "",
            ["오전 10시", "오후 2시"],
            horizontal=True,
            key="popup_expected_send_time",
        )

    left, right = st.columns([1, 1], gap="large")

    # -------------------------
    # 본부 선택 (value= 미사용 / session_state 키 단일화)
    # -------------------------
    with left:
        st.markdown("### 본부 선택")
        dept_box = st.container(border=True, height=420)
        with dept_box:
            for dept in DEPARTMENTS:
                dept_key = f"dlg_dept_{dept}"

                # set 기준 초기값을 위젯 상태로 넣어줌 (딱 1번)
                prev = dept in st.session_state.target_selected_departments
                st.session_state.setdefault(dept_key, prev)

                checked = st.checkbox(dept, key=dept_key)

                # 변경 감지
                if checked != prev:
                    if checked:
                        st.session_state.target_selected_departments.add(dept)
                    else:
                        st.session_state.target_selected_departments.discard(dept)

                    # 본부 → 하위 팀 전체 동기화 (rerun 없이 유지)
                    apply_dept_autoselect(dept, checked)

    # -------------------------
    # 팀 선택 (value= 미사용 / session_state 키 단일화)
    # -------------------------
    with right:
        st.markdown("### 팀 선택")
        team_box = st.container(border=True, height=420)
        with team_box:
            for dept, teams in TEAMS_BY_DEPT.items():
                st.markdown(f"**{dept}**")
                for t in teams:
                    team_key = f"dlg_team_{dept}_{t}"

                    prev = (t in st.session_state.target_selected_teams)
                    st.session_state.setdefault(team_key, prev)

                    checked = st.checkbox(t, key=team_key)

                    if checked:
                        st.session_state.target_selected_teams.add(t)
                    else:
                        st.session_state.target_selected_teams.discard(t)

                st.divider()

    st.divider()
    c1, c2 = st.columns([1, 1])

    with c1:
        if st.button("취소", use_container_width=True):
            reset_targets()
            st.session_state.open_target_dialog = False
            st.rerun()

    with c2:
        if st.button("선택한 대상에게 팝업 발송", type="primary", use_container_width=True):
            post = st.session_state.last_saved_post
            expected_send_time = st.session_state.get("popup_expected_send_time", "오전 10시")

            service.create_popup(
                post,
                sorted(st.session_state.target_selected_departments),
                sorted(st.session_state.target_selected_teams),
                expected_send_time=expected_send_time,
            )

            reset_targets()
            st.session_state.last_saved_post = None
            st.session_state.open_target_dialog = False
            st.session_state.admin_menu = "게시판"
            st.success("중요공지 등록 및 팝업 발송 완료")
            st.rerun()


def on_menu_change(new_menu: str):
    st.session_state.admin_menu = new_menu
    st.session_state.selected_post_id = None


# 왼쪽 네비
portal_sidebar(role="ADMIN", active_menu=st.session_state.admin_menu, on_menu_change=on_menu_change)

# 상단바
render_topbar("전사 Portal")

menu = st.session_state.admin_menu


# -------------------------
# 홈 카드
# -------------------------
def render_home_cards():
    a, b, c = st.columns([1.25, 3.25, 1.25], gap="large")

    with a:
        box = st.container(border=True)
        with box:
            info_card(
                title="사용자 정보",
                subtitle="관리자 계정",
                lines=[("권한", "ADMIN"), ("상태", "로그인")],
                badge="ADMIN",
            )

    with b:
        box = st.container(border=True)
        with box:
            info_card(
                title="전사게시판",
                subtitle="공지 목록/상세 확인",
                lines=[("기능", "공지 조회/상세"), ("권한", "관리자 작성 / 직원 조회")],
            )
            if st.button("게시판 바로가기", type="primary", key="go_board_admin"):
                on_menu_change("게시판")
                st.rerun()

    with c:
        box = st.container(border=True)
        with box:
            app_links_card("업무사이트 (데모)", ["e-Accounting", "JDE ERP", "HRM", "e-Procurement"], role="ADMIN")


if menu == "홈":
    render_home_cards()
    st.write("")
    st.divider()


# -------------------------
# 실제 기능 영역
# -------------------------
if menu == "홈":
    st.subheader("관리자 홈")
    st.write("좌측 메뉴에서 게시판/글쓰기를 선택하세요.")

elif menu == "게시판":

    def _clear_admin_board_selection():
        if "admin_board_table" in st.session_state:
            try:
                st.session_state.admin_board_table["selection"]["rows"] = []
            except Exception:
                pass

    if st.session_state.selected_post_id:
        st.subheader("게시글 상세")
        pid = int(st.session_state.selected_post_id)

        # 최초 1회만 조회수 증가
        if st.session_state.last_viewed_post_id != pid:
            service.increment_views(pid)
            st.session_state.last_viewed_post_id = pid

        post = service.get_post_by_id(pid)

        box = st.container(border=True)
        with box:
            if not post:
                st.error("게시글을 찾을 수 없습니다.")
            else:
                badge = "중요공지" if post["type"] == "중요" else "일반공지"
                st.markdown(f"**[{badge}] {post['title']}**")
                st.caption(
                    f"작성자: {post['author']} | 작성일: {fmt_dt(post['timestamp'])} | 조회: {post['views']}"
                )
                st.text(post["content"])
                # 첨부 표시
                attachments = post.get("attachments", []) if post else []
                if attachments:
                    st.markdown("**첨부파일**")
                    for a in attachments:
                        path = a.get("filePath", "")
                        name = a.get("filename", "file")
                        mime = (a.get("mimeType", "") or "").lower()

                        try:
                            with open(path, "rb") as f:
                                data = f.read()

                            # 이미지면 미리보기
                            if mime.startswith("image/"):
                                st.image(data, caption=name)

                            st.download_button(
                                label=f"다운로드: {name}",
                                data=data,
                                file_name=name,
                                mime=a.get("mimeType", "") or None,
                                key=f"dl_admin_{a['fileId']}",
                            )
                        except FileNotFoundError:
                            st.warning(f"파일을 찾을 수 없습니다: {name}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("목록으로", type="primary", use_container_width=True, key="admin_back_to_list"):
                st.session_state.selected_post_id = None
                _clear_admin_board_selection()
                st.rerun()
        with c2:
            if st.button("새글쓰기", use_container_width=True, key="admin_go_write"):
                on_menu_change("글쓰기")
                st.rerun()

    else:
        head_l, head_r = st.columns([6, 1.2])
        with head_l:
            st.subheader("게시판 홈")
        with head_r:
            if st.button("새글쓰기", type="primary", use_container_width=True, key="admin_write_btn"):
                on_menu_change("글쓰기")
                st.rerun()

        box = st.container(border=True)
        with box:
            st.markdown("**전사 공지**")
            posts = service.list_posts()

            if not posts:
                st.info("등록된 게시글이 없습니다.")
            else:
                table_rows = [
                    {
                        "번호": p["postId"],
                        "제목": p["title"],
                        "작성자": p["author"],
                        "작성일": fmt_dt(p["timestamp"]),
                        "조회": p["views"],
                    }
                    for p in posts
                ]

                event = st.dataframe(
                    table_rows,
                    width="stretch",
                    hide_index=True,
                    key="admin_board_table",
                    on_select="rerun",
                    selection_mode="single-row",
                )

                try:
                    if event is not None and event.selection.rows:
                        row_idx = event.selection.rows[0]
                        clicked_post_id = int(table_rows[row_idx]["번호"])
                        st.session_state.selected_post_id = clicked_post_id
                        st.rerun()
                except Exception:
                    pass

elif menu == "글쓰기":
    st.subheader("새글쓰기")

    ntype = st.radio("공지 유형", ["중요", "일반"], index=0, horizontal=True)
    title = st.text_input("제목", value="", key="w_title")
    content = st.text_area("내용", value="", height=220, key="w_content")
    files = st.file_uploader("첨부파일(이미지/파일)", accept_multiple_files=True, key="w_files")

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("등록", type="primary", use_container_width=True):
            if not title.strip() or not content.strip():
                st.error("제목과 내용을 입력해주세요.")
            else:
                post_info = service.save_post(title.strip(), content.strip(), ntype, uploaded_files=files)
                st.session_state.last_saved_post = post_info

                if ntype == "중요":
                    select_all_targets()
                    st.session_state.open_target_dialog = True
                else:
                    st.success("일반 공지 등록 완료")
                    on_menu_change("게시판")
                st.rerun()

    with c2:
        if st.button("취소", use_container_width=True):
            on_menu_change("게시판")
            st.rerun()

    if st.session_state.open_target_dialog:
        st.session_state.open_target_dialog = False
        target_dialog()
