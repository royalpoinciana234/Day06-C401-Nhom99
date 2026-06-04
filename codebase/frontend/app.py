import os
import httpx
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Long Châu AI Triage", page_icon="💊", layout="centered")

# ---------- Sidebar ----------
with st.sidebar:
    st.title("💊 Long Châu")
    st.caption("AI Middleware Demo — Tư vấn thuốc thông minh")
    st.divider()

    # Backend health check
    try:
        r = httpx.get(f"{BACKEND_URL}/health", timeout=3)
        if r.status_code == 200:
            st.success("✅ Backend: online")
        else:
            st.error("⚠️ Backend: lỗi")
    except Exception:
        st.error("❌ Backend: mất kết nối")

    st.divider()
    if st.button("🔄 Cuộc hội thoại mới"):
        st.session_state.history = []
        st.session_state.messages = []
        st.rerun()

    st.caption("Prototype — không thay thế tư vấn y tế chuyên nghiệp.")

# ---------- Session state ----------
if "history" not in st.session_state:
    st.session_state.history = []   # [{role, content}] sent to backend
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{role, content, meta}] for rendering

# ---------- Render history ----------
st.title("💬 Tư vấn thuốc Long Châu")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        meta = msg.get("meta", {})

        if meta.get("route") == "advisory_handoff":
            if meta.get("safety_gate_triggered"):
                st.caption("⚠️ Câu hỏi cần dược sĩ — được chuyển tự động qua safety gate")
            if meta.get("handoff_summary"):
                with st.expander("📋 Tóm tắt cho dược sĩ"):
                    st.info(meta["handoff_summary"])

        if meta.get("route") == "factual":
            st.caption("ℹ️ Thông tin chung — không thay thế tư vấn chuyên sâu")

        model = meta.get("model")
        if model:
            st.caption(f"_Model: {model}_")

# ---------- Chat input ----------
prompt = st.chat_input("Nhập câu hỏi về thuốc...")

if prompt:
    # Render user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            try:
                resp = httpx.post(
                    f"{BACKEND_URL}/chat",
                    json={"message": prompt, "history": st.session_state.history},
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()

                route = data.get("route", "")
                reply = data.get("reply", "")
                handoff_summary = data.get("handoff_summary")
                safety_triggered = data.get("safety_gate_triggered", False)
                model = data.get("model", "")

                st.markdown(reply)

                if route == "advisory_handoff":
                    if safety_triggered:
                        st.caption("⚠️ Câu hỏi cần dược sĩ — được chuyển tự động qua safety gate")
                    if handoff_summary:
                        with st.expander("📋 Tóm tắt cho dược sĩ"):
                            st.info(handoff_summary)

                if route == "factual":
                    st.caption("ℹ️ Thông tin chung — không thay thế tư vấn chuyên sâu")

                if model:
                    st.caption(f"_Model: {model}_")

                # Save to session
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                    "meta": {
                        "route": route,
                        "handoff_summary": handoff_summary,
                        "safety_gate_triggered": safety_triggered,
                        "model": model,
                    },
                })
                st.session_state.history.append({"role": "assistant", "content": reply})

            except httpx.ConnectError:
                st.error("❌ Mất kết nối backend. Vui lòng thử lại sau.")
            except httpx.TimeoutException:
                st.error("⏱️ Backend phản hồi quá chậm. Vui lòng thử lại.")
            except Exception as e:
                st.error(f"❌ Lỗi không xác định: {e}")
