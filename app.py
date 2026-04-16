import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="DED EL KASR | التخصيم الاحترافي", layout="wide")

st.markdown("""
    <style>
    .header-box {
        background-color: #1e272e;
        padding: 20px;
        border-radius: 15px;
        border-bottom: 5px solid #f1c40f;
        text-align: center;
        margin-bottom: 20px;
    }
    .unit-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dfe4ea;
        margin-bottom: 25px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .table-title-alum { color: #2980b9; font-weight: bold; margin-top: 15px; border-right: 5px solid #2980b9; padding-right: 10px; }
    .table-title-fiber { color: #27ae60; font-weight: bold; margin-top: 15px; border-right: 5px solid #27ae60; padding-right: 10px; }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []

# --- صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="header-box">
            <h1 style="color: #f1c40f; font-size: 3em; margin:0;">DED EL KASR</h1>
            <h2 style="color: white; margin:0;">نظام الجداول المنفصلة</h2>
            <p style="color: #bdc3c7;">إدارة المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 ابدأ التخصيم الاحترافي"):
            st.session_state.page = 'app'
            st.rerun()

# --- صفحة التطبيق ---
elif st.session_state.page == 'app':
    c_head = st.columns([8, 2])
    c_head[0].title("📐 تخصيم الوحدات (جداول منفصلة)")
    if c_head[1].button("🏠 الرئيسية"):
        st.session_state.page = 'welcome'
        st.rerun()

    with st.expander("➕ إضافة وحدة جديدة", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            u_name = st.text_input("اسم الوحدة", placeholder="مثلاً: وحدة أدراج")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "أخرى"])
            w = st.number_input("العرض الكلي", min_value=0.0)
            h = st.number_input("الارتفاع الكلي", min_value=0.0)
            d = st.number_input("العمق الكلي", min_value=0.0)
        with col2:
            st.write("**🧱 الرفوف والفواصل**")
            sh_w, sh_d, sh_n = st.number_input("عرض الرف", 0.0), st.number_input("عمق الرف", 0.0), st.number_input("عدد الرفوف", 0, step=1)
            dv_h, dv_d, dv_n = st.number_input("ارتفاع الفاصل", 0.0), st.number_input("عمق الفاصل", 0.0), st.number_input("عدد الفواصل", 0, step=1)
        with col3:
            st.write("**🗄️ الأدراج**")
            dr_w, dr_d, dr_n = st.number_input("عرض الدرج", 0.0), st.number_input("عمق الدرج", 0.0), st.number_input("عدد الأدراج", 0, step=1)
            st.write("---")
            if st.button("✅ تحسيب"):
                if w > 0 and h > 0:
                    # 1. تخصيمات الهيكل
                    h_b = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                    w_b, d_b = w - 5, d - 5

                    # 2. جدول الألومنيوم
                    alum_data = [
                        {"البيان": "قوايم الارتفاع", "المقاس": h_b, "العدد": "4 قطع"},
                        {"البيان": "عوارض العرض", "المقاس": w_b, "العدد": "4 قطع"},
                        {"البيان": "عوارض العمق", "المقاس": d_b, "العدد": "4 قطع"}
                    ]
                    if sh_n > 0:
                        alum_data.append({"البيان": "عوارض رف (عرض)", "المقاس": sh_w, "العدد": f"{sh_n*2} ق"})
                        alum_data.append({"البيان": "عوارض رف (عمق)", "المقاس": sh_d, "العدد": f"{sh_n*2} ق"})
                    if dr_n > 0:
                        alum_data.append({"البيان": "درج (عرض - 2.5)", "المقاس": dr_w-2.5, "العدد": f"{dr_n*2} ق"})
                        alum_data.append({"البيان": "درج (عمق)", "المقاس": dr_d, "العدد": f"{dr_n*2} ق"})

                    # 3. جدول الفيبر
                    fiber_data = [
                        {"البيان": "ضهرية", "المقاس": f"{w_b} × {h_b}", "العدد": "1 ق"},
                        {"البيان": "أرضية/سقف", "المقاس": f"{w_b} × {d_b}", "العدد": "2 ق" if u_type!="سفلية" else "1 ق"},
                        {"البيان": "أجناب", "المقاس": f"{h_b} × {d_b}", "العدد": "2 ق"}
                    ]
                    if sh_n > 0: fiber_data.append({"البيان": "فيبر رف", "المقاس": f"{sh_w-5} × {sh_d-5}", "العدد": f"{sh_n} ق"})
                    
                    st.session_state.project_list.append({
                        "name": u_name, "type": u_type, "dims": f"{w}x{h}x{d}",
                        "alum": pd.DataFrame(alum_data), "fiber": pd.DataFrame(fiber_data)
                    })
                    st.rerun()

    # عرض النتائج
    if st.session_state.project_list:
        for idx, item in enumerate(st.session_state.project_list):
            st.markdown(f"""<div class="unit-card">
                <h3>{idx+1}. {item['name']} ({item['type']}) - {item['dims']}</h3>""", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<p class="table-title-alum">⚔️ جدول تقطيع الألومنيوم (2*8)</p>', unsafe_allow_html=True)
                st.table(item['alum'])
            with c2:
                st.markdown('<p class="table-title-fiber">🪵 جدول تقطيع الفيبر</p>', unsafe_allow_html=True)
                st.table(item['fiber'])
            st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🗑️ مسح المشروع"):
            st.session_state.project_list = []
            st.rerun()
        
