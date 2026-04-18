import streamlit as st
import pandas as pd

# 1. إعداد واجهة الصفحة
st.set_page_config(page_title="نظام تخصيم الألومنيوم - نسخة الورشة", layout="wide")

# CSS لجعل الصفحة تدعم اللغة العربية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }
    .stCodeBlock { direction: ltr; }
    </style>
    """, unsafe_allow_html=True)

# 2. تعريف مخزن البيانات (بديل self.project_storage)
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

st.title("🏗️ نظام تخصيم الألومنيوم - نسخة الورشة النهائية")

# --- زر الجرد الإجمالي (في الأعلى كما في كودك) ---
if st.button("📊 جرد خامات المشروع بالكامل (فاتورة قص)", type="primary", use_container_width=True):
    if not st.session_state.project_storage:
        st.warning("⚠️ لا توجد بيانات في الجدول!")
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

        # عرض فاتورة الجرد النهائي (بديلة لـ SummaryDialog)
        st.success("📊 فاتورة جرد خامات المشروع")
        st.markdown(f"""
        ```text
        📊 جرد الخامات النهائي للمشروع:
        ━━━━━━━━━━━━━━━━━━━━━
        🔹 ألومنيوم مفرد:   {m_sum/600:.2f} عود
        🔹 ألومنيوم متقارب: {t_sum/600:.2f} عود
        🔹 فيبر (2.8*1.3):  {f_area/36400:.2f} لوح
        ━━━━━━━━━━━━━━━━━━━━━
        ```
        """)

# --- قسم المدخلات (بديل input_group) ---
st.subheader("📝 مدخلات المقاسات")
with st.container():
    col_u1, col_u2 = st.columns([3, 1])
    unit_title = col_u1.text_input("اسم الوحدة", key="unit_title")
    unit_type = col_u2.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"], key="unit_type")
    
    c1, c2, c3 = st.columns(3)
    w = c1.number_input("العرض الكلي", step=0.1, key="w")
    h = c2.number_input("الارتفاع الكلي", step=0.1, key="h")
    d = c3.number_input("العمق الكلي", step=0.1, key="d")

    s1, s2, s3 = st.columns(3)
    sh_w = s1.number_input("الرف (عرض)", step=0.1, key="sh_w")
    sh_d = s2.number_input("الرف (عمق)", step=0.1, key="sh_d")
    sh_n = s3.number_input("الرفوف (عدد)", step=1, key="sh_n")

    v1, v2, v3 = st.columns(3)
    dv_h = v1.number_input("الفاصل (ارتفاع)", step=0.1, key="dv_h")
    dv_d = v2.number_input("الفاصل (عمق)", step=0.1, key="dv_d")
    dv_n = v3.number_input("الفواصل (عدد)", step=1, key="dv_n")

    r1, r2, r3 = st.columns(3)
    dr_w = r1.number_input("الدرج (عرض)", step=0.1, key="dr_w")
    dr_d = r2.number_input("الدرج (عمق)", step=0.1, key="dr_d")
    dr_n = r3.number_input("الأدراج (عدد)", step=1, key="dr_n")

# --- أزرار التحكم ---
btn_col1, btn_col2 = st.columns(2)
if btn_col1.button("💾 إضافة للجدول", use_container_width=True):
    try:
        u = {
            'title': unit_title or "وحدة", 'type': unit_type,
            'w': float(w), 'h': float(h), 'd': float(d),
            'sh_w': float(sh_w), 'sh_d': float(sh_d), 'sh_n': int(sh_n),
            'dv_h': float(dv_h), 'dv_d': float(dv_d), 'dv_n': int(dv_n),
            'dr_w': float(dr_w), 'dr_d': float(dr_d), 'dr_n': int(dr_n)
        }
        st.session_state.project_storage.append(u)
        st.toast(f"تمت إضافة {u['title']}")
    except Exception as e:
        st.error(f"خطأ: {e}")

if btn_col2.button("🗑️ مسح الكل", use_container_width=True):
    st.session_state.project_storage = []
    st.rerun()

# --- العرض (بديل result_sheet و TableWidget) ---
st.divider()
display_col_txt, display_col_tbl = st.columns([7, 3])

with display_col_tbl:
    st.subheader("📋 جدول الوحدات")
    if st.session_state.project_storage:
        df = pd.DataFrame(st.session_state.project_storage)
        st.dataframe(df[['title', 'w', 'h', 'd']], hide_index=True)

with display_col_txt:
    st.subheader("📑 بيان التقطيع")
    for u in st.session_state.project_storage:
        h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_baky, d_baky = u['w'] - 5, u['d'] - 5

        # بناء النص بنفس أسلوبك بالضبط في PyQt5
        txt = f"📦 {u['title']} | النوع: {u['type']} | {u['w']}x{u['h']}x{u['d']}\n"
        txt += "━" * 40 + "\n"
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
        
        # ... يمكنك إضافة الفواصل والأدراج بنفس النمط هنا ...

        st.code(txt, language="text")
