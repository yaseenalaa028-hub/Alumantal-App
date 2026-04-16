import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والستايل الفني المطور (Professional Branding)
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

st.markdown("""
    <style>
    /* تنسيق الجداول: وضوح تام وأرقام بارزة */
    .stTable td { 
        font-size: 22px !important; 
        font-weight: bold !important; 
        color: #1e272e !important;
        text-align: center !important;
        border: 1px solid #bdc3c7 !important;
        padding: 12px !important;
    }
    .stTable th { 
        background-color: #2c3e50 !important; 
        color: white !important; 
        font-size: 19px !important; 
        text-align: center !important;
    }
    /* الهيدر المنسق الجديد */
    .header-box { 
        background-color: #1e272e; 
        padding: 20px; 
        border-radius: 12px; 
        border-bottom: 5px solid #f1c40f; 
        text-align: center; 
        margin-bottom: 25px; 
    }
    .main-title { 
        color: #f1c40f; 
        font-size: 2.8em; 
        margin: 0; 
        letter-spacing: 2px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .sub-title { 
        color: #ecf0f1; 
        font-size: 1.2em; 
        margin-top: 5px; 
        opacity: 0.9;
    }
    /* برواز الوحدات */
    .table-header {
        background-color: #f1c40f;
        color: #2c3e50;
        padding: 8px 15px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 1.3em;
        margin-top: 15px;
        margin-bottom: 10px;
        border-right: 8px solid #2c3e50;
    }
    .unit-card { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        border-right: 12px solid #2c3e50; 
        margin-bottom: 30px; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05); 
    }
    .footer-text { 
        text-align: center; 
        color: #2c3e50; 
        padding: 10px; 
        font-weight: bold; 
        background: #f1c40f; 
        border-radius: 8px; 
        margin-top: 30px; 
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة الصفحات والمخزن
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []

# --- 1. واجهة الترحيب المنسقة ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="header-box">
            <h1 class="main-title">DOGGA SYSTEM</h1>
            <p class="sub-title">المنظومة الذكية لتخصيمات المطابخ الحديثة</p>
            <hr style="width:20%; margin: 15px auto; border-color: #f1c40f;">
            <p style="color: #bdc3c7; font-size: 1.3em; font-weight: bold;">إشراف هندسي: ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 ابدأ العمل الآن"):
            st.session_state.page = 'app'
            st.rerun()

# --- 2. التطبيق الرئيسي ---
elif st.session_state.page == 'app':
    st.sidebar.markdown("<h3 style='text-align:center; color:#f1c40f;'>📦 إجمالي المشروع</h3>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align:center;'>م/ ياسين علاء</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    with st.expander("➕ إضافة وحدة جديدة", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            u_name = st.text_input("اسم الوحدة")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
            w = st.number_input("العرض (سم)", value=None)
            h = st.number_input("الارتفاع (سم)", value=None)
            d = st.number_input("العمق (سم)", value=None)
        with c2:
            st.write("**🧱 الرفوف والفواصل**")
            sh_w, sh_d, sh_n = st.number_input("عرض الرف", value=None), st.number_input("عمق الرف", value=None), st.number_input("عدد الرفوف", value=0)
            dv_h, dv_d, dv_n = st.number_input("ارتفاع الفاصل", value=None), st.number_input("عمق الفاصل", value=None), st.number_input("عدد الفواصل", value=0)
        with c3:
            st.write("**🗄️ الأدراج**")
            dr_w, dr_d, dr_n = st.number_input("عرض الدرج", value=None), st.number_input("عمق الدرج", value=None), st.number_input("عدد الأدراج", value=0)
            u_notes = st.text_area("ملاحظات فنية")
            
            if st.button("✅ حفظ البيانات"):
                if w and h:
                    # تخصيمات الألومنيوم
                    h_b = int(h - 13) if u_type in ["سفلية", "دولاب خزين"] else int(h - 5)
                    w_b, d_b = int(w - 5), int(d - 5)
                    
                    if u_type == "سفلية":
                        h_m, h_t, w_m, w_t, d_m, d_t = 2, 2, 3, 1, 2, 2
                    else:
                        h_m, h_t, w_m, w_t, d_m, d_t = 2, 2, 2, 2, 0, 4

                    alum_rows = [
                        {"البند": "قوايم الارتفاع", "مقاس المفرد": h_b, "عدد المفرد": f"{h_m} ق", "مقاس المتقارب": h_b, "عدد المتقارب": f"{h_t} ق"},
                        {"البند": "عوارض العرض", "مقاس المفرد": w_b, "عدد المفرد": f"{w_m} ق", "مقاس المتقارب": w_b, "عدد المتقارب": f"{w_t} ق"},
                        {"البند": "عوارض العمق", 
                         "مقاس المفرد": d_b if d_m > 0 else "-", "عدد المفرد": f"{d_m} ق" if d_m > 0 else "-", 
                         "مقاس المتقارب": d_b if d_t > 0 else "-", "عدد المتقارب": f"{d_t} ق" if d_t > 0 else "-"}
                    ]
                    
                    if sh_n > 0:
                        alum_rows.append({"البند": "عوارض رف (عرض)", "مقاس المفرد": int(sh_w), "عدد المفرد": f"{int(sh_n*2)} ق", "مقاس المتقارب": "-", "عدد المتقارب": "-"})
                        alum_rows.append({"البند": "عوارض رف (عمق)", "مقاس المفرد": int(sh_d), "عدد المفرد": f"{int(sh_n*2)} ق", "مقاس المتقارب": "-", "عدد المتقارب": "-"})
                    if dv_n > 0:
                        alum_rows.append({"البند": "عوارض فاصل (ارتفاع)", "مقاس المفرد": int(dv_h), "عدد المفرد": f"{int(dv_n*2)} ق", "مقاس المتقارب": "-", "عدد المتقارب": "-"})
                        alum_rows.append({"البند": "عوارض فاصل (عمق)", "مقاس المفرد": int(dv_d), "عدد المفرد": f"{int(dv_n*2)} ق", "مقاس المتقارب": "-", "عدد المتقارب": "-"})
                    if dr_n > 0:
                        alum_rows.append({"البند": "إطار درج (عرض)", "مقاس المفرد": int(dr_w-2.5), "عدد المفرد": f"{int(dr_n*2)} ق", "مقاس المتقارب": "-", "عدد المتقارب": "-"})
                        alum_rows.append({"البند": "إطار درج (عمق)", "مقاس المفرد": int(dr_d), "عدد المفرد": f"{int(dr_n*2)} ق", "مقاس المتقارب": "-", "عدد المتقارب": "-"})

                    fiber_rows = [
                        {"القطعة": "فيبر ضهرية", "المقاس الصافي": f"{w_b} x {h_b}", "العدد": "1"},
                        {"القطعة": "فيبر أجناب", "المقاس الصافي": f"{h_b} x {d_b}", "العدد": "2"},
                        {"القطعة": "فيبر أرضية/سقف", "المقاس الصافي": f"{w_b} x {d_b}", "العدد": "1" if u_type=="سفلية" else "2"}
                    ]
                    if sh_n > 0: fiber_rows.append({"القطعة": "فيبر رف", "المقاس الصافي": f"{int(sh_w-5)} x {int(sh_d-5)}", "العدد": int(sh_n)})
                    if dv_n > 0: fiber_rows.append({"القطعة": "فيبر فاصل", "المقاس الصافي": f"{int(dv_h-5)} x {int(dv_d-5)}", "العدد": int(dv_n)})

                    m_m = (h_b * h_m) + (w_b * w_m) + (d_b * d_m)
                    m_t = (h_b * h_t) + (w_b * w_t) + (d_b * d_t)
                    if sh_n: m_m += (sh_w*2 + sh_d*2) * sh_n
                    if dv_n: m_m += (dv_h*2 + dv_d*2) * dv_n
                    if dr_n: m_m += ((dr_w-2.5)*2 + dr_d*2) * dr_n
                    f_area = (w_b*h_b) + (h_b*d_b*2) + (w_b*d_b*(1 if u_type=="سفلية" else 2))
                    if sh_n: f_area += (sh_w-5)*(sh_d-5)*sh_n
                    if dv_n: f_area += (dv_h-5)*(dv_d-5)*dv_n

                    st.session_state.project_list.append({
                        "name": u_name, "type": u_type, "dims": f"{w}x{h}x{d}", 
                        "alum": pd.DataFrame(alum_rows), "fiber": pd.DataFrame(fiber_rows),
                        "m_m": m_m, "m_t": m_t, "f_a": f_area, "notes": u_notes
                    })
                    st.rerun()

    # جرد السايد بار
    if st.session_state.project_list:
        tot_m = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        tot_t = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        tot_f = sum([x['f_a'] for x in st.session_state.project_list]) / (280*130)
        st.sidebar.metric("🪵 أعواد مفرد", f"{round(tot_m, 1)} عود")
        st.sidebar.metric("🪵 أعواد متقارب", f"{round(tot_t, 1)} عود")
        st.sidebar.metric("💎 ألواح فيبر", f"{round(tot_f, 1)} لوح")
        if st.sidebar.button("🗑️ مسح المشروع"): st.session_state.project_list = []; st.rerun()

    # عرض كشوف التقطيع
    for idx, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><h3>#{idx+1} {item["name"]} ({item["dims"]} سم)</h3>', unsafe_allow_html=True)
        st.markdown(f'<div class="table-header">⚔️ تقطيع ألومنيوم - وحدة ({item["type"]})</div>', unsafe_allow_html=True)
        st.table(item['alum'])
        st.markdown(f'<div class="table-header">🪵 تقطيع فيبر - وحدة ({item["type"]})</div>', unsafe_allow_html=True)
        st.table(item['fiber'])
        if item['notes']: st.warning(f"📌 {item['notes']}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="footer-text">DOGGA SYSTEM 2026 | م/ ياسين علاء</div>', unsafe_allow_html=True)
