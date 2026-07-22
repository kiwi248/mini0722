"""FastAPI 백엔드(Chat/Post/User)를 호출하는 Streamlit 프런트엔드입니다.

실행 방법(프로젝트 루트에서):
    1) uvicorn app.main:app --reload        # 백엔드 먼저 실행
    2) streamlit run streamlit_app.py       # 프런트엔드 실행
"""

import httpx
import streamlit as st

st.set_page_config(page_title="Team1 관리 콘솔", page_icon="🗂️", layout="wide")

if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = "https://mini0722.onrender.com"

with st.sidebar:
    st.header("설정")
    st.session_state.api_base_url = st.text_input(
        "백엔드 API 주소", value=st.session_state.api_base_url
    )
    st.caption("FastAPI 서버가 이 주소에서 실행 중이어야 합니다.")

BASE_URL = st.session_state.api_base_url.rstrip("/")


def call_api(method: str, path: str, **kwargs):
    """공통 API 호출 함수. 성공 시 (True, data), 실패 시 (False, 에러 메시지)를 반환합니다."""
    try:
        response = httpx.request(method, f"{BASE_URL}{path}", timeout=60.0, **kwargs)
    except httpx.RequestError as exc:
        return False, f"백엔드에 연결할 수 없습니다: {exc}"

    try:
        body = response.json()
    except ValueError:
        body = response.text

    if response.status_code >= 400:
        detail = body.get("detail") if isinstance(body, dict) else body
        return False, f"[{response.status_code}] {detail}"
    return True, body


st.title("🗂️ Team1 관리 콘솔")

user_tab, post_tab, chat_tab = st.tabs(["👤 회원 관리", "📝 게시글 관리", "💬 Gemini 챗봇"])


# ------------------------------------------------------------------
# 회원 관리
# ------------------------------------------------------------------
with user_tab:
    st.subheader("회원 목록")
    if st.button("회원 목록 새로고침", key="refresh_users"):
        st.rerun()

    ok, result = call_api("GET", "/users")
    if ok:
        users = result.get("data", []) if isinstance(result, dict) else result
        if users:
            st.dataframe(users, use_container_width=True)
        else:
            st.info("등록된 회원이 없습니다.")
    else:
        st.error(result)

    st.divider()
    col_create, col_manage = st.columns(2)

    with col_create:
        st.markdown("### 회원 등록")
        with st.form("create_user_form"):
            new_email = st.text_input("이메일")
            new_password = st.text_input("비밀번호", type="password")
            new_name = st.text_input("이름")
            submitted = st.form_submit_button("등록")
            if submitted:
                ok, result = call_api(
                    "POST",
                    "/users",
                    json={"email": new_email, "password": new_password, "name": new_name},
                )
                if ok:
                    st.success(result.get("message", "회원이 생성되었습니다."))
                    st.rerun()
                else:
                    st.error(result)

    with col_manage:
        st.markdown("### 회원 조회 / 수정 / 삭제")
        target_user_id = st.text_input("대상 user_id")

        if st.button("조회", key="get_user"):
            if target_user_id:
                ok, result = call_api("GET", f"/users/{target_user_id}")
                if ok:
                    st.json(result.get("data"))
                else:
                    st.error(result)
            else:
                st.warning("user_id를 입력해 주세요.")

        with st.form("update_user_form"):
            st.caption("수정할 값을 모두 입력해 주세요.")
            upd_email = st.text_input("새 이메일", key="upd_email")
            upd_password = st.text_input("새 비밀번호", type="password", key="upd_password")
            upd_name = st.text_input("새 이름", key="upd_name")
            update_submitted = st.form_submit_button("수정")
            if update_submitted:
                if target_user_id:
                    ok, result = call_api(
                        "PUT",
                        f"/users/{target_user_id}",
                        json={"email": upd_email, "password": upd_password, "name": upd_name},
                    )
                    if ok:
                        st.success(result.get("message", "회원 정보가 수정되었습니다."))
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.warning("user_id를 입력해 주세요.")

        if st.button("삭제", key="delete_user"):
            if target_user_id:
                ok, result = call_api("DELETE", f"/users/{target_user_id}")
                if ok:
                    st.success(result.get("message", "회원이 삭제되었습니다."))
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.warning("user_id를 입력해 주세요.")


# ------------------------------------------------------------------
# 게시글 관리
# ------------------------------------------------------------------
with post_tab:
    st.subheader("게시글 목록")
    if st.button("게시글 목록 새로고침", key="refresh_posts"):
        st.rerun()

    ok, posts = call_api("GET", "/posts")
    if ok:
        if posts:
            st.dataframe(posts, use_container_width=True)
        else:
            st.info("등록된 게시글이 없습니다.")
    else:
        st.error(posts)

    st.divider()
    col_create, col_manage = st.columns(2)

    with col_create:
        st.markdown("### 게시글 작성")
        with st.form("create_post_form"):
            post_user_id = st.number_input("작성자 user_id", min_value=1, step=1)
            post_title = st.text_input("제목")
            post_content = st.text_area("내용")
            submitted = st.form_submit_button("작성")
            if submitted:
                ok, result = call_api(
                    "POST",
                    "/posts",
                    json={"user_id": int(post_user_id), "title": post_title, "content": post_content},
                )
                if ok:
                    st.success("게시글이 생성되었습니다.")
                    st.rerun()
                else:
                    st.error(result)

    with col_manage:
        st.markdown("### 게시글 조회 / 수정 / 삭제")
        target_post_id = st.number_input("대상 post_id", min_value=1, step=1, key="target_post_id")

        if st.button("조회", key="get_post"):
            ok, result = call_api("GET", f"/posts/{int(target_post_id)}")
            if ok:
                st.json(result)
            else:
                st.error(result)

        with st.form("update_post_form"):
            upd_title = st.text_input("새 제목", key="upd_title")
            upd_content = st.text_area("새 내용", key="upd_content")
            update_submitted = st.form_submit_button("수정")
            if update_submitted:
                ok, result = call_api(
                    "PUT",
                    f"/posts/{int(target_post_id)}",
                    json={"title": upd_title, "content": upd_content},
                )
                if ok:
                    st.success("게시글이 수정되었습니다.")
                    st.rerun()
                else:
                    st.error(result)

        if st.button("삭제", key="delete_post"):
            ok, result = call_api("DELETE", f"/posts/{int(target_post_id)}")
            if ok:
                st.success(result.get("message", "게시글이 삭제되었습니다."))
                st.rerun()
            else:
                st.error(result)


# ------------------------------------------------------------------
# Gemini 챗봇
# ------------------------------------------------------------------
with chat_tab:
    st.subheader("Gemini 챗봇")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    prompt = st.chat_input("메시지를 입력하세요")
    if prompt:
        st.session_state.chat_history.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        ok, result = call_api(
            "POST",
            "/chat/gemini",
            json={"user_id": "streamlit-user", "prompt": prompt},
        )
        if ok:
            answer = result.get("data", {}).get("answer", "") if isinstance(result, dict) else ""
        else:
            answer = f"오류: {result}"

        st.session_state.chat_history.append(("assistant", answer))
        with st.chat_message("assistant"):
            st.markdown(answer)
