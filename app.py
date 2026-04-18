import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (الواجهة الرئيسية)
st.set_page_config(page_title="نظام تخصيم الألومنيوم - نسخة الورشة", layout="wide")

# تنسيق اللغة العربية والشكل العام
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }
    .stButton>button { width: 100%; height: 50px; font-weight: bold; font-size: 18px; border-radius: 10px; }
    .total-btn button { background-color: #d35400 !important; color: white !important; }
    .add-btn button { background-color: #27ae60 !important; color: white !important; }
    .clear-btn button { background-color: #c0392b !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة مخزن البيانات (بديل self.project_storage)
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- [الواجهة الرئيسية - الجزء العلوي] ---
st.markdown('<h1 style="text-align: center;">📊 نظام تخصيم الألومنيوم - نسخة الورشة النهائية</h1>', unsafe_allow_html=True)

# زر الجرد الإجمالي (show_project_totals)
st.markdown('<div class="total-btn">', unsafe_allow_html=True)
if st.button("📊 جرد خامات المشروع بالكامل (فاتورة قص)"):
    if not st.session_state.project_storage:
        st.warning("⚠️ لا توجد وحدات في المشروع حالياً")
    else:
        m_sum, t_sum, f_area = 0, 0, 0
        for u in st.session_state.project_storage:
            h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_b, d_b = u['w'] - 5, u['d'] - 5
            if u['type'] == "سفلية":
                m_sum += (h_b*2)+(w_b*3)+(d_b*2); t_sum += (h_b*2)+(w_b*1)+(d_b*2)
                f_area += (w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)
            else:
                m_sum += (h_b*2)+(w_b*2); t_sum += (h_b*2)+(w_b*2)+(d_b*4)
                f_area += (w_b*h_b) + (w_b*d_b*2) + (h_b*d_b*2)
            m_sum += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
            m_sum += (u['dv_h']*2 + u['dv_d']*2) * u['dv_n']
            f_area += (u['sh_w']-5)*(u['sh_d']-5)*u['sh_n'] + (u['dv_h']-5)*(u['dv_d']-5)*u['dv_n']
            m_sum += ((u['dr_w']-2.5)*2 + u['dr_d']*2) * u['dr_n']

        # نافذة الجرد (SummaryDialog)
        st.markdown(f"""
        <div style="background-color: #1e272e; color: #f1c40f; padding: 20px; border-radius: 10px; font-family: 'Consolas'; font-size: 16px;">
            <h3>📊 جرد الخامات النهائي للمشروع:</h3>
            <p>━━━━━━━━━━━━━━━━━━━━━</p>
            <p>🔹 ألومنيوم مفرد: &nbsp;&nbsp; {m_sum/600:.2f} عود</p>
            <p>🔹 ألومنيوم متقارب: {t_sum/600:.2f} عود</p>
            <p>🔹 فيبر (2.8*1.3): &nbsp; {f_area/36400:.2f} لوح</p>
            <p>━━━━━━━━━━━━━━━━━━━━━</p>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- [مدخلات المقاسات - QGroupBox] ---
st.divider()
st.subheader("📝 مدخلات المقاسات")
with st.expander("اضغط هنا لإدخال مقاسات الوحدة", expanded=True):
    col_t1, col_t2 = st.columns([2, 1])
    unit_title = col_t1.text_input("اسم الوحدة", placeholder="مثال: مطبخ علوي")
    unit_type = col_t2.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
    
    c1, c2, c3 = st.columns(3)
    w = c1.number_input("العرض الكلي", min_value=0.0, step=0.1)
    h = c2.number_input("الارتفاع الكلي", min_value=0.0, step=0.1)
    d = c3.number_input("العمق الكلي", min_value=0.0, step=0.1)

    s1, s2, s3 = st.columns(3)
    sh_w = s1.number_input("الرف (عرض)", min_value=0.0)
    sh_d = s2.number_input("الرف (عمق)", min_value=0.0)
    sh_n = s3.number_input("الرفوف (عدد)", min_value=0, step=1)

    v1, v2, v3 = st.columns(3)
    dv_h = v1.number_input("الفاصل (ارتفاع)", min_value=0.0)
    dv_d = v2.number_input("الفاصل (عمق)", min_value=0.0)
    dv_n = v3.number_input("الفواصل (عدد)", min_value=0, step=1)

    r1, r2, r3 = st.columns(3)
    dr_w = r1.number_input("الدرج (عرض)", min_value=0.0)
    dr_d = r2.number_input("الدرج (عمق)", min_value=0.0)
    dr_n = r3.number_input("الأدراج (عدد)", min_value=0, step=1)

# أزرار الإضافة والمسح (btns)
col_b1, col_b2 = st.columns(2)
with col_b1:
    st.markdown('<div class="add-btn">', unsafe_allow_html=True)
    if st.button("💾 إضافة للجدول"):
        if w > 0 and h > 0:
            u_data = {
                'title': unit_title or "وحدة", 'type': unit_type,
                'w': w, 'h': h, 'd': d, 'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n,
                'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': dv_n, 'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': dr_n
            }
            st.session_state.project_storage.append(u_data)
            st.rerun()
        else:
            st.error("⚠️ يرجى إدخال المقاسات الأساسية")
    st.markdown('</div>', unsafe_allow_html=True)

with col_b2:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("🗑️ مسح الكل"):
        st.session_state.project_storage = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- [قسم العرض - Display Layout] ---
st.divider()
display_left, display_right = st.columns([7, 3])

with display_right:
    st.subheader("📋 جدول المشروع")
    if st.session_state.project_storage:
        df = pd.DataFrame(st.session_state.project_storage)
        st.table(df[['title', 'w', 'h', 'd']])

with display_left:
    st.subheader("📑 بيان التقطيع التفصيلي")
    for u in st.session_state.project_storage:
        h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_baky, d_baky = u['w'] - 5, u['d'] - 5
        
        # بناء النص بنفس أسلوبك في PyQt5 (process_unit)
        txt = f"📦 {u['title']} | النوع: {u['type']} | {u['w']}x{u['h']}x{u['d']}\n"
        txt += "━" * 50 + "\n"
        txt += "📐 [1] تخصيم الألومنيوم (2*8):\n"
        if u['type'] == "سفلية":
            txt += f"  - ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\n"
            txt += f"  - عــــرض {w_baky}: [3 مفرد] [1 متقارب]\n"
            txt += f"  - عمــــق {d_baky}: [2 مفرد] [2 متقارب]\n"
        else:
            txt += f"  - ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\n"
            txt += f"  - عــــرض {w_baky}: [2 مفرد] [2 متقارب]\n"
            txt += f"  - عمــــق {d_baky}: [4 متقارب]\n"

        txt += f"\n🪵 [2] تخصيم الفيبر (التقطيع):\n"
        txt += f"  - ضهرية: {w_baky} × {h_baky} (1)\n"
        txt += f"  - أرضية: {w_baky} × {d_baky} ({'1' if u['type']=='سفلية' else '2'})\n"
        txt += f"  - أجناب: {h_baky} × {d_baky} (2)\n"

        if u['sh_n'] > 0:
            txt += f"\n🧱 [3] الرفوف ({u['sh_n']}):\n"
            txt += f"  - ألومنيوم: {u['sh_w']} × {u['sh_n']*2} قطعة | {u['sh_d']} × {u['sh_n']*2} قطعة [مفرد]\n"
            txt += f"  - فيبر الرف: {u['sh_w']-5} × {u['sh_d']-5} ({u['sh_n']} قطعة)\n"
        
        if u['dv_n'] > 0:
            txt += f"\n📐 [4] الفواصل ({u['dv_n']}):\n"
            txt += f"  - ألومنيوم: {u['dv_h']} × {u['dv_n']*2} قطعة | {u['dv_d']} × {u['dv_n']*2} قطعة [مفرد]\n"
            txt += f"  - فيبر الفاصل: {u['dv_h']-5} × {u['dv_d']-5} ({u['dv_n']} قطعة)\n"

        if u['dr_n'] > 0:
            txt += f"\n🗄️ [5] الأدراج ({u['dr_n']}):\n"
            txt += f"  - ألومنيوم العرض: {u['dr_w']-2.5} × {u['dr_n']*2} | العمق: {u['dr_d']} × {u['dr_n']*2}\n"

        st.code(txt, language="text")
