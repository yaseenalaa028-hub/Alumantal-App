import streamlit as st
import pandas as pd

# إعدادات واجهة "Ded El Kasr"
st.set_page_config(page_title="Ded El Kasr - Aluminum System", layout="wide")

# تصميم الهيدر
st.markdown("""
    <div style="background-color: #2c3e50; padding: 20px; border-radius: 15px; border-bottom: 5px solid #f1c40f; text-align: center;">
        <h1 style="color: #f1c40f; margin: 0;">DED EL KASR | ضد الكسر</h1>
        <p style="color: white; font-size: 1.2em;">نظام التخصيم الفني - المهندس ياسين علاء</p>
    </div>
    <br>
""", unsafe_allow_html=True)

if 'project' not in st.session_state:
    st.session_state.project = []

# منطقة المدخلات
with st.form("input_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        u_name = st.text_input("اسم الوحدة", "مطبخ 1")
        u_type = st.selectbox("النوع", ["سفلية", "علوية", "دولاب خزين"])
    with c2:
        w = st.number_input("العرض (سم)", min_value=0.0, step=0.1)
        h = st.number_input("الارتفاع (سم)", min_value=0.0, step=0.1)
    with c3:
        d = st.number_input("العمق (سم)", min_value=0.0, step=0.1)
        add_unit = st.form_submit_button("➕ إضافة الوحدة وتحسيبها")

if add_unit:
    # معادلات الورشة (المهندس ياسين)
    h_b = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
    w_b, d_b = w - 5, d - 5
    
    unit_res = {
        "الوحدة": u_name, "النوع": u_type,
        "ارتفاع التخصيم": h_b, "عرض التخصيم": w_b, "عمق التخصيم": d_b
    }
    st.session_state.project.append(unit_res)

# عرض النتائج والجرد
if st.session_state.project:
    st.subheader("📋 جدول الوحدات المضافة")
    df = pd.DataFrame(st.session_state.project)
    st.table(df)

    # حسابات الجرد السريع
    st.sidebar.header("📊 إجمالي خامات المشروع")
    total_f = sum([(x['عرض التخصيم'] * x['ارتفاع التخصيم']) / 10000 for x in st.session_state.project])
    st.sidebar.metric("مساحة الفيبر المطلوبة", f"{total_f:.2f} م²")
    
    if st.sidebar.button("🗑️ مسح المشروع"):
        st.session_state.project = []
        st.rerun()

st.info("💡 للتشغيل: اكتب streamlit run app.py في التيرمينال")
