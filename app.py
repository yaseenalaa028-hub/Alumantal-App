import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kitchen Pro ERP", layout="wide")

# ================= SESSION =================
if "db" not in st.session_state:
    st.session_state.db = []

# ================= HEADER =================
st.markdown("""
<div style="background:#2f3640;color:#fbc531;padding:20px;text-align:center;border-radius:10px;">
<h2>💎 نظام تخصيم الألومنيوم</h2>
<p>برمجة المهندس ياسين علاء</p>
</div>
""", unsafe_allow_html=True)

# ================= INPUT =================
st.subheader("📝 إضافة وحدة")

c1, c2, c3 = st.columns(3)
name = c1.text_input("اسم الوحدة")
u_type = c2.selectbox("النوع", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
qty = c3.number_input("العدد", 1)

c4, c5, c6 = st.columns(3)
w = c4.number_input("العرض")
h = c5.number_input("الارتفاع")
d = c6.number_input("العمق")

st.write("### الإضافات")

c7, c8, c9 = st.columns(3)
sh_w = c7.number_input("عرض الرف")
sh_d = c8.number_input("عمق الرف")
sh_n = c9.number_input("عدد الرفوف", 0)

c10, c11, c12 = st.columns(3)
dv_h = c10.number_input("ارتفاع الفاصل")
dv_d = c11.number_input("عمق الفاصل")
dv_n = c12.number_input("عدد الفواصل", 0)

c13, c14, c15 = st.columns(3)
dr_w = c13.number_input("عرض الدرج")
dr_d = c14.number_input("عمق الدرج")
dr_n = c15.number_input("عدد الأدراج", 0)

# ================= ADD =================
if st.button("➕ إضافة الوحدة"):

    if w > 0 and h > 0:
        st.session_state.db.append({
            "title": name or f"UNIT-{len(st.session_state.db)+1}",
            "type": u_type,
            "qty": qty,
            "w": w, "h": h, "d": d,
            "sh_w": sh_w, "sh_d": sh_d, "sh_n": sh_n,
            "dv_h": dv_h, "dv_d": dv_d, "dv_n": dv_n,
            "dr_w": dr_w, "dr_d": dr_d, "dr_n": dr_n
        })
        st.success("تمت الإضافة ✔")

# ================= MAIN =================
if st.session_state.db:

    st.divider()

    table_data = []
    report_text = ""

    total_m, total_t, total_f = 0, 0, 0

    for u in st.session_state.db:

        h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_b = u['w'] - 5
        d_b = u['d'] - 5

        # ================= TABLE =================
        table_data.append({
            "الوحدة": u["title"],
            "النوع": u["type"],
            "العدد": u["qty"],
            "W": w_b,
            "H": h_b,
            "D": d_b
        })

        # ================= REPORT =================
        txt = f"\n📦 {u['title']} | {u['type']} | {u['w']}x{u['h']}x{u['d']}\n"
        txt += "━"*50 + "\n"

        if u['type'] == "سفلية":
            txt += f"ارتفاع {h_b}: 2 مفرد / 2 متقارب\n"
            txt += f"عرض {w_b}: 3 مفرد / 1 متقارب\n"
            txt += f"عمق {d_b}: 2 مفرد / 2 متقارب\n"
        else:
            txt += f"ارتفاع {h_b}: 2 مفرد / 2 متقارب\n"
            txt += f"عرض {w_b}: 2 مفرد / 2 متقارب\n"
            txt += f"عمق {d_b}: 4 متقارب\n"

        txt += f"\n🪵 فيبر: {w_b}×{h_b} | {w_b}×{d_b} | {h_b}×{d_b}\n"

        if u['sh_n'] > 0:
            txt += f"رفوف: {u['sh_n']}\n"
        if u['dv_n'] > 0:
            txt += f"فواصل: {u['dv_n']}\n"
        if u['dr_n'] > 0:
            txt += f"أدراج: {u['dr_n']}\n"

        txt += "━"*50
        report_text += txt + "\n"

        # ================= CALC =================
        if u['type'] == "سفلية":
            m = (h_b*2)+(w_b*3)+(d_b*2)
            t = (h_b*2)+(w_b*1)+(d_b*2)
        else:
            m = (h_b*2)+(w_b*2)
            t = (h_b*2)+(w_b*2)+(d_b*4)

        f = (w_b*h_b)+(w_b*d_b)+(h_b*d_b*2)

        total_m += m * u["qty"]
        total_t += t * u["qty"]
        total_f += f * u["qty"]

    # ================= TABLE VIEW =================
    st.subheader("📊 جدول التخصيم")
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True)

    # ================= REPORT VIEW =================
    st.subheader("📄 تقرير التخصيم")
    st.text_area("التقرير", report_text, height=300)

    # ================= TOTAL =================
    st.subheader("📦 إجمالي المشروع")

    c1, c2, c3 = st.columns(3)
    c1.metric("ألومنيوم مفرد", f"{total_m/600:.2f} عود")
    c2.metric("ألومنيوم متقارب", f"{total_t/600:.2f} عود")
    c3.metric("فيبر", f"{total_f/36400:.2f} لوح")

    # ================= DOWNLOAD =================
    st.download_button("💾 تحميل التقرير", report_text, file_name="report.txt")

    # ================= CLEAR =================
    if st.button("🗑️ مسح المشروع"):
        st.session_state.db = []
