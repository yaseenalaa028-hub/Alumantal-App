import streamlit as st

# إعدادات الصفحة بصمة م/ ياسين علاء
st.set_page_config(page_title="نظام تخصيم الألومنيوم - ياسين علاء", layout="centered")

# الستايل اللي فيه "الأصفر" والأسود الاحترافي
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    /* الزرار الرئيسي باللون الأصفر والخط الأسود */
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background-color: #fbc531; color: #2f3640; 
        font-weight: bold; font-size: 18px; border: 2px solid #e1b12c;
    }
    .stButton>button:hover { background-color: #2f3640; color: #fbc531; }
    
    /* مربعات الإدخال */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border: 1px solid #fbc531 !important;
    }
    
    /* العناوين */
    h1 { text-align: center; color: #2f3640; border-bottom: 3px solid #fbc531; padding-bottom: 10px; }
    h4 { color: #2f3640; border-right: 5px solid #fbc531; padding-right: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'started' not in st.session_state:
    st.session_state.started = False
if 'storage' not in st.session_state:
    st.session_state.storage = []

# --- الصفحة الرئيسية ---
if not st.session_state.started:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1>🏗️ نظام تخصيم الألومنيوم</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>إشراف المهندس ياسين علاء</h3>", unsafe_allow_html=True)
    if st.button("🚀 ابدأ التخصيم الآن"):
        st.session_state.started = True
        st.rerun()

# --- صفحة إدخال البيانات (الأصفر شغال والمربعات فاضية) ---
else:
    st.markdown("<h1>📝 لوحة البيانات</h1>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            u_title = st.text_input("اسم الوحدة", placeholder="مثال: مطبخ سفلي")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
        with col2:
            # المربعات فاضية اهيه يا هندسة (None)
            w = st.number_input("العرض الكلي (سم)", value=None)
            h = st.number_input("الارتفاع الكلي (سم)", value=None)
            d = st.number_input("العمق الكلي (سم)", value=None)

        st.divider()
        
        st.markdown("#### 🧱 تفاصيل الإضافات")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write("**الرفوف**")
            sh_w = st.number_input("عرض الرف", value=None)
            sh_d = st.number_input("عمق الرف", value=None)
            sh_n = st.number_input("عدد الرفوف", value=None, step=1)
        with c2:
            st.write("**الفواصل**")
            dv_h = st.number_input("ارتفاع الفاصل", value=None)
            dv_d = st.number_input("عمق الفاصل", value=None)
            dv_n = st.number_input("عدد الفواصل", value=None, step=1)
        with c3:
            st.write("**الأدراج**")
            dr_w = st.number_input("عرض الدرج", value=None)
            dr_d = st.number_input("عمق الدرج", value=None)
            dr_n = st.number_input("عدد الأدراج", value=None, step=1)

        st.write("")
        if st.button("💾 احسب التخصيم واحفظ"):
            if w and h and d:
                # تطبيق قوانين الورشة (الـ 13 سم والـ 5 سم)
                h_baky = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                w_baky, d_baky = w - 5, d - 5
                
                unit = {
                    'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
                    'h_baky': h_baky, 'w_baky': w_baky, 'd_baky': d_baky,
                    'sh_n': sh_n if sh_n else 0,
                    'dv_n': dv_n if dv_n else 0,
                    'dr_n': dr_n if dr_n else 0
                }
                st.session_state.storage.append(unit)
                st.success("تم الحفظ في السجل")
            else:
                st.error("أدخل المقاسات الأساسية الأول")

    # عرض النتائج
    if st.session_state.storage:
        st.markdown("#### 📋 السجل الحالي")
        for u in st.session_state.storage:
            with st.expander(f"📦 {u['title']} - {u['type']}"):
                st.warning(f"الارتفاع المخصوم: {u['h_baky']} | العرض المخصوم: {u['w_baky']} | العمق المخصوم: {u['d_baky']}")

    if st.button("🔄 ابدأ مشروع جديد"):
        st.session_state.started = False
        st.session_state.storage = []
        st.rerun()
