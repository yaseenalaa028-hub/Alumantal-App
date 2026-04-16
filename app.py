import streamlit as st

# إعدادات الصفحة - نسخة المهندس ياسين علاء
st.set_page_config(page_title="AL-PRINCE SYSTEM", layout="centered")

# تصميم الواجهة (Dark Mode)
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .title-text { color: #2ecc71; text-align: center; font-size: 32px; font-weight: bold; padding: 20px; }
    .subtitle-text { color: #94a3b8; text-align: center; font-size: 18px; margin-bottom: 30px; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #1e293b !important; color: #2ecc71 !important; border: 1px solid #334155 !important;
    }
    label { color: #f8fafc !important; font-weight: bold !important; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 4em; 
        background-color: #2ecc71; color: #0f172a; 
        font-weight: bold; font-size: 20px; border: none;
    }
    .result-card {
        background-color: #1e293b; padding: 20px; border-radius: 10px; 
        border-right: 5px solid #2ecc71; color: #f8fafc; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'started' not in st.session_state:
    st.session_state.started = False
if 'storage' not in st.session_state:
    st.session_state.storage = []

# --- الصفحة الرئيسية ---
if not st.session_state.started:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div class="title-text">🏗️ نظام تخصيم الألومنيوم</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">إشراف المهندس ياسين علاء</div>', unsafe_allow_html=True)
    if st.button("🚀 ابدأ التخصيم"):
        st.session_state.started = True
        st.rerun()

# --- صفحة المدخلات ---
else:
    st.markdown('<div class="title-text" style="font-size:24px;">لوحة إدخال البيانات</div>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            u_title = st.text_input("اسم القطعة", placeholder="مثلاً: وحدة مطبخ")
            u_type = st.selectbox("نوع التخصيم", ["سفلية", "علوية", "دولاب خزين"])
        with col2:
            # هنا التعديل: استبدلنا 0.0 بـ None عشان الخانة تظهر فاضية
            w = st.number_input("العرض الكلي", value=None, placeholder="أدخل العرض")
            h = st.number_input("الارتفاع الكلي", value=None, placeholder="أدخل الارتفاع")
            d = st.number_input("العمق الكلي", value=None, placeholder="أدخل العمق")

        st.markdown("<hr style='border-color: #334155;'>", unsafe_allow_html=True)
        
        st.markdown("<p style='color:#2ecc71; font-weight:bold;'>🧱 تفاصيل الرفوف والفواصل والأدراج</p>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.caption("الرفوف")
            sh_w = st.number_input("عرض الرف", value=None, placeholder="0.0")
            sh_d = st.number_input("عمق الرف", value=None, placeholder="0.0")
            sh_n = st.number_input("عدد الرفوف", value=None, placeholder="0", step=1)
        with c2:
            st.caption("الفواصل")
            dv_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="0.0")
            dv_d = st.number_input("عمق الفاصل", value=None, placeholder="0.0")
            dv_n = st.number_input("عدد الفواصل", value=None, placeholder="0", step=1)
        with c3:
            st.caption("الأدراج")
            dr_w = st.number_input("عرض الدرج", value=None, placeholder="0.0")
            dr_d = st.number_input("عمق الدرج", value=None, placeholder="0.0")
            dr_n = st.number_input("عدد الأدراج", value=None, placeholder="0", step=1)

        if st.button("💾 تنفيذ التخصيم وإضافة للجدول"):
            # التأكد إن المستخدم دخل القيم الأساسية
            if w is not None and h is not None and d is not None:
                h_baky = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                w_baky, d_baky = w - 5, d - 5
                
                # معالجة القيم الاختيارية لو سابها فاضية (تعتبر صفر في الحسابات)
                sh_n_val = sh_n if sh_n is not None else 0
                dv_n_val = dv_n if dv_n is not None else 0
                dr_n_val = dr_n if dr_n is not None else 0
                
                unit = {
                    'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
                    'h_baky': h_baky, 'w_baky': w_baky, 'd_baky': d_baky,
                    'sh_n': sh_n_val, 'dv_n': dv_n_val, 'dr_n': dr_n_val
                }
                st.session_state.storage.append(unit)
                st.success("تم الحساب والإضافة!")
            else:
                st.warning("لازم تدخل العرض والارتفاع والعمق الأول!")

    if st.session_state.storage:
        for u in st.session_state.storage:
            with st.expander(f"✅ {u['title']}"):
                st.markdown(f'<div class="result-card">ارتفاع: {u["h_baky"]} | عرض: {u["w_baky"]} | عمق: {u["d_baky"]}</div>', unsafe_allow_html=True)

    if st.button("🔄 مشروع جديد"):
        st.session_state.started = False
        st.session_state.storage = []
        st.rerun()
