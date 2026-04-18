import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kitchen Pro ERP", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
body {font-family: Cairo;}
.header{
    background: linear-gradient(90deg,#1e272e,#2c3e50);
    padding:25px;
    text-align:center;
    color:#f1c40f;
    border-radius:15px;
    font-weight:bold;
}
.card{
    background:white;
    padding:15px;
    border-radius:15px;
    box-shadow:0 3px 12px rgba(0,0,0,0.1);
    margin-top:15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "db" not in st.session_state:
    st.session_state.db = []

# =====================================================
# 🟦 HOME PAGE
# =====================================================
if st.session_state.page == "home":

    st.markdown("""
    <div class="header">
        💎 KITCHEN PRO ERP <br>
        برمجة المهندس ياسين علاء
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.image("https://i.imgur.com/8Km9tLL.png", width=160)

    if st.button("🚀 الدخول للنظام", use_container_width=True):
        st.session_state.page = "system"
        st.rerun()

# =====================================================
# 🟩 SYSTEM PAGE
# =====================================================
else:

    st.title("📋 نظام التخصيم الاحترافي")

    if st.button("⬅ الرجوع"):
        st.session_state.page = "home"
        st.rerun()

    st.divider()

    # ---------------- INPUT ----------------
    st.subheader("➕ إضافة وحدة")

    c1, c2, c3, c4 = st.columns(4)
    name = c1.text_input("اسم الوحدة")
    u_type = c2.selectbox("النوع", ["سفلية", "علوية", "دولاب"])
    qty = c3.number_input("الكمية", 1)
    W = c4.number_input("العرض")

    c5, c6, c7 = st.columns(3)
    H = c5.number_input("الارتفاع")
    D = c6.number_input("العمق")

    shelves = c7.number_input("رفوف", 0)

    c8, c9, c10 = st.columns(3)
    dividers = c8.number_input("فواصل", 0)
    drawers = c9.number_input("أدراج", 0)

    if st.button("➕ إضافة الوحدة", use_container_width=True):

        if W > 0 and H > 0 and D > 0:

            st.session_state.db.append({
                "name": name or f"UNIT-{len(st.session_state.db)+1}",
                "type": u_type,
                "qty": qty,
                "W": W,
                "H": H,
                "D": D,
                "sh": shelves,
                "dv": dividers,
                "dr": drawers
            })

            st.success("تمت الإضافة ✔")
            st.rerun()

    st.divider()

    # =====================================================
    # 📊 CALCULATION ENGINE
    # =====================================================
    if st.session_state.db:

        st.subheader("📊 جدول التخصيم الكامل")

        table = []

        total_aluminum = 0
        total_fiber = 0

        for u in st.session_state.db:

            # =========================
            # الخصم حسب النوع
            # =========================
            h_deduct = 13 if u["type"] == "سفلية" or u["type"] == "دولاب" else 5

            W = u["W"] - 5
            H = u["H"] - h_deduct
            D = u["D"] - 5

            # =========================
            # الألومنيوم (المعادلات)
            # =========================
            alum_single = (H * 2) + (W * 3) + (D * 2)
            alum_double = (H * 2) + (W * 1) + (D * 2)

            if u["type"] != "سفلية":
                alum_single = (H * 2) + (W * 2)
                alum_double = (H * 2) + (W * 2) + (D * 4)

            # إضافات
            alum_single += (u["sh"] + u["dv"]) * 4 * 10
            alum_single += u["dr"] * 20

            # =========================
            # الفيبر
            # =========================
            fiber = (W * H) + (W * D) + (H * D * 2)

            if u["sh"] > 0:
                fiber += u["sh"] * (W * (D - 5))

            if u["dv"] > 0:
                fiber += u["dv"] * (H * (D - 5))

            # =========================
            # الإجمالي
            # =========================
            total_aluminum += alum_single * u["qty"]
            total_fiber += fiber * u["qty"]

            table.append({
                "الوحدة": u["name"],
                "النوع": u["type"],
                "العدد": u["qty"],
                "W": W,
                "H": H,
                "D": D,
                "ألمنيوم مفرد": alum_single,
                "ألمنيوم متقارب": alum_double,
                "فيبر": fiber
            })

        st.table(pd.DataFrame(table))

        st.divider()

        # =========================
        # TOTAL
        # =========================
        st.success(f"""
        📦 إجمالي الألومنيوم: {round(total_aluminum/600,2)} عود  
        🪵 إجمالي الفيبر: {round(total_fiber/36400,2)} لوح
        """)

        # =========================
        # RESET
        # =========================
        if st.button("🗑️ مسح المشروع بالكامل"):
            st.session_state.db = []
            st.rerun()

    else:
        st.info("ابدأ بإضافة وحدات لعرض التخصيم")
