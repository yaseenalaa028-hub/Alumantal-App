import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="DED EL KASR | ضد الكسر", layout="wide")

# تخصيص الألوان والخطوط (CSS)
st.markdown("""
    <style>
    .main { background-color: #f5f6fa; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #f1c40f;
        color: #2c3e50;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #d4ac0d; color: white; }
    .header-box {
        background-color: #1e272e;
        padding: 30px;
        border-radius: 15px;
        border-bottom: 5px solid #f1c40f;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة حالة الصفحة (البداية vs التخصيم)
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'project_list' not in st.session_state:
    st.session_state.project_list = []

# --- الصفحة الأولى: الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="header-box">
            <h1 style="color: #f1c40f; font-size: 3em;">DED EL KASR</h1>
            <h2 style="color: white;">ضد الكسر للألومنيوم والمطابخ</h2>
            <p style="color: #bdc3c7; font-size: 1.2em;">نظام المهندس ياسين علاء للتخصيم الفني الذكي</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write(" ")
        if st.button("🚀 ابدأ عملية التخصيم الآن"):
            st.session_state.page = 'app'
            st.rerun()

# --- الصفحة الثانية: تطبيق التخصيم ---
elif st.session_state.page == 'app':
    # هيدر صغير للعودة
    cols = st.columns([8, 2])
    cols[0].title("📐 لوحة التحكم في التخصيم")
    if cols[1].button("🏠 الرئيسية"):
        st.session_state.page = 'welcome'
        st.rerun()

    # منطقة المدخلات في حاوية أنيقة
    with st.expander("➕ إضافة وحدة جديدة", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            u_name = st.text_input("اسم الوحدة", placeholder="مثلاً: وحدة حوض")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "أخرى"])
        with c2:
            w = st.number_input("العرض (سم)", min_value=0.0, format="%.1f")
            h = st.number_input("الارتفاع (سم)", min_value=0.0, format="%.1f")
        with c3:
            d = st.number_input("العمق (سم)", min_value=0.0, format="%.1f")
            sh_n = st.number_input("الرفوف", min_value=0, step=1)
        
        if st.button("إضافة الوحدة للحسابات"):
            if w > 0 and h > 0:
                # المعادلات الخاصة بك يا هندسة
                h_calc = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                w_calc, d_calc = w - 5, d - 5
                
                new_item = {
                    "الوحدة": u_name,
                    "النوع": u_type,
                    "الارتفاع الصافي": h_calc,
                    "العرض الصافي": w_calc,
                    "العمق الصافي": d_calc,
                    "مساحة الفيبر (م²)": round((w_calc * h_calc) / 10000, 2)
                }
                st.session_state.project_list.append(new_item)
                st.success("تمت الإضافة بنجاح!")
            else:
                st.warning("برجاء إدخال المقاسات")

    # عرض النتائج
    if st.session_state.project_list:
        st.markdown("### 📋 كشف تقطيع الوحدات")
        df = pd.DataFrame(st.session_state.project_list)
        st.table(df)
        
        # خلاصة الجرد في أسفل الصفحة
        st.markdown("---")
        total_f = df["مساحة الفيبر (م²)"].sum()
        c1, c2 = st.columns(2)
        c1.metric("إجمالي الفيبر المطلوب", f"{total_f:.2f} م²")
        c2.metric("عدد الوحدات", len(df))
        
        if st.button("🗑️ مسح المشروع الحالي"):
            st.session_state.project_list = []
            st.rerun()
