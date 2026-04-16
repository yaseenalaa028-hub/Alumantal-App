import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والستايل الاحترافي
st.set_page_config(page_title="DED EL KASR | ضد الكسر", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f1f2f6; }
    .header-box {
        background-color: #1e272e;
        padding: 30px;
        border-radius: 15px;
        border-bottom: 5px solid #f1c40f;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .unit-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-right: 8px solid #f1c40f;
        margin-bottom: 15px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    }
    .section-title { color: #2980b9; font-weight: bold; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 10px; }
    .stButton>button { background-color: #f1c40f; color: #2c3e50; font-weight: bold; border-radius: 8px; height: 3em; }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []

# --- صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="header-box">
            <h1 style="color: #f1c40f; font-size: 3.5em; margin:0;">DED EL KASR</h1>
            <h2 style="color: white; margin:0;">ضد الكسر للألومنيوم والمطابخ</h2>
            <p style="color: #bdc3c7; font-size: 1.2em;">نظام المهندس ياسين علاء للتخصيم الفني</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 ابدأ عملية التخصيم"):
            st.session_state.page = 'app'
            st.rerun()

# --- صفحة التطبيق الأساسية ---
elif st.session_state.page == 'app':
    c_head = st.columns([8, 2])
    c_head[0].title("📐 لوحة التخصيم التفصيلية")
    if c_head[1].button("🏠 الرئيسية"):
        st.session_state.page = 'welcome'
        st.rerun()

    # منطقة المدخلات المرتبة
    with st.expander("➕ إضافة وحدة جديدة للمشروع", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            u_name = st.text_input("اسم الوحدة", placeholder="مثلاً: وحدة درج")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
            w_total = st.number_input("العرض الكلي (سم)", min_value=0.0)
            h_total = st.number_input("الارتفاع الكلي (سم)", min_value=0.0)
            d_total = st.number_input("العمق الكلي (سم)", min_value=0.0)
        
        with col2:
            st.markdown("**🧱 الرفوف والفواصل**")
            sh_w = st.number_input("عرض الرف", min_value=0.0)
            sh_d = st.number_input("عمق الرف", min_value=0.0)
            sh_n = st.number_input("عدد الرفوف", min_value=0, step=1)
            dv_h = st.number_input("ارتفاع الفاصل", min_value=0.0)
            dv_d = st.number_input("عمق الفاصل", min_value=0.0)
            dv_n = st.number_input("عدد الفواصل", min_value=0, step=1)

        with col3:
            st.markdown("**🗄️ الأدراج**")
            dr_w = st.number_input("عرض الدرج", min_value=0.0)
            dr_d = st.number_input("عمق الدرج", min_value=0.0)
            dr_n = st.number_input("عدد الأدراج", min_value=0, step=1)
            st.write("---")
            add_btn = st.button("✅ تحسيب وإضافة للتقرير")

    if add_btn:
        if w_total > 0 and h_total > 0:
            # تطبيق بنود التخصيم المظبوطة
            h_baky = h_total - 13 if u_type in ["سفلية", "دولاب خزين"] else h_total - 5
            w_baky = w_total - 5
            d_baky = d_total - 5

            # بناء تقرير الوحدة المرتب
            report = {
                "name": u_name,
                "type": u_type,
                "dims": f"{w_total}x{h_total}x{d_total}",
                "main": f"الارتفاع: {h_baky} | العرض: {w_baky} | العمق: {d_baky}",
                "fiber": f"ضهرية: {w_baky}x{h_baky} | أرضية: {w_baky}x{d_baky} | أجناب: {h_baky}x{d_baky}",
                "shelves": f"عوارض: {sh_w} سم و {sh_d} سم | فيبر: {sh_w-5}x{sh_d-5}" if sh_n > 0 else "لا يوجد",
                "dividers": f"عوارض: {dv_h} سم و {dv_d} سم | فيبر: {dv_h-5}x{dv_d-5}" if dv_n > 0 else "لا يوجد",
                "drawers": f"عوارض عرض: {dr_w-2.5} سم | عوارض عمق: {dr_d} سم" if dr_n > 0 else "لا يوجد",
                "sh_n": sh_n, "dv_n": dv_n, "dr_n": dr_n
            }
            st.session_state.project_list.append(report)
            st.success(f"تمت إضافة {u_name} بنجاح")
        else:
            st.error("خطأ: يرجى إدخال المقاسات الأساسية!")

    # عرض التقرير النهائي المرتب
    if st.session_state.project_list:
        st.markdown("### 📄 كشف تقطيع مشروع: ضد الكسر")
        for idx, item in enumerate(st.session_state.project_list):
            with st.container():
                st.markdown(f"""
                <div class="unit-card">
                    <h3 style="color:#2c3e50; margin:0;">{idx+1}. {item['name']} ({item['type']})</h3>
                    <p style="color:#7f8c8d;">المقاس الكلي: {item['dims']}</p>
                    <div class="section-title">📐 [1] تخصيم الهيكل الأساسي (2*8)</div>
                    <p>{item['main']}</p>
                    <div class="section-title">🪵 [2] تخصيم الفيبر</div>
                    <p>{item['fiber']}</p>
                    <div class="section-title">🧱 [3] الرفوف (عدد {item['sh_n']})</div>
                    <p>{item['shelves']}</p>
                    <div class="section-title">📏 [4] الفواصل (عدد {item['dv_n']})</div>
                    <p>{item['dividers']}</p>
                    <div class="section-title">🗄️ [5] الأدراج (عدد {item['dr_n']})</div>
                    <p>{item['drawers']}</p>
                </div>
                """, unsafe_allow_html=True)

        if st.button("🗑️ مسح المشروع الحالي"):
            st.session_state.project_list = []
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("برمجة وتطوير: DED EL KASR System v2.0")
