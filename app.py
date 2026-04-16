import streamlit as st

# إعدادات الصفحة بصمة م/ ياسين علاء
st.set_page_config(page_title="نظام تخصيم الألومنيوم - ياسين علاء", layout="centered")

# تصميم الواجهة (الألوان والستايل)
st.markdown("""
    <style>
    .main { background-color: #f5f6fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #2f3640; color: #fbc531; font-weight: bold; font-size: 18px; border: 2px solid #fbc531; }
    .stButton>button:hover { background-color: #fbc531; color: #2f3640; }
    .input-card { background-color: #ffffff; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 20px; }
    h1 { text-align: center; color: #2f3640; font-family: 'Segoe UI'; }
    </style>
    """, unsafe_allow_html=True)

# إدارة حالة الصفحة (هل بدأنا التخصيم أم لا)
if 'started' not in st.session_state:
    st.session_state.started = False
if 'storage' not in st.session_state:
    st.session_state.storage = []

# --- الصفحة الرئيسية (الصافية) ---
if not st.session_state.started:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1>🏗️ نظام تخصيم الألومنيوم</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>برمجة المهندس ياسين علاء</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 ابدأ التخصيم الآن"):
        st.session_state.started = True
        st.rerun()

# --- صفحة إدخال البيانات (تظهر بعد الضغط على الزرار) ---
else:
    st.markdown("### 📝 مدخلات الوحدة الجديدة")
    
    with st.container():
        # الخانات الأساسية
        col1, col2 = st.columns(2)
        with col1:
            u_title = st.text_input("اسم الوحدة", "وحدة 1")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
        with col2:
            w = st.number_input("العرض الكلي", 0.0)
            h = st.number_input("الارتفاع الكلي", 0.0)
            d = st.number_input("العمق الكلي", 0.0)

        st.divider()
        
        # خانات الرفوف والفواصل والأدراج (زي ما طلبت بالترتيب)
        st.markdown("#### 🧱 تفاصيل الإضافات")
        c1, c2, c3 = st.columns(3)
        with c1:
            sh_w = st.number_input("مقاس الرف (عرض)", 0.0)
            sh_d = st.number_input("عمق الرف", 0.0)
            sh_n = st.number_input("عدد الرفوف", 0)
        with c2:
            dv_h = st.number_input("مقاس الفاصل (ارتفاع)", 0.0)
            dv_d = st.number_input("عمق الفاصل", 0.0)
            dv_n = st.number_input("عدد الفواصل", 0)
        with c3:
            dr_w = st.number_input("مقاس الدرج (عرض)", 0.0)
            dr_d = st.number_input("عمق الدرج", 0.0)
            dr_n = st.number_input("عدد الأدراج", 0)

        # زر الحفظ والحساب
        if st.button("💾 حفظ الوحدة وحساب التخصيم"):
            if w > 0 and h > 0:
                # قوانين التخصيم الخاصة بك
                h_baky = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                w_baky, d_baky = w - 5, d - 5
                
                unit = {
                    'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
                    'h_baky': h_baky, 'w_baky': w_baky, 'd_baky': d_baky,
                    'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n,
                    'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': dv_n,
                    'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': dr_n
                }
                st.session_state.storage.append(unit)
                st.success("تم الحفظ بنجاح!")
            else:
                st.error("أدخل المقاسات الأساسية الأول!")

    # عرض النتائج تحت الخانات
    if st.session_state.storage:
        st.divider()
        st.subheader("📋 فاتورة القص والجرد")
        for u in st.session_state.storage:
            with st.expander(f"📦 {u['title']} - {u['type']}"):
                st.write(f"**تخصيم الألومنيوم:** ارتفاع {u['h_baky']} | عرض {u['w_baky']} | عمق {u['d_baky']}")
                if u['sh_n'] > 0: st.write(f"**الرفوف:** عرض {u['sh_w']} | عمق {u['sh_d']} | عدد {u['sh_n']}")
                if u['dv_n'] > 0: st.write(f"**الفواصل:** ارتفاع {u['dv_h']} | عمق {u['dv_d']} | عدد {u['dv_n']}")
                if u['dr_n'] > 0: st.write(f"**الأدراج:** عرض {u['dr_w']} | عمق {u['dr_d']} | عدد {u['dr_n']}")

    if st.button("🔄 إرجاع للصفحة الرئيسية"):
        st.session_state.started = False
        st.session_state.storage = []
        st.rerun()
