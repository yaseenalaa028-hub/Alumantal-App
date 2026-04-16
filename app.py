import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="DED EL KASR - Pro", layout="wide")

# تخصيص التصميم (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #f1c40f; color: #2c3e50; font-weight: bold; }
    .header-box { background-color: #1e272e; padding: 25px; border-radius: 15px; border-bottom: 5px solid #f1c40f; text-align: center; margin-bottom: 20px; }
    .res-box { background-color: #ffffff; padding: 15px; border-radius: 10px; border-right: 5px solid #27ae60; margin-bottom: 10px; box-shadow: 0px 2px 5px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []

# --- صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="header-box">
            <h1 style="color: #f1c40f; font-size: 3.5em; margin:0;">DED EL KASR</h1>
            <h2 style="color: white; margin:0;">ضد الكسر للألومنيوم</h2>
            <p style="color: #bdc3c7; font-size: 1.2em;">الإصدار الاحترافي - نظام المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("🚀 ابدأ التخصيم الفني"):
            st.session_state.page = 'app'
            st.rerun()

# --- صفحة التطبيق ---
elif st.session_state.page == 'app':
    cols = st.columns([8, 2])
    cols[0].title("📐 لوحة تخصيم الوحدات التفصيلية")
    if cols[1].button("🏠 الرئيسية"):
        st.session_state.page = 'welcome'
        st.rerun()

    # منطقة المدخلات
    with st.expander("📝 إضافة وحدة جديدة (أدخل المقاسات بالكلي)", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            u_name = st.text_input("اسم الوحدة", placeholder="مثلاً: مطبخ علوي")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "أخرى"])
            w = st.number_input("العرض الكلي (سم)", min_value=0.0)
            h = st.number_input("الارتفاع الكلي (سم)", min_value=0.0)
            d = st.number_input("العمق الكلي (سم)", min_value=0.0)
        
        with c2:
            st.write("**🧱 الرفوف**")
            sh_w = st.number_input("عرض الرف", min_value=0.0)
            sh_d = st.number_input("عمق الرف", min_value=0.0)
            sh_n = st.number_input("عدد الرفوف", min_value=0, step=1)
            st.write("**📐 الفواصل**")
            dv_h = st.number_input("ارتفاع الفاصل", min_value=0.0)
            dv_d = st.number_input("عمق الفاصل", min_value=0.0)
            dv_n = st.number_input("عدد الفواصل", min_value=0, step=1)

        with c3:
            st.write("**🗄️ الأدراج**")
            dr_w = st.number_input("عرض الدرج", min_value=0.0)
            dr_d = st.number_input("عمق الدرج", min_value=0.0)
            dr_n = st.number_input("عدد الأدراج", min_value=0, step=1)
            st.write("---")
            submit = st.button("✅ إضافة الوحدة وتحسيب التفاصيل")

    if submit:
        if w > 0 and h > 0:
            # 1. تخصيم الباكي الرئيسي
            h_b = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
            w_b, d_b = w - 5, d - 5
            
            # 2. تفاصيل الألومنيوم والفيبر
            res_txt = f"**{u_name} ({u_type})**\n\n"
            res_txt += f"📏 **الباكي الرئيسي:** ع {w_b} | ار {h_b} | عم {d_b}\n"
            
            if sh_n > 0:
                res_txt += f"🧱 **الرفوف ({sh_n}):** عوارض عرض {sh_w} ({sh_n*2} ق) | عوارض عمق {sh_d} ({sh_n*2} ق) | فيبر {sh_w-5}x{sh_d-5}\n"
            
            if dv_n > 0:
                res_txt += f"📐 **الفواصل ({dv_n}):** عوارض ارتفاع {dv_h} ({dv_n*2} ق) | عوارض عمق {dv_d} ({dv_n*2} ق) | فيبر {dv_h-5}x{dv_d-5}\n"
            
            if dr_n > 0:
                res_txt += f"🗄️ **الأدراج ({dr_n}):** عوارض عرض {dr_w-2.5} ({dr_n*2} ق) | عوارض عمق {dr_d} ({dr_n*2} ق)\n"

            st.session_state.project_list.append({"info": res_txt, "fiber": (w_b*h_b)/10000})
            st.success("تمت الإضافة")
        else:
            st.error("برجاء إدخال المقاسات الأساسية")

    # عرض النتائج النهائية
    if st.session_state.project_list:
        st.markdown("### 📋 كشف تفاصيل التقطيع")
        for idx, item in enumerate(st.session_state.project_list):
            st.markdown(f"""<div class="res-box">{item['info']}</div>""", unsafe_allow_html=True)
            
        if st.button("🗑️ مسح المشروع"):
            st.session_state.project_list = []
            st.rerun()
