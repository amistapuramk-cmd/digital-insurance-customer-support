"""Digital Insurance Customer Support - Streamlit app.
Run: streamlit run app.py
"""
import pandas as pd
import streamlit as st

import database as db
from chatbot import FAQBot

ADMIN_PASSWORD = "admin123"  # demo only - change this!
CATEGORIES = ["Claim", "Renewal", "Premium Payment", "Policy Update", "Cancellation", "Other"]

st.set_page_config(page_title="Digital Insurance Support", page_icon="🛡️")
db.init_db()


@st.cache_resource
def get_bot():
    return FAQBot()


bot = get_bot()
st.title("🛡️ Digital Insurance Customer Support")

tab_chat, tab_ticket, tab_track, tab_policy, tab_admin = st.tabs(
    ["💬 Chat Assistant", "🎫 Raise Ticket", "🔍 Track Ticket", "📄 Policy Status", "🔐 Admin"])

# ---- Chat ----
with tab_chat:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! Ask me about claims, renewals, premiums or your policy."}]
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.write(m["content"])
    if prompt := st.chat_input("Type your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": bot.reply(prompt)})
        st.rerun()

# ---- Raise ticket ----
with tab_ticket:
    st.subheader("Raise a support ticket")
    with st.form("ticket_form", clear_on_submit=True):
        name = st.text_input("Full name")
        email = st.text_input("Email")
        policy_no = st.text_input("Policy number (e.g. POL1001)")
        category = st.selectbox("Category", CATEGORIES)
        desc = st.text_area("Describe your issue")
        if st.form_submit_button("Submit"):
            if not (name and email and policy_no and desc):
                st.error("Please fill all fields.")
            elif not db.get_policy(policy_no):
                st.error("Policy number not found.")
            else:
                tid = db.create_ticket(policy_no, name, email, category, desc)
                st.success(f"Ticket created! Your Ticket ID is **{tid}**. Save it to track status.")

# ---- Track ticket ----
with tab_track:
    st.subheader("Track your ticket")
    tid = st.number_input("Ticket ID", min_value=1, step=1)
    if st.button("Check status"):
        t = db.get_ticket(int(tid))
        if t:
            st.info(f"**Status:** {t['status']}  \n**Category:** {t['category']}  \n"
                    f"**Created:** {t['created_at']}  \n**Issue:** {t['description']}")
        else:
            st.error("Ticket not found.")

# ---- Policy status ----
with tab_policy:
    st.subheader("Check policy status")
    st.caption("Demo policy numbers: POL1001, POL1002, POL1003, POL1004")
    pno = st.text_input("Policy number", key="pno")
    if st.button("Search policy"):
        p = db.get_policy(pno)
        if p:
            st.success(f"Policy found: {p['policy_no']}")
            st.write(f"**Holder:** {p['holder']}")
            st.write(f"**Type:** {p['type']}")
            st.write(f"**Cover amount:** ₹{p['cover_amount']:,}")
            st.write(f"**Expiry date:** {p['expiry_date']}")
            st.write(f"**Status:** {p['status']}")
        else:
            st.error("Policy not found.")

# ---- Admin ----
with tab_admin:
    st.subheader("Admin panel")
    if st.text_input("Password", type="password", key="admin_pw") == ADMIN_PASSWORD:
        tickets = db.get_all_tickets()
        if tickets:
            st.dataframe(pd.DataFrame(tickets), use_container_width=True)
            c1, c2, c3 = st.columns([1, 2, 1])
            uid = c1.number_input("Ticket ID", min_value=1, step=1, key="uid")
            status = c2.selectbox("New status", ["Open", "In Progress", "Resolved", "Closed"])
            if c3.button("Update"):
                db.update_ticket_status(int(uid), status)
                st.success("Updated.")
                st.rerun()
        else:
            st.write("No tickets yet.")
    else:
        st.caption("Enter the admin password (demo: admin123).")
