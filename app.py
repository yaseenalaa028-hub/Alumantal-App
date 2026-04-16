import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="برمجة المهندس ياسين علاء", layout="wide")

# العنوان بتنسيق شيك
st.markdown("""
    <style>
    .main-header {background-color: #2f3640; color: #fbc531; font-size: 30px; font-weight: bold; 
                 padding: 20px; border-radius: 10px; text-align: center; border-bottom: 5px solid #e1b12c;}
    </style>
    <div class="main-header">نظام تخصيم الألومنيوم - برمجة م/ ياسين علاء</div>
    """, unsafe_allow_html=True)

# تهيئة المخزن في الجلسة (Session State)
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# تقسيم الشاشة لمدخلات
col1, col2, col3 = st.columns(3)

with col1:
    title = st.text_input("اسم الوحدة", "وحدة جديدة")
    u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
    w = st.number_input("العرض الكلي (سم)", 0.0)

with col2:
    h = st.number_input("الارتفاع الكلي (سم)", 0.0)
    d = st.number_input("العمق الكلي (سم)", 0.0)
    sh_n = st.number_input("عدد الرفوف", 0)

with col3:
    dr_n = st.number_input("عدد الأدراج", 0)
    dr_w = st.number_input("عرض الدرج", 0.0)
    dr_d = st.number_input("عمق الدرج", 0.0)

if st.button("➕ إضافة للجدول واحسب التخصيم"):
    # الحسابات بناءً على معادلات كود ياسين علاء
    h_baky = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
    w_baky = w - 5
    d_baky = d - 5
    
    unit_data = {
        "title": title, "type": u_type, "w": w, "h": h, "d": d,
        "h_baky": h_baky, "w_baky": w_baky, "d_baky": d_baky,
        "sh_n": sh_n, "dr_n": dr_n, "dr_w": dr_w, "dr_d": dr_d
    }
    st.session_state.project_storage.append(unit_data)
    st.success(f"تمت إضافة {title} بنجاح!")

# عرض النتائج والجرد
if st.session_state.project_storage:
    st.divider()
    st.header("📋 تفاصيل المشروع والجرد")
    
    m_sum, t_sum, f_area = 0, 0, 0
    
    for u in st.session_state.project_storage:
        with st.expander(f"📦 {u['title']} - {u['type']} ({u['w']}x{u['h']})"):
            st.write(f"📐 **تخصيم الألومنيوم:**")
            st.write(f"- ارتفاع {u['h_baky']} | عرض {u['w_baky']} | عمق {u['d_baky']}")
            st.write(f"🪵 **تخصيم الفيبر:**")
            st.write(f"- ضهرية: {u['w_baky']}x{u['h_baky']} | أجناب: {u['h_baky']}x{u['d_baky']}")

        # حسابات الجرد التراكمية (نفس معادلاتك)
        if u['type'] == "سفلية":
            m_sum += (u['h_baky']*2)+(u['w_baky']*3)+(u['d_baky']*2)
            t_sum += (u['h_baky']*2)+(u['w_baky']*1)+(u['d_baky']*2)
            f_area += (u['w_baky']*u['h_baky']) + (u['w_baky']*u['d_baky']) + (u['h_baky']*u['d_baky']*2)
        else:
            m_sum += (u['h_baky']*2)+(u['w_baky']*2)
            t_sum += (u['h_baky']*2)+(u['w_baky']*2)+(u['d_baky']*4)
            f_area += (u['w_baky']*u['h_baky']) + (u['w_baky']*u['d_baky']*2) + (u['h_baky']*u['d_baky']*2)

    # عرض الفاتورة النهائية
    st.sidebar.header("📊 فاتورة جرد الخامات")
    st.sidebar.metric("ألومنيوم مفرد (عود)", f"{m_sum/600:.2f}")
    st.sidebar.metric("ألومنيوم متقارب (عود)", f"{t_sum/600:.2f}")
    st.sidebar.metric("فيبر (لوح)", f"{f_area/36400:.2f}")

if st.button("🗑️ مسح الكل"):
    st.session_state.project_storage = []
    st.rerun()
