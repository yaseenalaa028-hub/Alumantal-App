import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="نظام ياسين علاء", layout="centered")

# الستايل: شيلنا كل التعقيدات وخلينا الشكل "رايق"
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background-color: #fbc531; color: #2f3640; font-weight: bold; border: none;
    }
    .result-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #fbc531;
        margin-bottom: 20px;
        direction: rtl;
    }
    .title-line { color: #1e3799; font-weight: bold; font-size: 20px; border-bottom: 2px solid #fbc531; margin-bottom: 10px; }
    .data-line { font-size: 18px; margin: 10px 0; color: #2f3640; }
    </style>
    """, unsafe_allow_html=True)

if 'started' not in st.session_state:
    st.session_state.started = False
if 'storage' not in st.session_state:
    st.session_state.storage = []

# --- الصفحة الرئيسية ---
if not st.session_state.started:
    st.markdown("<br><br><h1 style='text-align: center;'>🏗️ نظام تخصيم الألومنيوم</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>المهندس ياسين علاء</h3><br>", unsafe_allow_html=True)
    if st.button("🚀 ابدأ التخصيم"):
        st.session_state.started = True
        st.rerun()

# --- صفحة الإدخال والنتائج ---
else:
    st.markdown("<h2 style='text-align: center;'>📝 أدخل المقاسات</h2>", unsafe_allow_html=True)
    
    with st.container():
        u_title = st.text_input("اسم الوحدة", "مطبخ")
        u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
        
        c1, c2, c3 = st.columns(3)
        with c1: w = st.number_input("العرض", value=None)
        with c2: h = st.number_input("الارتفاع", value=None)
        with c3: d = st.number_input("العمق", value=None)

        if st.button("✅ احسب الآن"):
            if w and h and d:
                h_bak = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                unit = {'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d, 'h_bak': h_bak, 'w_bak': w-5, 'd_bak': d-5}
                st.session_state.storage.append(unit)
            else:
                st.error("كمل المقاسات يا هندسة")

    # --- عرض النتائج بشكل "كارت" نضيف ---
    if st.session_state.storage:
        st.markdown("<br><h3 style='text-align: right;'>📋 مقاسات القص:</h3>", unsafe_allow_html=True)
        for u in st.session_state.storage:
            st.markdown(f"""
            <div class="result-box">
                <div class="title-line">📦 {u['title']} - {u['type']}</div>
                <div class="data-line"><b>📏 الألومنيوم:</b></div>
                <div class="data-line">الارتفاع: {u['h_bak']} سم</div>
                <div class="data-line">العرض: {u['w_bak']} سم</div>
                <div class="data-line">العمق: {u['d_bak']} سم</div>
                <hr>
                <div class="data-line"><b>🪵 الفيبر:</b></div>
                <div class="data-line">الضهرية: {u['w_bak']} × {u['h_bak']}</div>
                <div class="data-line">الأرضية: {u['w_bak']} × {u['d_bak']}</div>
                <div class="data-line">الأجناب: {u['h_bak']} × {u['d_bak']} (قطعتين)</div>
            </div>
            """, unsafe_allow_html=True)

    if st.button("🗑️ مسح وابدأ من جديد"):
        st.session_state.storage = []
        st.rerun()
