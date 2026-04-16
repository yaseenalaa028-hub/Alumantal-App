import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="نظام تخصيمات ياسين علاء", layout="wide")

# الستايل الاحترافي (أصفر ورشة + أسود هيبة)
st.markdown("""
    <style>
    .main { background-color: #f1f2f6; }
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background-color: #fbc531; color: #2f3640; font-weight: bold; border: 2px solid #2f3640; font-size: 18px;
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
if 'started' not in st.session_state:
    st.session_state.started = False

# --- 1. الواجهة الصافية (البداية) ---
if not st.session_state.started:
    st.markdown("<br><br><h1 style='text-align: center; color: #2f3640;'>🏗️ نظام تخصيم الألومنيوم</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #7f8c8d;'>إشراف المهندس ياسين علاء</h3><br>", unsafe_allow_html=True)
    if st.button("🚀 ابدأ التخصيم الآن"):
        st.session_state.started = True
        st.rerun()

# --- 2. واجهة الإدخال الكاملة (بدون حذف أي بند) ---
else:
    st.markdown("<h2 style='text-align: center;'>📝 مدخلات المقاسات</h2>", unsafe_allow_html=True)
    
    with st.container():
        col_name, col_type = st.columns(2)
        with col_name: u_title = st.text_input("اسم القطعة", placeholder="مثال: مطبخ سفلي")
        with col_type: u_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "أخرى"])
        
        st.markdown("#### 📐 المقاسات الكلية")
        c1, c2, c3 = st.columns(3)
        with c1: w = st.number_input("إجمالي العرض (سم)", value=None)
        with c2: h = st.number_input("إجمالي الارتفاع (سم)", value=None)
        with c3: d = st.number_input("إجمالي العمق (سم)", value=None)

        st.divider()
        # --- بنود الأرفف والفواصل والأدراج ---
        st.markdown("#### 🧱 بنود الإضافات (الأرفف - الفواصل - الأدراج)")
        f1, f2, f3 = st.columns(3)
        with f1:
            sh_n = st.number_input("عدد الأرفف", value=0, step=1)
        with f2:
            dv_n = st.number_input("عدد الفواصل", value=0, step=1)
        with f3:
            dr_n = st.number_input("عدد الأدراج", value=0, step=1)

        if st.button("💾 استخراج شيت القص التفصيلي"):
            if w and h and d:
                # تخصيمات الارتفاع (13 للسفلي والخزين / 5 للباقي)
                h_c = h - 13 if u_type in ["وحدة سفلية", "دولاب خزين"] else h - 5
                w_c = w - 5
                d_c = d - 5

                unit = {
                    'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
                    'h_c': h_c, 'w_c': w_c, 'd_c': d_c,
                    'sh_n': sh_n, 'dv_n': dv_n, 'dr_n': dr_n
                }
                st.session_state.storage.append(unit)
            else:
                st.error("أدخل المقاسات الأساسية الأول يا هندسة!")

    # --- 3. عرض شيت التخصيم النهائي ---
    if st.session_state.storage:
        st.markdown("<h2 style='text-align: center; color: #2f3640;'>📋 قائمة القص النهائية</h2>", unsafe_allow_html=True)
        for u in st.session_state.storage:
            st.markdown(f"""
            <div class="report-card">
                <div class="title-line">📦 {u['title']} - {u['type']}</div>
                
                <div class="section-label">🪵 تخصيم الفيبر (الخامات):</div>
                <div class="data-line">الضهرية: {u['w_c']} * {u['h_c']} * 1</div>
                <div class="data-line">الارضية: {u['w_c']} * {u['d_c']} * 1</div>
                <div class="data-line">الاجناب: {u['h_c']} * {u['d_c']} * 2</div>
            """, unsafe_allow_html=True)
            
            # تخصيم الرفوف والفواصل (فيبر - خصم 5 سم)
            if u['sh_n'] > 0:
                st.markdown(f'<div class="data-line">الارفف (فيبر): {u["w_c"]-5} * {u["d_c"]-5} * {u["sh_n"]}</div>', unsafe_allow_html=True)
            if u['dv_n'] > 0:
                st.markdown(f'<div class="data-line">الفواصل (فيبر): {u["h_c"]} * {u["d_c"]-5} * {u["dv_n"]}</div>', unsafe_allow_html=True)
            
            # تخصيم الأدراج (عرض - 2.5 والعمق ثابت)
            if u['dr_n'] > 0:
                st.markdown(f'<div class="data-line">الأدراج: {u["w"]-2.5} عرض * {u["d"]} عمق * {u["dr_n"]}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-label">📐 تخصيم الألومنيوم (2*8):</div>', unsafe_allow_html=True)
            
            # الارتفاع (ثابت 2 مفرد + 2 متقارب)
            st.markdown(f'<div class="data-line">الارتفاع: {u["h_c"]} سم (2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
            
            # العرض والعمق حسب نظامك
            if u['type'] == "وحدة سفلية":
                st.markdown(f'<div class="data-line">العرض: {u["w_c"]} سم (3 مفرد + 1 متقارب)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="data-line">العمق: {u["d_c"]} سم (2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="data-line">العرض: {u["w_c"]} سم (2 مفرد + 2 متقارب)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="data-line">العمق: {u["d_c"]} سم (4 متقارب)</div>', unsafe_allow_html=True)
            
            # ألومنيا الأرفف والفواصل (4 مفرد لكل واحد)
            if u['sh_n'] > 0 or u['dv_n'] > 0:
                sh_count = (u['sh_n'] + u['dv_n']) * 4
                st.markdown(f'<div class="data-line">ألومنيا (أرفف/فواصل): {u["d_c"]} سم ({sh_count} حتة مفرد)</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔄 مسح السجل والعودة"):
        st.session_state.storage = []
        st.session_state.started = False
        st.rerun()
