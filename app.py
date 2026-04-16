import streamlit as st

# إعدادات الصفحة - بصمة المهندس ياسين علاء
st.set_page_config(page_title="نظام تخصيم الألومنيوم - م/ ياسين علاء", layout="wide")

# تصميم الواجهة بالألوان اللي كانت في كودك (الأسود والأصفر والأخضر)
st.markdown("""
    <style>
    .main { background-color: #1e272e; }
    div[data-testid="stMetricValue"] { color: #f1c40f !important; }
    .stButton>button { background-color: #27ae60; color: white; font-weight: bold; border-radius: 5px; height: 3em; }
    .header-box { background-color: #2f3640; color: #fbc531; padding: 20px; border-radius: 10px; text-align: center; border-bottom: 4px solid #e1b12c; margin-bottom: 20px; }
    .result-box { background-color: #ffffff; color: #2c3e50; padding: 15px; border-radius: 5px; font-family: 'Courier New'; border-right: 5px solid #27ae60; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="header-box"><h1>نظام تخصيم الألومنيوم - برمجة م/ ياسين علاء</h1></div>', unsafe_allow_html=True)

# إدارة البيانات
if 'storage' not in st.session_state:
    st.session_state.storage = []

# --- منطقة المدخلات (نفس ترتيب كودك بالظبط) ---
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        u_title = st.text_input("اسم الوحدة", "مطبخ - وحدة 1")
        u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        w = st.number_input("العرض الكلي", 0.0)
    with col2:
        h = st.number_input("الارتفاع الكلي", 0.0)
        d = st.number_input("العمق الكلي", 0.0)
        sh_n = st.number_input("عدد الرفوف", 0)
    with col3:
        dv_n = st.number_input("عدد الفواصل", 0)
        dr_n = st.number_input("عدد الأدراج", 0)
        dr_w = st.number_input("عرض الدرج", 0.0)

# زر الإضافة (Enter)
if st.button("💾 إضافة للجدول والحساب"):
    if w > 0 and h > 0:
        # معادلات التخصيم من كودك الأصلي بالمللي
        h_baky = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
        w_baky, d_baky = w - 5, d - 5
        
        # تجميع البيانات
        unit = {
            'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
            'h_baky': h_baky, 'w_baky': w_baky, 'd_baky': d_baky,
            'sh_n': sh_n, 'dv_n': dv_n, 'dr_n': dr_n, 'dr_w': dr_w
        }
        st.session_state.storage.append(unit)
    else:
        st.error("برجاء مراجعة المقاسات يا هندسة")

# --- عرض النتائج (الفاتورة والجرد) ---
if st.session_state.storage:
    st.divider()
    
    # حسابات الجرد الكلي (نفس معادلات calculate_project_data في كودك)
    m_sum, t_sum, f_area = 0, 0, 0
    
    for u in st.session_state.storage:
        # حسابات الألومنيوم والفيبر لكل وحدة
        if u['type'] == "سفلية":
            m_sum += (u['h_baky']*2)+(u['w_baky']*3)+(u['d_baky']*2)
            t_sum += (u['h_baky']*2)+(u['w_baky']*1)+(u['d_baky']*2)
            f_area += (u['w_baky']*u['h_baky']) + (u['w_baky']*u['d_baky']) + (u['h_baky']*u['d_baky']*2)
        else:
            m_sum += (u['h_baky']*2)+(u['w_baky']*2)
            t_sum += (u['h_baky']*2)+(u['w_baky']*2)+(u['d_baky']*4)
            f_area += (u['w_baky']*u['h_baky']) + (u['w_baky']*u['d_baky']*2) + (u['h_baky']*u['d_baky']*2)
        
        # إضافة الرفوف والفواصل والأدراج للجرد
        m_sum += (u['w']-5 + u['d']-5) * 2 * u['sh_n']
        m_sum += (u['h_baky'] + u['d_baky']) * 2 * u['dv_n']
        m_sum += ((u['dr_w']-2.5)*2 + u['d_baky']*2) * u['dr_n']

    # عرض الجرد فوق بشكل ملخص (زي الـ SummaryDialog)
    c1, c2, c3 = st.columns(3)
    c1.metric("ألومنيوم مفرد (عود)", f"{m_sum/600:.2f}")
    c2.metric("ألومنيوم متقارب (عود)", f"{t_sum/600:.2f}")
    c3.metric("فيبر لوح (2.8*1.3)", f"{f_area/36400:.2f}")

    st.subheader("📋 تفاصيل التخصيم (فاتورة القص)")
    for u in st.session_state.storage:
        with st.expander(f"📦 {u['title']} | {u['type']} | {u['w']}x{u['h']}x{u['d']}"):
            st.markdown(f"""
            <div class="result-box">
            <b>📐 [1] تخصيم الألومنيوم (2*8):</b><br>
            - ارتفاع {u['h_baky']}: [2 مفرد] [2 متقارب]<br>
            - عرض {u['w_baky']}: [3 مفرد] [1 متقارب]<br>
            - عمق {u['d_baky']}: [2 مفرد] [2 متقارب]<br><br>
            <b>🪵 [2] تخصيم الفيبر:</b><br>
            - ضهرية: {u['w_baky']} × {u['h_baky']} (1)<br>
            - أرضية: {u['w_baky']} × {u['d_baky']} (1)<br>
            - أجناب: {u['h_baky']} × {u['d_baky']} (2)
            </div>
            """, unsafe_allow_html=True)

    if st.button("🗑️ مسح الكل"):
        st.session_state.storage = []
        st.rerun()
