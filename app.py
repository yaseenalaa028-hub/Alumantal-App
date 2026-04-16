import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والستايل
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

st.markdown("""
    <style>
    .header-box { background-color: #1e272e; padding: 25px; border-radius: 15px; border-bottom: 5px solid #f1c40f; text-align: center; margin-bottom: 20px; }
    .unit-card { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #dfe4ea; margin-bottom: 25px; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); }
    .table-title { color: #2c3e50; font-weight: bold; border-right: 5px solid #f1c40f; padding-right: 10px; margin-top: 15px; margin-bottom: 10px; }
    .footer-text { text-align: center; color: #7f8c8d; padding: 20px; font-weight: bold; border-top: 1px solid #eee; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []

# --- صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="header-box">
            <h1 style="color: #f1c40f; font-size: 4em; margin:0;">DOGGA SYSTEM</h1>
            <h2 style="color: white; margin:0;">نظام التخصيم الفني المتكامل</h2>
            <p style="color: #bdc3c7; font-size: 1.5em; margin-top: 10px;">برمجة المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 دخول للنظام"):
            st.session_state.page = 'app'
            st.rerun()

# --- صفحة التطبيق ---
elif st.session_state.page == 'app':
    st.sidebar.title("📊 جرد خامات المشروع")
    st.sidebar.markdown("---")
    
    with st.expander("➕ إضافة وحدة جديدة (أدخل البيانات هنا)", expanded=True):
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
            u_notes = st.text_area("ملاحظات إضافية", placeholder="اكتب ملاحظاتك هنا...")
            
            if st.button("✅ تحسيب وحفظ"):
                if w and h:
                    # معادلات التخصيم الأساسية
                    h_b = h - 13 if u_type in ["سفلية", "دولاب خزين"] else h - 5
                    w_b, d_b = w - 5, d - 5
                    
                    # 1. بناء جدول الألومنيوم (فصل كامل لكل بند)
                    alum_list = [
                        {"البند": "قوايم الارتفاع", "المقاس": h_b, "العدد": "4 قطع", "النوع": "2 مفرد / 2 متقارب"},
                        {"البند": "عوارض العرض", "المقاس": w_b, "العدد": "4 قطع", "النوع": "3 مفرد / 1 متقارب" if u_type=="سفلية" else "2 مفرد / 2 متقارب"},
                        {"البند": "عوارض العمق", "المقاس": d_b, "العدد": "4 قطع", "النوع": "2 مفرد / 2 متقارب" if u_type=="سفلية" else "4 متقارب"}
                    ]
                    if sh_n:
                        alum_list.append({"البند": "عوارض الرف (عرض)", "المقاس": sh_w, "العدد": f"{int(sh_n*2)} ق", "النوع": "مفرد"})
                        alum_list.append({"البند": "عوارض الرف (عمق)", "المقاس": sh_d, "العدد": f"{int(sh_n*2)} ق", "النوع": "مفرد"})
                    if dv_n:
                        alum_list.append({"البند": "عوارض الفاصل (ارتفاع)", "المقاس": dv_h, "العدد": f"{int(dv_n*2)} ق", "النوع": "مفرد"})
                        alum_list.append({"البند": "عوارض الفاصل (عمق)", "المقاس": dv_d, "العدد": f"{int(dv_n*2)} ق", "النوع": "مفرد"})
                    if dr_n:
                        alum_list.append({"البند": "عوارض الدرج (عرض-2.5)", "المقاس": dr_w-2.5, "العدد": f"{int(dr_n*2)} ق", "النوع": "مفرد"})
                        alum_list.append({"البند": "عوارض الدرج (عمق)", "المقاس": dr_d, "العدد": f"{int(dr_n*2)} ق", "النوع": "مفرد"})

                    # 2. بناء جدول الفيبر التفصيلي
                    fiber_list = [
                        {"القطعة": "فيبر ضهرية", "المقاس": f"{w_b}x{h_b}", "العدد": "1"},
                        {"القطعة": "فيبر أجناب", "المقاس": f"{h_b}x{d_b}", "العدد": "2"},
                        {"القطعة": "فيبر أرضية/سقف", "المقاس": f"{w_b}x{d_b}", "العدد": "1" if u_type=="سفلية" else "2"}
                    ]
                    if sh_n: fiber_list.append({"القطعة": "فيبر رف", "المقاس": f"{sh_w-5}x{sh_d-5}", "العدد": int(sh_n)})
                    if dv_n: fiber_list.append({"القطعة": "فيبر فاصل", "المقاس": f"{dv_h-5}x{dv_d-5}", "العدد": int(dv_n)})

                    # الجرد (العود 600سم واللوح 280x130)
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

    # تحديث الجرد الجانبي
    if st.session_state.project_list:
        tot_m = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        tot_t = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        tot_f = sum([x['f_a'] for x in st.session_state.project_list]) / (280*130)
        
        st.sidebar.metric("أعواد مفرد", f"{round(tot_m, 1)} عود")
        st.sidebar.metric("أعواد متقارب", f"{round(tot_t, 1)} عود")
        st.sidebar.metric("ألواح فيبر", f"{round(tot_f, 1)} لوح")
        if st.sidebar.button("🗑️ مسح المشروع"):
            st.session_state.project_list = []
            st.rerun()

    # عرض النتائج
    for idx, item in enumerate(st.session_state.project_list):
        with st.container():
            st.markdown(f'<div class="unit-card"><h3>{idx+1}. {item["name"]} ({item["type"]}) - {item["dims"]}</h3>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<p class="table-title">⚔️ تقطيع الألومنيوم (DOGGA SYSTEM)</p>', unsafe_allow_html=True)
                st.table(item['alum_df'])
            with col2:
                st.markdown('<p class="table-title">🪵 تقطيع الفيبر</p>', unsafe_allow_html=True)
                st.table(item['fiber_df'])
                if item['notes']: st.info(f"📌 ملاحظات: {item['notes']}")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="footer-text">برمجة المهندس ياسين علاء © 2026</div>', unsafe_allow_html=True)
