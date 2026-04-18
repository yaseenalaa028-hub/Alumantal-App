import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="نظام تخصيم الألومنيوم", layout="wide")

# تهيئة المخزن في السجل (Session State)
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

st.title("📊 نظام تخصيم الألومنيوم - نسخة الويب")

# --- الجزء العلوي: الجرد الإجمالي ---
if st.button("📊 جرد خامات المشروع بالكامل (فاتورة قص)", use_container_width=True):
    if not st.session_state.project_storage:
        st.warning("المشروع فارغ! أضف وحدات أولاً.")
    else:
        m_sum, t_sum, f_area = 0, 0, 0
        for u in st.session_state.project_storage:
            h_b = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
            w_b, d_b = u['w'] - 5, u['d'] - 5
            
            if u['type'] == "سفلية":
                m_sum += (h_b*2)+(w_b*3)+(d_b*2)
                t_sum += (h_b*2)+(w_b*1)+(d_b*2)
                f_area += (w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)
            else:
                m_sum += (h_b*2)+(w_b*2)
                t_sum += (h_b*2)+(w_b*2)+(d_b*4)
                f_area += (w_b*h_b) + (w_b*d_b*2) + (h_b*d_b*2)
            
            m_sum += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
            m_sum += (u['dv_h']*2 + u['dv_d']*2) * u['dv_n']
            f_area += (u['sh_w']-5)*(u['sh_d']-5)*u['sh_n'] + (u['dv_h']-5)*(u['dv_d']-5)*u['dv_n']
            m_sum += ((u['dr_w']-2.5)*2 + u['dr_d']*2) * u['dr_n']

        st.info(f"""
        **نتائج الجرد النهائي:**
        * 🔹 ألومنيوم مفرد: **{m_sum/600:.2f}** عود
        * 🔹 ألومنيوم متقارب: **{t_sum/600:.2f}** عود
        * 🔹 فيبر (2.8*1.3): **{f_area/36400:.2f}** لوح
        """)

# --- مدخلات المقاسات ---
with st.expander("📝 مدخلات المقاسات الجديدة", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        unit_title = st.text_input("اسم الوحدة", "وحدة جديدة")
        w = st.number_input("العرض الكلي (سم)", min_value=0.0)
        sh_w = st.number_input("الرف (عرض)", min_value=0.0)
    with col2:
        unit_type = st.selectbox("النوع", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        h = st.number_input("الارتفاع الكلي (سم)", min_value=0.0)
        sh_d = st.number_input("الرف (عمق)", min_value=0.0)
    with col3:
        d = st.number_input("العمق الكلي (سم)", min_value=0.0)
        sh_n = st.number_input("عدد الرفوف", min_value=0)

    # خانات إضافية للفواصل والأدراج
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        dv_h = st.number_input("الفاصل (ارتفاع)", min_value=0.0)
        dr_w = st.number_input("الدرج (عرض)", min_value=0.0)
    with col_b:
        dv_d = st.number_input("الفاصل (عمق)", min_value=0.0)
        dr_d = st.number_input("الدرج (عمق)", min_value=0.0)
    with col_c:
        dv_n = st.number_input("عدد الفواصل", min_value=0)
        dr_n = st.number_input("عدد الأدراج", min_value=0)

    if st.button("💾 إضافة للجدول وتجهيز التخصيم"):
        new_unit = {
            'title': unit_title, 'type': unit_type, 'w': w, 'h': h, 'd': d,
            'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': int(sh_n),
            'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': int(dv_n),
            'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': int(dr_n)
        }
        st.session_state.project_storage.append(new_unit)
        st.success("تمت الإضافة!")

# --- عرض النتائج والجدول ---
col_res, col_tab = st.columns([2, 1])

with col_res:
    st.subheader("📐 مقاسات القص (تخصيمات)")
    for i, u in enumerate(st.session_state.project_storage):
        h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_baky, d_baky = u['w'] - 5, u['d'] - 5
        
        with st.container():
            st.markdown(f"**📦 {u['title']} ({u['type']})**")
            st.code(f"""
- ألومنيوم (ارتفاع {h_baky} سم): [2 مفرد] [2 متقارب]
- ألومنيوم (عرض {w_baky} سم): [2 مفرد] [2 متقارب]
- فيبر ضهرية: {w_baky} × {h_baky} (1)
- فيبر أرضية: {w_baky} × {d_baky} (1)
            """)

with col_tab:
    st.subheader("📋 قائمة الوحدات")
    if st.session_state.project_storage:
        st.table(st.session_state.project_storage)
        if st.button("🗑️ مسح كل البيانات"):
            st.session_state.project_storage = []
            st.rerun() 
# --- عرض النتائج وتفاصيل القص ---
st.divider()
col_res, col_tab = st.columns([3, 2])

with col_res:
    st.subheader("📐 تفاصيل مقاسات القص (التخصيمات)")
    for i, u in enumerate(st.session_state.project_storage):
        # منطق التخصيم (نفس اللي كان في PyQt5)
        h_baky = u['h'] - 13 if u['type'] in ["سفلية", "دولاب خزين"] else u['h'] - 5
        w_baky, d_baky = u['w'] - 5, u['d'] - 5
        
        with st.expander(f"📦 وحدة: {u['title']} - {u['w']}×{u['h']}×{u['d']}", expanded=True):
            st.markdown(f"**النوع:** {u['type']}")
            
            # عرض تخصيم الألومنيوم
            st.write("🔗 **الألومنيوم (2*8):**")
            if u['type'] == "سفلية":
                st.code(f"ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\nعرض {w_baky}: [3 مفرد] [1 متقارب]\nعمق {d_baky}: [2 مفرد] [2 متقارب]")
            else:
                st.code(f"ارتفاع {h_baky}: [2 مفرد] [2 متقارب]\nعرض {w_baky}: [2 مفرد] [2 متقارب]\nعمق {d_baky}: [4 متقارب]")
            
            # عرض تخصيم الفيبر
            st.write("🪵 **الفيبر (التقطيع):**")
            st.code(f"ضهرية: {w_baky} × {h_baky} (1)\nأرضية: {w_baky} × {d_baky} ({'1' if u['type']=='سفلية' else '2'})\nأجناب: {h_baky} × {d_baky} (2)")
            
            # الرفوف والأدراج لو موجودة
            if u['sh_n'] > 0:
                st.write(f"🧱 **الرفوف ({u['sh_n']}):**")
                st.code(f"ألومنيوم: {u['sh_w']}×2 قطعة | {u['sh_d']}×2 قطعة لكل رف\nفيبر: {u['sh_w']-5} × {u['sh_d']-5}")

with col_tab:
    st.subheader("📋 قائمة الوحدات المضافة")
    if st.session_state.project_storage:
        # تحويل القائمة لجدول بيانات
        import pandas as pd
        df = pd.DataFrame(st.session_state.project_storage)
        st.dataframe(df[['title', 'type', 'w', 'h', 'd']], use_container_width=True)
        
        if st.button("🗑️ مسح كل بيانات المشروع", type="primary"):
            st.session_state.project_storage = []
            st.rerun()
    else:
        st.info("لم يتم إضافة وحدات بعد.")
