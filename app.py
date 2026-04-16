import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والستايل الاحترافي
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

st.markdown("""
    <style>
    /* تحسين شكل الهيدر */
    .header-box { 
        background-color: #1e272e; 
        padding: 30px; 
        border-radius: 20px; 
        border-bottom: 8px solid #f1c40f; 
        text-align: center; 
        margin-bottom: 30px; 
        box-shadow: 0px 10px 20px rgba(0,0,0,0.2);
    }
    /* تحسين كروت الوحدات */
    .unit-card { 
        background-color: #f8f9fa; 
        padding: 25px; 
        border-radius: 15px; 
        border-right: 10px solid #2c3e50; 
        margin-bottom: 30px; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        border-top: 1px solid #dee2e6;
    }
    /* عناوين الجداول */
    .table-header-alum { color: #2980b9; font-size: 1.4em; font-weight: bold; margin-bottom: 10px; border-bottom: 2px solid #2980b9; display: inline-block; }
    .table-header-fiber { color: #27ae60; font-size: 1.4em; font-weight: bold; margin-bottom: 10px; border-bottom: 2px solid #27ae60; display: inline-block; }
    /* تذييل الصفحة */
    .footer-text { 
        text-align: center; 
        color: #2c3e50; 
        padding: 20px; 
        font-size: 1.2em;
        font-weight: bold; 
        background: #f1c40f;
        border-radius: 10px;
        margin-top: 50px; 
    }
    /* توضيح الكلام داخل الجداول */
    .stTable td { font-size: 1.2em !important; font-weight: 500 !important; }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []

# --- صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="header-box">
            <h1 style="color: #f1c40f; font-size: 5em; margin:0; font-family: 'Arial Black';">DOGGA SYSTEM</h1>
            <h2 style="color: white; margin:0; letter-spacing: 2px;">نظام التخصيم الفني المتكامل</h2>
            <p style="color: #bdc3c7; font-size: 1.8em; margin-top: 15px; font-weight: bold;">برمجة المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 دخول للنظام الاحترافي"):
            st.session_state.page = 'app'
            st.rerun()

# --- صفحة التطبيق ---
elif st.session_state.page == 'app':
    st.sidebar.markdown(f"<h2 style='text-align:center; color:#f1c40f;'>DOGGA SYSTEM</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='text-align:center;'><b>برمجة المهندس ياسين علاء</b></p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.title("📊 جرد الخامات")
    
    with st.expander("📝 إضافة وحدة جديدة - أدخل المقاسات بدقة", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            u_name = st.text_input("اسم الوحدة", placeholder="مثلاً: وحدة حوض")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "أخرى"])
            w = st.number_input("العرض الكلي (سم)", value=None)
            h = st.number_input("الارتفاع الكلي (سم)", value=None)
            d = st.number_input("العمق الكلي (سم)", value=None)
        with c2:
            st.write("**🧱 الرفوف**")
            sh_w = st.number_input("عرض الرف", value=None)
            sh_d = st.number_input("عمق الرف", value=None)
            sh_n = st.number_input("عدد الرفوف", value=None, step=1)
            st.write("**📐 الفواصل**")
            dv_h = st.number_input("ارتفاع الفاصل", value=None)
            dv_d = st.number_input("عمق الفاصل", value=None)
            dv_n = st.number_input("عدد الفواصل", value=None, step=1)
        with c3:
            st.write("**🗄️ الأدراج**")
            dr_w = st.number_input("عرض الدرج", value=None)
            dr_d = st.number_input("عمق الدرج", value=None)
            dr_n = st.number_input("عدد الأدراج", value=None, step=1)
            u_notes = st.text_area("ملاحظات إضافية", placeholder="مقابض، ليد، إكسسوارات...")
            
            if st.button("✅ تحسيب وحفظ في القائمة"):
                if w and h:
                    h_b = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                    w_b, d_b = w - 5, d - 5
                    
                    # 1. قائمة الألومنيوم التفصيلية
                    alum_list = [
                        {"البيان": "قوايم الارتفاع", "المقاس الصافي": f"{h_b} سم", "العدد": "4", "النوع": "2 مفرد / 2 متقارب"},
                        {"البيان": "عوارض العرض", "المقاس الصافي": f"{w_b} سم", "العدد": "4", "النوع": "3 مفرد / 1 متقارب" if u_type=="سفلية" else "2 مفرد / 2 متقارب"},
                        {"البيان": "عوارض العمق", "المقاس الصافي": f"{d_b} سم", "العدد": "4", "النوع": "2 مفرد / 2 متقارب" if u_type=="سفلية" else "4 متقارب"}
                    ]
                    if sh_n:
                        alum_list.append({"البيان": "عوارض الرف (عرض)", "المقاس الصافي": f"{sh_w} سم", "العدد": f"{int(sh_n*2)}", "النوع": "مفرد"})
                        alum_list.append({"البيان": "عوارض الرف (عمق)", "المقاس الصافي": f"{sh_d} سم", "العدد": f"{int(sh_n*2)}", "النوع": "مفرد"})
                    if dv_n:
                        alum_list.append({"البيان": "عوارض الفاصل (ارتفاع)", "المقاس الصافي": f"{dv_h} سم", "العدد": f"{int(dv_n*2)}", "النوع": "مفرد"})
                        alum_list.append({"البيان": "عوارض الفاصل (عمق)", "المقاس الصافي": f"{dv_d} سم", "العدد": f"{int(dv_n*2)}", "النوع": "مفرد"})
                    if dr_n:
                        alum_list.append({"البيان": "إطار الدرج (عرض-2.5)", "المقاس الصافي": f"{dr_w-2.5} سم", "العدد": f"{int(dr_n*2)}", "النوع": "مفرد"})
                        alum_list.append({"البيان": "إطار الدرج (عمق)", "المقاس الصافي": f"{dr_d} سم", "العدد": f"{int(dr_n*2)}", "النوع": "مفرد"})

                    # 2. قائمة الفيبر التفصيلية
                    fiber_list = [
                        {"القطعة": "فيبر ضهرية", "المقاس (عرض × طول)": f"{w_b} x {h_b}", "العدد": "1"},
                        {"القطعة": "فيبر أجناب", "المقاس (عرض × طول)": f"{h_b} x {d_b}", "العدد": "2"},
                        {"القطعة": "فيبر أرضية/سقف", "المقاس (عرض × طول)": f"{w_b} x {d_b}", "العدد": "1" if u_type=="سفلية" else "2"}
                    ]
                    if sh_n: fiber_list.append({"القطعة": "فيبر رف", "المقاس (عرض × طول)": f"{sh_w-5} x {sh_d-5}", "العدد": int(sh_n)})
                    if dv_n: fiber_list.append({"القطعة": "فيبر فاصل", "المقاس (عرض × طول)": f"{dv_h-5} x {dv_d-5}", "العدد": int(dv_n)})

                    # حسابات الجرد
                    m_m = (h_b*2) + (w_b*(3 if u_type=="سفلية" else 2)) + (d_b*2 if u_type=="سفلية" else 0)
                    m_t = (h_b*2) + (w_b*(1 if u_type=="سفلية" else 2)) + (d_b*(2 if u_type=="سفلية" else 4))
                    if sh_n: m_m += (sh_w*2 + sh_d*2) * sh_n
                    if dv_n: m_m += (dv_h*2 + dv_d*2) * dv_n
                    if dr_n: m_m += ((dr_w-2.5)*2 + dr_d*2) * dr_n
                    f_area = (w_b*h_b) + (h_b*d_b*2) + (w_b*d_b*(1 if u_type=="سفلية" else 2))
                    if sh_n: f_area += (sh_w-5)*(sh_d-5)*sh_n
                    if dv_n: f_area += (dv_h-5)*(dv_d-5)*dv_n

                    st.session_state.project_list.append({
                        "name": u_name, "type": u_type, "dims": f"{w}x{h}x{d}",
                        "alum_df": pd.DataFrame(alum_list), "fiber_df": pd.DataFrame(fiber_list),
                        "m_m": m_m, "m_t": m_t, "f_a": f_area, "notes": u_notes
                    })
                    st.rerun()

    # تحديث السايد بار بالجرد
    if st.session_state.project_list:
        tot_m = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        tot_t = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        tot_f = sum([x['f_a'] for x in st.session_state.project_list]) / (280*130)
        
        st.sidebar.metric("🪵 أعواد مفرد", f"{round(tot_m, 1)} عود")
        st.sidebar.metric("🪵 أعواد متقارب", f"{round(tot_t, 1)} عود")
        st.sidebar.metric("💎 ألواح فيبر", f"{round(tot_f, 1)} لوح")
        if st.sidebar.button("🗑️ مسح المشروع بالكامل"):
            st.session_state.project_list = []
            st.rerun()

    # عرض النتائج بشكل مرتب جداً
    for idx, item in enumerate(st.session_state.project_list):
        st.markdown(f"""
            <div class="unit-card">
                <h2 style="color:#2c3e50; border-bottom: 2px dashed #bdc3c7; padding-bottom:10px;">
                #{idx+1} | {item['name']} <span style="font-size:0.6em; color:#7f8c8d;">({item['type']} - {item['dims']} سم)</span>
                </h2>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="table-header-alum">⚔️ تقطيع الألومنيوم (DOGGA)</p>', unsafe_allow_html=True)
            st.table(item['alum_df'])
        with col2:
            st.markdown('<p class="table-header-fiber">🪵 تقطيع الفيبر الصافي</p>', unsafe_allow_html=True)
            st.table(item['fiber_df'])
            if item['notes']:
                st.warning(f"📌 **ملاحظات:** {item['notes']}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="footer-text">برمجة المهندس ياسين علاء - DOGGA SYSTEM 2026</div>', unsafe_allow_html=True)
