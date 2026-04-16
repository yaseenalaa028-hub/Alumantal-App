import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="AL-PRINCE SYSTEM", layout="centered")

# الستايل الاحترافي (أصفر + أبيض + خطوط واضحة)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 3.5em; 
        background-color: #fbc531; color: #2f3640; font-weight: bold; border: none;
    }
    .bill-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border-right: 10px solid #fbc531; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px; direction: rtl; text-align: right;
    }
    .category-title { color: #1e3799; font-weight: bold; font-size: 19px; border-bottom: 1px solid #eee; margin: 10px 0; padding-bottom: 5px; }
    .item-line { font-size: 17px; margin: 8px 0; color: #333; }
    label { color: #2f3640 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

if 'started' not in st.session_state:
    st.session_state.started = False
if 'storage' not in st.session_state:
    st.session_state.storage = []

# --- الصفحة الرئيسية ---
if not st.session_state.started:
    st.markdown("<br><br><h1 style='text-align: center;'>🏗️ نظام تخصيم الألومنيوم</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>إشراف المهندس ياسين علاء</h3><br>", unsafe_allow_html=True)
    if st.button("🚀 ابدأ التخصيم الآن"):
        st.session_state.started = True
        st.rerun()

# --- صفحة الإدخال والنتائج الكاملة ---
else:
    st.markdown("<h2 style='text-align: center;'>📝 مدخلات المقاسات</h2>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            u_title = st.text_input("اسم الوحدة", "مطبخ")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
        with col2:
            w = st.number_input("العرض الكلي", value=None)
            h = st.number_input("الارتفاع الكلي", value=None)
            d = st.number_input("العمق الكلي", value=None)

        st.divider()
        st.markdown("#### 🧱 الإضافات")
        c1, c2, c3 = st.columns(3)
        with c1:
            sh_w = st.number_input("عرض الرف", value=None)
            sh_d = st.number_input("عمق الرف", value=None)
            sh_n = st.number_input("عدد الرفوف", value=None, step=1)
        with c2:
            dv_h = st.number_input("ارتفاع الفاصل", value=None)
            dv_d = st.number_input("عمق الفاصل", value=None)
            dv_n = st.number_input("عدد الفواصل", value=None, step=1)
        with c3:
            dr_w = st.number_input("عرض الدرج", value=None)
            dr_d = st.number_input("عمق الدرج", value=None)
            dr_n = st.number_input("عدد الأدراج", value=None, step=1)

        if st.button("💾 احسب واحفظ في السجل"):
            if w and h and d:
                h_bak = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                unit = {
                    'title': u_title, 'type': u_type, 'w': w, 'h': h, 'd': d,
                    'h_bak': h_bak, 'w_bak': w-5, 'd_bak': d-5,
                    'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n if sh_n else 0,
                    'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': dv_n if dv_n else 0,
                    'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': dr_n if dr_n else 0
                }
                st.session_state.storage.append(unit)
            else:
                st.error("دخل المقاسات الأساسية الأول")

    # --- عرض النتائج "الفاتورة الكاملة" ---
    if st.session_state.storage:
        st.markdown("<br><h3 style='text-align: right;'>📋 تفاصيل القص والخامات:</h3>", unsafe_allow_html=True)
        for u in st.session_state.storage:
            st.markdown(f"""
            <div class="bill-card">
                <div style="font-size: 22px; font-weight: bold; color: #2f3640;">📦 {u['title']} ({u['type']})</div>
                
                <div class="category-title">📐 مقاسات الألومنيوم (2*8)</div>
                <div class="item-line">• الارتفاع: {u['h_bak']} سم (2 مفرد + 2 متقارب)</div>
                <div class="item-line">• العرض: {u['w_bak']} سم (3 مفرد + 1 متقارب)</div>
                <div class="item-line">• العمق: {u['d_bak']} سم (2 مفرد + 2 متقارب)</div>
                
                <div class="category-title">🪵 مقاسات الفيبر</div>
                <div class="item-line">• الضهرية: {u['w_bak']} × {u['h_bak']} (1)</div>
                <div class="item-line">• الأرضية: {u['w_bak']} × {u['d_bak']} (1)</div>
                <div class="item-line">• الأجناب: {u['h_bak']} × {u['d_bak']} (2)</div>
            """, unsafe_allow_html=True)
            
            # عرض الإضافات لو موجودة
            if u['sh_n'] > 0:
                st.markdown(f'<div class="category-title">🧱 الرفوف</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="item-line">• {u["sh_w"]} × {u["sh_d"]} (عدد {u["sh_n"]})</div>', unsafe_allow_html=True)
            if u['dv_n'] > 0:
                st.markdown(f'<div class="category-title">🧱 الفواصل</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="item-line">• {u["dv_h"]} × {u["dv_d"]} (عدد {u["dv_n"]})</div>', unsafe_allow_html=True)
            if u['dr_n'] > 0:
                st.markdown(f'<div class="category-title">🧱 الأدراج</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="item-line">• {u["dr_w"]} × {u["dr_d"]} (عدد {u["dr_n"]})</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🗑️ مسح الكل وابدأ جديد"):
        st.session_state.storage = []
        st.rerun()
