import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="AL-PRINCE SYSTEM", layout="centered")

# الستايل اللي فيه "الأصفر" والأسود
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background-color: #fbc531; color: #2f3640; 
        font-weight: bold; font-size: 18px; border: 2px solid #e1b12c;
    }
    .stNumberInput>div>div>input { border: 1px solid #fbc531 !important; }
    h1 { text-align: center; color: #2f3640; border-bottom: 3px solid #fbc531; padding-bottom: 10px; }
    .bill-card { background-color: #ffffff; padding: 15px; border-radius: 10px; border-right: 8px solid #fbc531; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 15px; text-align: right; direction: rtl; }
    .section-title { color: #1e3799; font-weight: bold; margin-top: 10px; border-bottom: 1px solid #dcdde1; }
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

# --- صفحة إدخال البيانات ---
else:
    st.markdown("<h1>📝 لوحة البيانات</h1>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            u_title = st.text_input("اسم الوحدة", placeholder="مثال: مطبخ سفلي")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
        with col2:
            w = st.number_input("العرض الكلي (سم)", value=None)
            h = st.number_input("الارتفاع الكلي (سم)", value=None)
            d = st.number_input("العمق الكلي (سم)", value=None)

        st.divider()
        st.markdown("#### 🧱 الإضافات (رفوف - فواصل - أدراج)")
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

        if st.button("💾 احسب التخصيم والمقاسات"):
            if w and h and d:
                # قوانين التخصيم
                h_baky = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                w_baky, d_baky = w - 5, d - 5
                
                # حفظ البيانات والتأكد من وجود القيم لتجنب KeyError
                unit = {
                    'title': u_title if u_title else "وحدة بدون اسم",
                    'type': u_type, 'w': w, 'h': h, 'd': d,
                    'h_baky': h_baky, 'w_baky': w_baky, 'd_baky': d_baky,
                    'sh_w': sh_w if sh_w else 0, 'sh_d': sh_d if sh_d else 0, 'sh_n': sh_n if sh_n else 0,
                    'dv_h': dv_h if dv_h else 0, 'dv_d': dv_d if dv_d else 0, 'dv_n': dv_n if dv_n else 0,
                    'dr_w': dr_w if dr_w else 0, 'dr_d': dr_d if dr_d else 0, 'dr_n': dr_n if dr_n else 0
                }
                st.session_state.storage.append(unit)
                st.toast("تم حفظ الوحدة بنجاح!")
            else:
                st.error("أدخل المقاسات الأساسية (العرض والارتفاع والعمق) الأول")

    # --- عرض تفاصيل القص والخامات ---
    if st.session_state.storage:
        st.divider()
        st.markdown("### 📋 فاتورة القص وتفاصيل الخامات")
        for u in st.session_state.storage:
            with st.container():
                st.markdown(f"""
                <div class="bill-card">
                    <h3 style='color:#2f3640;'>📦 {u['title']} ({u['type']})</h3>
                    
                    <div class="section-title">📐 مقاسات الألومنيوم (2*8)</div>
                    <p>• <b>الارتفاع المخصوم:</b> {u['h_baky']} سم (2 مفرد + 2 متقارب)</p>
                    <p>• <b>العرض المخصوم:</b> {u['w_baky']} سم (3 مفرد + 1 متقارب)</p>
                    <p>• <b>العمق المخصوم:</b> {u['d_baky']} سم (2 مفرد + 2 متقارب)</p>
                    
                    <div class="section-title">🪵 مقاسات الفيبر</div>
                    <p>• <b>الضهرية:</b> {u['w_baky']} × {u['h_baky']} (قطعة 1)</p>
                    <p>• <b>الأرضية:</b> {u['w_baky']} × {u['d_baky']} (قطعة 1)</p>
                    <p>• <b>الأجناب:</b> {u['h_baky']} × {u['d_baky']} (قطعة 2)</p>
                """, unsafe_allow_html=True)
                
                # إظهار الإضافات فقط لو كانت أكبر من صفر
                if u['sh_n'] > 0:
                    st.markdown(f"<p>• <b>الرفوف:</b> {u['sh_w']} × {u['sh_d']} (عدد {u['sh_n']})</p>", unsafe_allow_html=True)
                if u['dv_n'] > 0:
                    st.markdown(f"<p>• <b>الفواصل:</b> {u['dv_h']} × {u['dv_d']} (عدد {u['dv_n']})</p>", unsafe_allow_html=True)
                if u['dr_n'] > 0:
                    st.markdown(f"<p>• <b>الأدراج:</b> {u['dr_w']} × {u['dr_d']} (عدد {u['dr_n']})</p>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔄 مسح السجل وبدء مشروع جديد"):
        st.session_state.storage = []
        st.rerun()
