import streamlit as st

# إعدادات الصفحة والستايل
st.set_page_config(page_title="نظام ياسين علاء للألومنيوم", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #27ae60; color: white; font-weight: bold; }
    .report-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border-right: 8px solid #fbc531; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .metric-box { background-color: #2f3640; color: #fbc531; padding: 15px; border-radius: 10px; text-align: center; }
    h1, h2, h3 { text-align: right; font-family: 'Segoe UI'; }
    div[data-testid="stExpander"] { border: 1px solid #dcdde1; border-radius: 10px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<div style="background-color: #2f3640; color: #fbc531; font-size: 28px; font-weight: bold; padding: 20px; border-radius: 10px; text-align: center;">📊 نظام تخصيم الألومنيوم | برمجة م/ ياسين علاء</div>', unsafe_allow_html=True)
st.write("")

# إدارة البيانات
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- منطقة المدخلات ---
with st.container():
    st.markdown("### 📝 مدخلات المقاسات")
    c1, c2, c3 = st.columns(3)
    with c1:
        title = st.text_input("اسم الوحدة", "مطبخ - وحدة 1")
        u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
    with c2:
        w = st.number_input("العرض الكلي (سم)", 0.0, step=0.1)
        h = st.number_input("الارتفاع الكلي (سم)", 0.0, step=0.1)
    with c3:
        d = st.number_input("العمق الكلي (سم)", 0.0, step=0.1)
        sh_n = st.number_input("عدد الرفوف", 0, step=1)

    # زر الإضافة
    if st.button("➕ إضافة الوحدة للحسابات"):
        if w > 0 and h > 0:
            # نفس تخصيماتك بالضبط
            h_baky = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
            w_baky = w - 5
            d_baky = d - 5
            
            unit = {
                "title": title, "type": u_type, "w": w, "h": h, "d": d,
                "h_baky": h_baky, "w_baky": w_baky, "d_baky": d_baky, "sh_n": sh_n
            }
            st.session_state.project_storage.append(unit)
            st.toast(f"تمت إضافة {title}", icon='✅')
        else:
            st.error("دخل المقاسات الأول يا هندسة!")

# --- عرض النتائج والجرد ---
if st.session_state.project_storage:
    st.divider()
    
    # الجرد في الجنب (Sidebar)
    st.sidebar.markdown("### 📊 إجمالي جرد المشروع")
    m_sum, t_sum, f_area = 0, 0, 0
    
    for u in st.session_state.project_storage:
        if u['type'] == "سفلية":
            m_sum += (u['h_baky']*2)+(u['w_baky']*3)+(u['d_baky']*2)
            t_sum += (u['h_baky']*2)+(u['w_baky']*1)+(u['d_baky']*2)
            f_area += (u['w_baky']*u['h_baky']) + (u['w_baky']*u['d_baky']) + (u['h_baky']*u['d_baky']*2)
        else:
            m_sum += (u['h_baky']*2)+(u['w_baky']*2)
            t_sum += (u['h_baky']*2)+(u['w_baky']*2)+(u['d_baky']*4)
            f_area += (u['w_baky']*u['h_baky']) + (u['w_baky']*u['d_baky']*2) + (u['h_baky']*u['d_baky']*2)
        
        # إضافة رفوف لو وجدت
        m_sum += (u['sh_n'] * 2 * ( (u['w']-5) + (u['d']-5) ))

    with st.sidebar:
        st.markdown(f'<div class="metric-box">📏 ألومنيوم مفرد<br><h2>{m_sum/600:.2f} عود</h2></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown(f'<div class="metric-box">📏 ألومنيوم متقارب<br><h2>{t_sum/600:.2f} عود</h2></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown(f'<div class="metric-box">🪵 فيبر (لوح)<br><h2>{f_area/36400:.2f} لوح</h2></div>', unsafe_allow_html=True)
        st.write("")
        if st.button("🗑️ مسح كل البيانات", type="secondary"):
            st.session_state.project_storage = []
            st.rerun()

    # عرض الوحدات المضافة
    st.markdown("### 🏗️ تفاصيل التخصيم")
    for idx, u in enumerate(st.session_state.project_storage):
        with st.expander(f"وحدة: {u['title']} | النوع: {u['type']}"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**📐 مقاسات الألومنيوم:**")
                st.info(f"الارتفاع: {u['h_baky']} سم\n\nالعرض: {u['w_baky']} سم\n\nالعمق: {u['d_baky']} سم")
            with col_b:
                st.markdown("**🪵 مقاسات الفيبر:**")
                st.success(f"الضهرية: {u['w_baky']} × {u['h_baky']}\n\nالأرضية: {u['w_baky']} × {u['d_baky']}\n\nالأجناب: {u['h_baky']} × {u['d_baky']} (2 قطعة)")
