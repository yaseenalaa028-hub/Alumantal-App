import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="نظام تخصيم الألومنيوم - برمجة البرنس", layout="wide")

# الهيدر الاحترافي باسمك الجديد
st.markdown("""
    <style>
    .main-header {
        text-align: center; 
        color: #fbc531; 
        background-color: #2f3640; 
        padding: 20px; 
        border-radius: 15px; 
        border-bottom: 5px solid #e1b12c;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #27ae60;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
    }
    </style>
    <div class="main-header">
        <h1>نظام تخصيم الألومنيوم 🏗️</h1>
        <h2>برمجة البرنس</h2>
    </div>
    """, unsafe_allow_html=True)

# تهيئة مخزن البيانات في المتصفح
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# --- منطقة المدخلات ---
st.markdown("### 📝 مدخلات المقاسات (برمجة البرنس)")
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        unit_title = st.text_input("اسم الوحدة", value="وحدة 1")
        w = st.number_input("العرض الكلي", min_value=0.0, step=0.1)
        sh_w = st.number_input("عرض الرف", min_value=0.0, step=0.1)
        dr_w = st.number_input("عرض الدرج", min_value=0.0, step=0.1)

    with col2:
        unit_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        h = st.number_input("الارتفاع الكلي", min_value=0.0, step=0.1)
        sh_d = st.number_input("عمق الرف", min_value=0.0, step=0.1)
        dr_d = st.number_input("عمق الدرج", min_value=0.0, step=0.1)

    with col3:
        d = st.number_input("العمق الكلي", min_value=0.0, step=0.1)
        sh_n = st.number_input("عدد الرفوف", min_value=0, step=1)
        dv_n = st.number_input("عدد الفواصل", min_value=0, step=1)
        dr_n = st.number_input("عدد الأدراج", min_value=0, step=1)

# --- تنفيذ الحسابات ---
if st.button("💾 إضافة للجدول وحساب التخصيم", use_container_width=True):
    if w > 0 and h > 0:
        # معادلات التخصيم الخاصة بالورشة
        # السفلي ودولاب الخزين يخصم 13 سم من الارتفاع، والعلوي يخصم 5 سم
        h_baky = h - 13 if unit_type in ["سفلية", "دولاب خزين"] else h - 5
        w_baky, d_baky = w - 5, d - 5
        
        new_unit = {
            'title': unit_title, 'type': unit_type, 
            'w': w, 'h': h, 'd': d,
            'h_baky': h_baky, 'w_baky': w_baky, 'd_baky': d_baky,
            'sh_n': sh_n, 'sh_w': sh_w, 'sh_d': sh_d,
            'dr_n': dr_n, 'dr_w': dr_w, 'dr_d': dr_d,
            'dv_n': dv_n
        }
        st.session_state.project_storage.append(new_unit)
        st.success(f"تم إضافة {unit_title} بنجاح .. تسلم إيدك يا برنس!")
    else:
        st.error("يا برنس لازم تدخل العرض والارتفاع عشان أحسب!")

# --- عرض النتائج ---
if st.session_state.project_storage:
    st.divider()
    
    col_res, col_table = st.columns([2, 1])
    
    with col_res:
        st.subheader("📐 تفاصيل التخصيم والتقطيع")
        for u in st.session_state.project_storage:
            with st.expander(f"📦 تفاصيل: {u['title']} ({u['type']})"):
                st.markdown(f"""
                * **الألومنيوم (2*8):** * ارتفاع صافي: `{u['h_baky']}`
                    * عرض صافي: `{u['w_baky']}`
                    * عمق صافي: `{u['d_baky']}`
                * **الفيبر:**
                    * ضهرية: `{u['w_baky']} × {u['h_baky']}` (1)
                    * أرضية: `{u['w_baky']} × {u['d_baky']}` ({"1" if u['type']=='سفلية' else "2"})
                """)
                if u['sh_n'] > 0:
                    st.markdown(f"* **الرفوف ({u['sh_n']}):** فيبر `{u['sh_w']-5} × {u['sh_d']-5}`")
                if u['dr_n'] > 0:
                    st.markdown(f"* **الأدراج ({u['dr_n']}):** عرض ألومنيوم `{u['dr_w']-2.5}` | عمق `{u['dr_d']}`")

    with col_table:
        st.subheader("📊 الجدول")
        df = pd.DataFrame(st.session_state.project_storage)[['title', 'w', 'h', 'd']]
        st.table(df)
        if st.button("🗑️ مسح الكل"):
            st.session_state.project_storage = []
            st.rerun()

    # --- جرد خامات المشروع ---
    st.divider()
    st.markdown("### 📊 جرد خامات المشروع - برمجة البرنس")
    m_sum, t_sum, f_area = 0, 0, 0
    
    for u in st.session_state.project_storage:
        # حسابات العيدان (المخزن)
        if u['type'] == "سفلية":
            m_sum += (u['h_baky']*2)+(u['w_baky']*3)+(u['d_baky']*2)
            t_sum += (u['h_baky']*2)+(u['w_baky']*1)+(u['d_baky']*2)
            f_area += (u['w_baky']*u['h_baky']) + (u['w_baky']*u['d_baky']) + (u['h_baky']*u['d_baky']*2)
        else:
            m_sum += (u['h_baky']*2)+(u['w_baky']*2)
            t_sum += (u['h_baky']*2)+(u['w_baky']*2)+(u['d_baky']*4)
            f_area += (u['w_baky']*u['h_baky']) + (u['w_baky']*u['d_baky']*2) + (u['h_baky']*u['d_baky']*2)
            
    c1, c2, c3 = st.columns(3)
    c1.metric("ألومنيوم مفرد (عود)", f"{m_sum/600:.2f}")
    c2.metric("ألومنيوم متقارب (عود)", f"{t_sum/600:.2f}")
    c3.metric("فيبر (لوح)", f"{f_area/36400:.2f}")
