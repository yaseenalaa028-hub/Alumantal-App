import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="نظام تخصيم الألومنيوم - المهندس ياسين علاء", layout="wide")

# الهيدر الاحترافي
st.markdown("""
    <style>
    .main-header {text-align: center; color: #fbc531; background-color: #2f3640; padding: 20px; border-radius: 10px; border-bottom: 4px solid #e1b12c;}
    </style>
    <div class="main-header">
        <h1>نظام تخصيم الألومنيوم - نسخة المهندس ياسين علاء</h1>
    </div>
    """, unsafe_allow_html=True)

# تهيئة مخزن البيانات (Session State) عشان البيانات ما تتمسحش لما الصفحة تعمل Refresh
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# قسم المدخلات
st.subheader("📝 مدخلات المقاسات")
with st.expander("اضغط هنا لإدخال بيانات وحدة جديدة", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        unit_title = st.text_input("اسم الوحدة", value="وحدة جديدة")
        w = st.number_input("العرض الكلي (W)", min_value=0.0, step=0.1)
        sh_w = st.number_input("الرف (عرض)", min_value=0.0, step=0.1)
        dv_h = st.number_input("الفاصل (ارتفاع)", min_value=0.0, step=0.1)
        dr_w = st.number_input("الدرج (عرض)", min_value=0.0, step=0.1)

    with col2:
        unit_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
        h = st.number_input("الارتفاع الكلي (H)", min_value=0.0, step=0.1)
        sh_d = st.number_input("الرف (عمق)", min_value=0.0, step=0.1)
        dv_d = st.number_input("الفاصل (عمق)", min_value=0.0, step=0.1)
        dr_d = st.number_input("الدرج (عمق)", min_value=0.0, step=0.1)

    with col3:
        st.write("") # فاصل
        d = st.number_input("العمق الكلي (D)", min_value=0.0, step=0.1)
        sh_n = st.number_input("الرفوف (عدد)", min_value=0, step=1)
        dv_n = st.number_input("الفواصل (عدد)", min_value=0, step=1)
        dr_n = st.number_input("الأدراج (عدد)", min_value=0, step=1)

    if st.button("💾 إضافة للجدول وحساب التخصيم", use_container_width=True):
        if w > 0 and h > 0:
            # منطق الحسابات (نفس اللي كان في كود PyQt)
            h_baky = h - 13 if unit_type in ["سفلية", "دولاب خزين"] else h - 5
            w_baky, d_baky = w - 5, d - 5
            
            new_unit = {
                'title': unit_title, 'type': unit_type, 'w': w, 'h': h, 'd': d,
                'h_baky': h_baky, 'w_baky': w_baky, 'd_baky': d_baky,
                'sh_n': sh_n, 'sh_w': sh_w, 'sh_d': sh_d,
                'dv_n': dv_n, 'dv_h': dv_h, 'dv_d': dv_d,
                'dr_n': dr_n, 'dr_w': dr_w, 'dr_d': dr_d
            }
            st.session_state.project_storage.append(new_unit)
            st.success(f"تمت إضافة {unit_title} بنجاح!")
        else:
            st.error("يرجى إدخال العرض والارتفاع")

# عرض النتائج
if st.session_state.project_storage:
    st.divider()
    col_res, col_table = st.columns([2, 1])
    
    with col_res:
        st.subheader("📐 تفاصيل التخصيم")
        full_report = ""
        for u in st.session_state.project_storage:
            txt = f"📦 **{u['title']}** | {u['type']} | {u['w']}x{u['h']}x{u['d']}\n\n"
            txt += f"- **الألومنيوم (2*8):** الارتفاع {u['h_baky']} | العرض {u['w_baky']} | العمق {u['d_baky']}\n"
            txt += f"- **الفيبر:** ضهرية ({u['w_baky']}x{u['h_baky']}) | أرضية ({u['w_baky']}x{u['d_baky']})\n"
            if u['sh_n'] > 0:
                txt += f"- **الرفوف:** عدد {u['sh_n']} | فيبر الرف ({u['sh_w']-5}x{u['sh_d']-5})\n"
            txt += "---"
            st.markdown(txt)
            full_report += txt + "\n"

    with col_table:
        st.subheader("📊 قائمة الوحدات")
        df = pd.DataFrame(st.session_state.project_storage)[['title', 'w', 'h', 'd']]
        st.table(df)
        if st.button("🗑️ مسح كل البيانات"):
            st.session_state.project_storage = []
            st.rerun()

    # جرد الخامات (الفاتورة)
    st.divider()
    st.subheader("📊 إجمالي جرد خامات المشروع")
    m_sum, t_sum, f_area = 0, 0, 0
    for u in st.session_state.project_storage:
        # حسابات الجرد (الأمتار الطولية)
        m_sum += (u['h_baky']*2)+(u['w_baky']*3)+(u['d_baky']*2)
        f_area += (u['w_baky']*u['h_baky']) + (u['w_baky']*u['d_baky'])
    
    c1, c2, c3 = st.columns(3)
    c1.metric("ألومنيوم مفرد (عود)", f"{m_sum/600:.2f}")
    c2.metric("ألومنيوم متقارب (عود)", f"{t_sum/600:.2f}")
    c3.metric("فيبر (لوح)", f"{f_area/36400:.2f}")
