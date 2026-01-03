import base64
import mimetypes
from pathlib import Path
import streamlit as st


PORTAL_PRIMARY = "#139fb0"
PORTAL_BG = "#f5f7fb"
CARD_BORDER = "rgba(17,24,39,0.10)"

def apply_portal_theme(*, hide_pages_sidebar_nav: bool, hide_sidebar: bool, active_menu: str | None = None):
    active_menu = active_menu or ""
    st.markdown(
        f"""
        <style>
        body {{ background: {PORTAL_BG}; }}
        .block-container {{
            padding-top: 0.8rem;
            padding-bottom: 1.2rem;
            max-width: 1600px;
        }}

        {"div[data-testid='stSidebarNav']{display:none !important;}" if hide_pages_sidebar_nav else ""}
        {"section[data-testid='stSidebar']{display:none !important;}" if hide_sidebar else ""}

        section[data-testid="stSidebar"] > div {{
            background: {PORTAL_PRIMARY};
            color: #fff;
            padding-top: 18px;
        }}

        section[data-testid="stSidebar"] .stButton button {{
            width: 100%;
            border-radius: 0px;
            border: none;
            padding: 10px 12px;
            font-weight: 900;
            margin-bottom: 8px;
            background: transparent;
            color: #fff;
            height: 44px;
            box-shadow: none;

            display: flex !important;
            justify-content: flex-start !important;
            align-items: center !important;
            text-align: left !important;
            padding-left: 16px !important;
        }}

        section[data-testid="stSidebar"] .stButton button > div {{
            width: 100% !important;
            display: flex !important;
            justify-content: flex-start !important;
        }}

        section[data-testid="stSidebar"] .stButton button:hover {{
            background: rgba(255,255,255,0.10);
            border-radius: 12px;
        }}

        section[data-testid="stSidebar"] .stButton button.hs-active {{
            background: rgba(255,255,255,0.18) !important;
            border-radius: 12px !important;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.30);
        }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            border-color: {CARD_BORDER};
            border-radius: 14px;
            background: #fff;
            box-shadow: 0 10px 26px rgba(0,0,0,0.06);
        }}

        .stButton button[kind="primary"] {{
            background: {PORTAL_PRIMARY};
            border: 1px solid {PORTAL_PRIMARY};
            font-weight: 900;
            border-radius: 12px;
            height: 42px;
        }}

        .hs-card {{
            min-height: 230px;
            height: 230px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        </style>

        <script>
        (function () {{
          const active = {active_menu!r};
          const doc = window.parent.document;
          const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
          if (!sidebar) return;

          const btns = sidebar.querySelectorAll('button');
          btns.forEach((b) => {{
            const t = (b.innerText || '').trim();
            if (!t) return;
            if (t === active) b.classList.add('hs-active');
            else b.classList.remove('hs-active');
          }});
        }})();
        </script>
        """,
        unsafe_allow_html=True,
    )

PORTAL_PRIMARY = "#139fb0"
PORTAL_BG = "#f5f7fb"
CARD_BORDER = "rgba(17,24,39,0.10)"

def render_floating_widget(*, img_path: str, href: str, width_px: int = 200, bottom_px: int = 0, right_px: int = 0):
    """
    우측 하단 플로팅 '이미지 위젯' - 이미지 원본 형태 유지
    - width_px: 이미지 너비 기준(비율 유지)
    """

    p = Path(img_path)
    if not p.exists():
        st.warning(f"Floating widget image not found: {p.resolve()}")
        return

    mime, _ = mimetypes.guess_type(str(p))
    mime = mime or "image/png"

    b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
    data_url = f"data:{mime};base64,{b64}"

    st.markdown(
        f"""
        <style>
          .hs-fab-img {{
            position: fixed;
            right: {right_px}px;
            bottom: {bottom_px}px;
            z-index: 999999;

            /* 원본 형태 유지: 컨테이너는 마스크 역할 안 함 */
            background: transparent;
            border: none;
            border-radius: 0;
            overflow: visible;

            /* 살짝 띄워주는 그림자만 */
            filter: none;
            transform: translateY(0);
            transition: transform 0.12s ease, filter 0.12s ease;
            display: inline-block;
          }}

          .hs-fab-img:hover {{
            transform: translateY(-2px);
            filter: drop-shadow(0 22px 42px rgba(0,0,0,0.34));
          }}

          .hs-fab-img img {{
            width: {width_px}px;    /* 너비만 고정 */
            height: auto;           /* 비율 유지 */
            display: block;
            user-select: none;
          }}
        </style>

        <a class="hs-fab-img" href="{href}" target="_blank" rel="noopener">
          <img src="{data_url}" alt="floating-widget"/>
        </a>
        """,
        unsafe_allow_html=True,
    )


def render_topbar(title: str):
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:10px;">
          <div style="font-size:22px;font-weight:950;color:#111827;">{title}</div>
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="min-width:320px;">
        """,
        unsafe_allow_html=True,
    )
    st.text_input("통합검색", placeholder="통합검색 (데모)", label_visibility="collapsed", key="global_search")
    st.markdown("</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1], gap="small")
    with c1:
        st.button("🔔", key="topbell")
    with c2:
        st.button("👤", key="topuser")
    st.markdown("</div></div>", unsafe_allow_html=True)

def info_card(title: str, subtitle: str, lines: list[tuple[str, str]], badge: str | None = None):
    badge_html = ""
    if badge:
        badge_html = f"""
        <span style="
          background: rgba(19,159,176,0.15);
          color: #0b7f8e;
          font-weight: 950;
          padding: 6px 10px;
          border-radius: 999px;
          font-size: 12px;
          border: 1px solid rgba(19,159,176,0.25);
          white-space: nowrap;
        ">{badge}</span>
        """

    kv_html = "".join([
        f'<div style="color:rgba(0,0,0,0.55);font-weight:850;">{k}</div>'
        f'<div style="color:#111827;font-weight:950;">{v}</div>'
        for k, v in lines
    ])

    st.markdown(
        f"""
        <div class="hs-card">
          <div style="display:flex;align-items:center;justify-content:space-between;">
            <div>
              <div style="font-weight:950;font-size:15px;color:#111827;">{title}</div>
              <div style="margin-top:2px;color:rgba(0,0,0,0.55);font-size:13px;">{subtitle}</div>
            </div>
            {badge_html}
          </div>

          <div style="display:grid;grid-template-columns:92px 1fr;row-gap:8px;column-gap:12px;font-size:13px;margin-top:10px;flex:1;">
            {kv_html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def app_links_card(title: str, links: list[str], role: str):
    st.markdown(f"**{title}**")
    for i, name in enumerate(links):
        st.button(name, use_container_width=True, key=f"link_{role}_{name}_{i}")

def portal_sidebar(*, role: str, active_menu: str, on_menu_change):
    st.sidebar.markdown("## HS HYOSUNG")

    menus = ["홈", "게시판"] + (["글쓰기"] if role == "ADMIN" else []) + ["메일","문서관리","커뮤니티","보고"]
    for m in menus:
        if st.sidebar.button(m, key=f"nav_{role}_{m}", use_container_width=True):
            on_menu_change(m)
            st.rerun()

    st.sidebar.markdown("---")

    if st.sidebar.button("로그아웃", key=f"logout_{role}", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.employee_id = None
        st.session_state.employee_info = None
        st.session_state._login_modal_open = True
        st.switch_page("pages/0_Login.py")
