import streamlit as st

st.set_page_config(page_title="AL-PRINCE SYSTEM", layout="wide")

# ستايل الورشة الاحترافي
st.markdown("""
    <style>
    .main { background-color: #f1f2f6; }
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background-color: #fbc531; color: #2f3640; font-weight: bold; border: 2px solid #2f3640;
    }
    .report-card {
        background-color: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); direction: rtl; text-align: right;
        border-right: 12px solid #fbc531; margin-bottom: 20px;
    }
    .title-line { font-size: 26px; font-weight: bold; color: #1e3799; border-bottom: 3px solid #fbc531; padding-bottom: 5px; }
    .section-label { color: #c0392b; font-size: 22px; margin-top: 20px; font-weight: bold; border-right: 5px solid #c0392b; padding-right: 10px; }
    .data-line { font-size: 20px; margin: 12px 0; color: #2d3436; font-weight: bold; }
    .highlight { color: #2980b9; }
    </style>
    """, unsafe_allow_html=True)

if 'storage' not in st.session_state:
    st.session_state.storage = []

st.markdown("<h1 style='text-align: center;'>🏗️ نظام التخصيم الفني (النسخة المعتمدة)</h1>", unsafe_allow_html=True)

# --- إدخال البيانات ---
with st.expander("📝 إضافة مقاسات جديدة", expanded=True):
    u_title = st.text_input("اسم القطعة")
    u_type = st.selectbox("تصنيف الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "وحدة أخرى"])
    
    col1, col2, col3 = st.columns(3)
    with col1: w = st.number_input("إجمالي العرض (سم)", value=None)
    with col2: h = st.number_input("إجمالي الارتفاع (سم)", value=None)
    with col3: d = st.number_input("إجمالي العمق (سم)", value=None)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1: sh_n = st.number_input("عدد الأرفف", value=0)
    with c2: dv_n = st.number_input("عدد الفواصل", value=0)
    with c3: dr_n = st.number_input("عدد الأدراج", value=0)

    if st.button("💾 استخراج شيت القص التفصيلي"):
        if w and h and d:
            # تطبيق قواعد التخصيم الصارمة
            # 1. تخصيم الارتفاع
            h_clean = h - 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else h - 5
            w_clean = w - 5
            d_clean = d - 5

            unit = {
                'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
                'h_c': h_clean, 'w_c': w_clean, 'd_c': d_clean,
                'sh_n': sh_n, 'dv_n': dv_n, 'dr_n': dr_n
            }
            st.session_state.storage.append(unit)
        else:
            st.error("أدخل المقاسات أولاً")

# --- عرض النتائج (شيت القص) ---
if st.session_state.storage:
    for u in st.session_state.storage:
        st.markdown(f"""
        <div class="report-card">
            <div class="title-line">📄 شيت تفصيل: {u['title']} ({u['type']})</div>
            
            <div class="section-label">🪵 أولاً: مقاسات الفيبر (الصافي)</div>
            <div class="data-line">📏 الضهرية: <span class="highlight">{u['w_c']} × {u['h_c']}</span> (عدد 1)</div>
            <div class="data-line">📏 الأرضية: <span class="highlight">{u['w_c']} × {u['d_c']}</span> (عدد 1)</div>
            <div class="data-line">📏 الأجناب: <span class="highlight">{u['h_c']} × {u['d_c']}</span> (عدد 2)</div>
        """, unsafe_allow_html=True)

        if u['sh_n'] > 0:
            st.markdown(f'<div class="data-line">📏 الرفوف (فيبر): <span class="highlight">{u["w_c"]-5} × {u["d_c"]-5}</span> (عدد {u["sh_n"]})</div>', unsafe_allow_html=True)
        if u['dv_n'] > 0:
            st.markdown(f'<div class="data-line">📏 الفواصل (فيبر): <span class="highlight">{u["w_c"]-5} × {u["d_c"]-5}</span> (عدد {u["dv_n"]})</div>', unsafe_allow_html=True)
        if u['dr_n'] > 0:
            st.markdown(f'<div class="data-line">📏 الأدراج: العرض <span class="highlight">{u["w"]-2.5}</span> | العمق <span class="highlight">{u["d"]}</span> (عدد {u["dr_n"]})</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">📐 ثانياً: مقاسات الألومنيوم (قطاع 2*8)</div>', unsafe_allow_html=True)
        
        # الارتفاع ثابت لكل الوحدات
        st.markdown(f'<div class="data-line">🛠️ الارتفاع: {u["h_c"]} سم <span class="highlight">(2 مفرد + 2 متقارب)</span></div>', unsafe_allow_html=True)
        
        # العرض والعمق يختلف حسب النوع
        if u['type'] == "وحدة سفلية":
            st.markdown(f'<div class="data-line">🛠️ العرض: {u["w_c"]} سم <span class="highlight">(3 مفرد + 1 متقارب)</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="data-line">🛠️ العمق: {u["d_c"]} سم <span class="highlight">(2 مفرد + 2 متقارب)</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="data-line">🛠️ العرض: {u["w_c"]} سم <span class="highlight">(2 مفرد + 2 متقارب)</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="data-line">🛠️ العمق: {u["d_c"]} سم <span class="highlight">(4 متقارب)</span></div>', unsafe_allow_html=True)

        # إضافة ألومنيا الرفوف والفواصل
        if u['sh_n'] > 0 or u['dv_n'] > 0:
            count = (u['sh_n'] + u['dv_n']) * 4
            st.markdown(f'<div class="data-line">🛠️ ألومنيا الرفوف/الفواصل: {u["d_c"]} سم <span class="highlight">({count} قطعة مفرد)</span></div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

if st.button("🔄 تصفير الشيت وبدء جديد"):
    st.session_state.storage = []
    st.rerun()
