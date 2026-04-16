import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="DED EL KASR | التخصيم الكامل", layout="wide")

st.markdown("""
    <style>
    .header-box { background-color: #1e272e; padding: 20px; border-radius: 15px; border-bottom: 5px solid #f1c40f; text-align: center; margin-bottom: 20px; }
    .unit-card { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #dfe4ea; margin-bottom: 25px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); }
    .table-title { color: #2c3e50; font-weight: bold; border-right: 5px solid #f1c40f; padding-right: 10px; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []

# --- صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="header-box">
            <h1 style="color: #f1c40f; font-size: 3.5em; margin:0;">DED EL KASR</h1>
            <h2 style="color: white; margin:0;">نظام التخصيم والجرد الشامل</h2>
            <p style="color: #bdc3c7;">إشراف م/ ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 ابدأ التخصيم الآن"):
            st.session_state.page = 'app'
            st.rerun()

# --- صفحة التطبيق ---
elif st.session_state.page == 'app':
    # لوحة الجرد الجانبية
    st.sidebar.title("📊 جرد المشروع")
    
    with st.expander("➕ إضافة وحدة جديدة بجميع بنودها", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            u_name = st.text_input("اسم الوحدة", placeholder="مثلاً: مطبخ علوي")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "أخرى"])
            w = st.number_input("العرض الكلي", value=None)
            h = st.number_input("الارتفاع الكلي", value=None)
            d = st.number_input("العمق الكلي", value=None)
        with c2:
            st.write("**🧱 الرفوف**")
            sh_w, sh_d, sh_n = st.number_input("عرض الرف", value=None), st.number_input("عمق الرف", value=None), st.number_input("عدد الرفوف", value=None, step=1)
            st.write("**📐 الفواصل**")
            dv_h, dv_d, dv_n = st.number_input("ارتفاع الفاصل", value=None), st.number_input("عمق الفاصل", value=None), st.number_input("عدد الفواصل", value=None, step=1)
        with c3:
            st.write("**🗄️ الأدراج**")
            dr_w, dr_d, dr_n = st.number_input("عرض الدرج", value=None), st.number_input("عمق الدرج", value=None), st.number_input("عدد الأدراج", value=None, step=1)
            if st.button("✅ تحسيب وإضافة"):
                if w and h:
                    # معادلات التخصيم (بدون تغيير)
                    h_b = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                    w_b, d_b = w - 5, d - 5
                    
                    # 1. جدول الألومنيوم التفصيلي
                    alum_list = [
                        {"البند": "قوايم الارتفاع", "المقاس": h_b, "النوع": "2 مفرد / 2 متقارب"},
                        {"البند": "عوارض العرض", "المقاس": w_b, "النوع": "3 مفرد / 1 متقارب" if u_type=="سفلية" else "2 مفرد / 2 متقارب"},
                        {"البند": "عوارض العمق", "المقاس": d_b, "النوع": "2 مفرد / 2 متقارب" if u_type=="سفلية" else "4 متقارب"}
                    ]
                    if sh_n: alum_list.append({"البند": "عوارض الرف", "المقاس": f"{sh_w} و {sh_d}", "النوع": f"{int(sh_n*2)} مفرد لكل اتجاه"})
                    if dv_n: alum_list.append({"البند": "عوارض الفاصل", "المقاس": f"{dv_h} و {dv_d}", "النوع": f"{int(dv_n*2)} مفرد لكل اتجاه"})
                    if dr_n: alum_list.append({"البند": "إطار الدرج", "المقاس": f"{dr_w-2.5} و {dr_d}", "النوع": f"{int(dr_n*2)} مفرد لكل اتجاه"})

                    # 2. جدول الفيبر التفصيلي
                    fiber_list = [
                        {"القطعة": "ضهرية", "المقاس": f"{w_b}x{h_b}", "العدد": "1"},
                        {"القطعة": "أجناب", "المقاس": f"{h_b}x{d_b}", "العدد": "2"},
                        {"القطعة": "أرضية/سقف", "المقاس": f"{w_b}x{d_b}", "العدد": "1" if u_type=="سفلية" else "2"}
                    ]
                    if sh_n: fiber_list.append({"القطعة": "فيبر رف", "المقاس": f"{sh_w-5}x{sh_d-5}", "العدد": int(sh_n)})
                    if dv_n: fiber_list.append({"القطعة": "فيبر فاصل", "المقاس": f"{dv_h-5}x{dv_d-5}", "العدد": int(dv_n)})

                    # الجرد التراكمي
                    m_m = (h_b*2) + (w_b*3 if u_type=="سفلية" else w_b*2) + (d_b*2 if u_type=="سفلية" else 0)
                    m_t = (h_b*2) + (w_b*1 if u_type=="سفلية" else w_b*2) + (d_b*2 if u_type=="سفلية" else d_b*4)
                    if sh_n: m_m += (sh_w*2 + sh_d*2) * sh_n
                    if dv_n: m_m += (dv_h*2 + dv_d*2) * dv_n
                    if dr_n: m_m += ((dr_w-2.5)*2 + dr_d*2) * dr_n
                    
                    f_area = (w_b*h_b) + (h_b*d_b*2) + (w_b*d_b*(1 if u_type=="سفلية" else 2))
                    if sh_n: f_area += (sh_w-5)*(sh_d-5)*sh_n
                    if dv_n: f_area += (dv_h-5)*(dv_d-5)*dv_n

                    st.session_state.project_list.append({
                        "name": u_name, "type": u_type, "dims": f"{w}x{h}x{d}",
                        "alum_df": pd.DataFrame(alum_list), "fiber_df": pd.DataFrame(fiber_list),
                        "m_m": m_m, "m_t": m_t, "f_a": f_area
                    })
                    st.rerun()

    # تحديث السايد بار بالجرد
    if st.session_state.project_list:
        total_m = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        total_t = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        total_f = sum([x['f_a'] for x in st.session_state.project_list]) / (280*130)
        
        st.sidebar.metric("أعواد مفرد", f"{round(total_m, 1)} عود")
        st.sidebar.metric("أعواد متقارب", f"{round(total_t, 1)} عود")
        st.sidebar.metric("ألواح فيبر", f"{round(total_f, 1)} لوح")
        if st.sidebar.button("🗑️ مسح الكل"):
            st.session_state.project_list = []
            st.rerun()

    # عرض النتائج الكاملة
    for idx, item in enumerate(st.session_state.project_list):
        with st.container():
            st.markdown(f'<div class="unit-card"><h3>{idx+1}. {item["name"]} - {item["dims"]}</h3>', unsafe_allow_html=True)
            col_a, col_f = st.columns(2)
            with col_a:
                st.markdown('<p class="table-title">⚔️ ألومنيوم (مفرد/متقارب)</p>', unsafe_allow_html=True)
                st.table(item['alum_df'])
            with col_f:
                st.markdown('<p class="table-title">🪵 فيبر (بخصم 5 سم)</p>', unsafe_allow_html=True)
                st.table(item['fiber_df'])
            st.markdown('</div>', unsafe_allow_html=True)
