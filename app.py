import streamlit as st
import pandas as pd

# إعدادات واجهة التطبيق
st.set_page_config(page_title="DED EL KASR - Aluminum System", layout="wide")

# تصميم الهيدر (العنوان)
st.markdown("""
    <div style="background-color: #1e272e; padding: 25px; border-radius: 15px; border-bottom: 5px solid #f1c40f; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">
        <h1 style="color: #f1c40f; margin: 0; font-family: 'Segoe UI';">DED EL KASR | ضد الكسر</h1>
        <p style="color: #d2dae2; font-size: 1.3em; margin-top: 10px;">نظام التخصيم الفني والإداري - م/ ياسين علاء</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# تخزين البيانات في الجلسة (عشان متتمسحش لما الصفحة تعمل ريفريش)
if 'project_list' not in st.session_state:
    st.session_state.project_list = []

# منطقة المدخلات الفنية
st.markdown("### 📝 إدخال بيانات الوحدة")
with st.container():
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        u_name = st.text_input("اسم الوحدة (مثلاً: مطبخ علوي يمين)", "وحدة جديدة")
        u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
    with col2:
        w = st.number_input("العرض الكلي (سم)", min_value=0.0, step=0.1, format="%.1f")
        h = st.number_input("الارتفاع الكلي (سم)", min_value=0.0, step=0.1, format="%.1f")
    with col3:
        d = st.number_input("العمق الكلي (سم)", min_value=0.0, step=0.1, format="%.1f")
        sh_n = st.number_input("عدد الرفوف", min_value=0, step=1)

# زر الإضافة
if st.button("✅ إضافة للجدول وتحسيب المقاسات", use_container_width=True):
    if w > 0 and h > 0:
        # معادلات التخصيم المعتمدة في ورشتك (م/ ياسين علاء)
        # السفلية والدولاب خصم 13 سم للارتفاع، الباقي 5 سم
        h_baky = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
        w_baky = w - 5
        d_baky = d - 5
        
        # حسبة الفيبر (مساحة تقريبية بالمتر المربع)
        # ضهرية + أرضية + 2 جنب
        f_area = ((w_baky * h_baky) + (w_baky * d_baky) + (h_baky * d_baky * 2)) / 10000
        
        new_unit = {
            "اسم الوحدة": u_name,
            "النوع": u_type,
            "ارتفاع الباكي": round(h_baky, 1),
            "عرض الباكي": round(w_baky, 1),
            "عمق الباكي": round(d_baky, 1),
            "مساحة الفيبر (م²)": round(f_area, 2)
        }
        st.session_state.project_list.append(new_unit)
        st.balloons()
    else:
        st.error("برجاء إدخال المقاسات بشكل صحيح!")

# عرض النتائج والجرد
if st.session_state.project_list:
    st.markdown("---")
    st.subheader("📋 جدول الوحدات المضافة")
    df = pd.DataFrame(st.session_state.project_list)
    st.dataframe(df, use_container_width=True)

    # حسابات الجرد الكلي في الجنب
    st.sidebar.markdown(f"""
        <div style="background-color: #2f3640; padding: 15px; border-radius: 10px; border-right: 5px solid #f1c40f;">
            <h2 style="color: #f1c40f; text-align: center;">📊 إجمالي المشروع</h2>
        </div>
    """, unsafe_allow_html=True)
    
    total_fiber = df["مساحة الفيبر (م²)"].sum()
    total_units = len(df)
    
    st.sidebar.metric("إجمالي الوحدات", f"{total_units} وحدة")
    st.sidebar.metric("إجمالي الفيبر المطلوب", f"{total_fiber:.2f} م²")
    st.sidebar.write(f"عدد ألواح الفيبر التقريبي: {max(1, round(total_fiber / 3.6, 1))} لوح")

    if st.sidebar.button("🗑️ مسح كل البيانات", use_container_width=True):
        st.session_state.project_list = []
        st.rerun()

st.markdown("---")
st.caption("برمجة وتطوير نظام DED EL KASR الذكي | 2026")
