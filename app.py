import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وحماية مجهود المهندس ياسين علاء
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

st.markdown("""
    <style>
    /* حماية مجهود المهندس: إخفاء القطة، المنيو، وأي زرار يظهر الكود */
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    [data-testid="stActionButtonIcon"] { display: none !important; }
    button[title="View source"] { display: none !important; }
    .stCodeBlock button { display: none !important; }
    
    /* منع تحديد النصوص بالماوس */
    body {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }

    /* تنسيق الجداول باللون الأصفر والأسود */
    .stTable td { 
        font-size: 20px !important; 
        font-weight: bold !important; 
        color: #1e272e !important;
        text-align: center !important;
        border: 1px solid #f1c40f !important;
    }
    .stTable th { 
        background-color: #f1c40f !important; 
        color: #1e272e !important; 
        font-size: 18px !important;
    }
    .header-box { 
        background-color: #1e272e; padding: 25px; border-radius: 15px; 
        border: 3px solid #f1c40f; border-bottom: 8px solid #f1c40f; 
        text-align: center; margin-bottom: 30px; 
    }
    .main-title { color: #f1c40f; font-size: 3em; margin: 0; font-weight: 900; }
    .sub-title { color: #ffffff; font-size: 1.4em; margin-top: 10px; font-weight: bold; }
    .engineer-name { color: #f1c40f; font-size: 1.2em; margin-top: 15px; font-weight: bold; }
    
    .table-header {
        background-color: #f1c40f; color: #1e272e; padding: 10px;
        border-radius: 5px; font-weight: bold; font-size: 1.3em;
        margin-top: 20px; text-align: right;
    }
    .unit-card { 
        background-color: #f8f9fa; padding: 20px; border-radius: 15px; 
        border-right: 15px solid #f1c40f; margin-bottom: 30px; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1); 
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة المخزن والصفحات
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []

# --- 1. واجهة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div class="header-box">
            <h1 class="main-title">DOGGA SYSTEM</h1>
            <p class="sub-title">المنظومة الذكية لتخصيمات المطابخ الحديثة</p>
            <p class="engineer-name">برمجة المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 دخول نظام التخصيم"):
            st.session_state.page = 'app'
            st.rerun()

# --- 2. التطبيق الرئيسي ---
elif st.session_state.page == 'app':
    st.sidebar.markdown("<h2 style='text-align:center; color:#f1c40f;'>📊 جرد الخامات</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align:center; color:white;'>م/ ياسين علاء</p>", unsafe_allow_html=True)
    
    with st.expander("➕ إضافة وحدة جديدة", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            u_name = st.text_input("اسم الوحدة")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])
            w = st.number_input("العرض (سم)", value=0.0)
            h = st.number_input("الارتفاع (سم)", value=0.0)
            d = st.number_input("العمق (سم)", value=0.0)
        with c2:
            st.write("**🧱 الرفوف والفواصل**")
            sh_w = st.number_input("عرض الرف", value=0.0)
            sh_d = st.number_input("عمق الرف", value=0.0)
            sh_n = st.number_input("عدد الرفوف", value=0)
            dv_h = st.number_input("ارتفاع الفاصل", value=0.0)
            dv_d = st.number_input("عمق الفاصل", value=0.0)
            dv_n = st.number_input("عدد الفواصل", value=0)
        with c3:
            st.write("**🗄️ الأدراج**")
            dr_w = st.number_input("عرض الدرج", value=0.0)
            dr_d = st.number_input("عمق الدرج", value=0.0)
            dr_n = st.number_input("عدد الأدراج", value=0)
            u_notes = st.text_area("ملاحظات")
            
            if st.button("✅ حفظ وتحسيب"):
                if w > 0 and h > 0:
                    # التخصيمات الأساسية (13 سم للسفلي و 5 سم للعالي)
                    h_b = int(h - 13) if u_type in ["سفلية", "دولاب خزين"] else int(h - 5)
                    w_b, d_b = int(w - 5), int(d - 5)
                    
                    # توزيع مفرد ومتقارب
                    if u_type == "سفلية":
                        h_m, h_t, w_m, w_t, d_m, d_t = 2, 2, 3, 1, 2, 2
                    else:
                        h_m, h_t, w_m, w_t, d_m, d_t = 2, 2, 2, 2, 0, 4

                    # جدول الألومنيوم
                    alum_rows = [
                        {"البند": "قوايم الارتفاع", "مقاس المفرد": h_b, "عدد": f"{h_m} ق", "مقاس المتقارب": h_b, "عدد ": f"{h_t} ق"},
                        {"البند": "عوارض العرض", "مقاس المفرد": w_b, "عدد": f"{w_m} ق", "مقاس المتقارب": w_b, "عدد ": f"{w_t} ق"},
                        {"البند": "عوارض العمق", "مقاس المفرد": d_b if d_m>0 else "-", "عدد": f"{d_m} ق" if d_m>0 else "-", "مقاس المتقارب": d_b if d_t>0 else "-", "عدد ": f"{d_t} ق" if d_t>0 else "-"}
                    ]
                    
                    # تخصيمات الرفوف والفواصل
                    if sh_n > 0:
                        alum_rows.append({"البند": "عوارض رف (عرض)", "مقاس المفرد": int(sh_w), "عدد": f"{sh_n*2} ق", "مقاس المتقارب": "-", "عدد ": "-"})
                        alum_rows.append({"البند": "عوارض رف (عمق)", "مقاس المفرد": int(sh_d), "عدد": f"{sh_n*2} ق", "مقاس المتقارب": "-", "عدد ": "-"})
                    if dv_n > 0:
                        alum_rows.append({"البند": "عوارض فاصل (ارتفاع)", "مقاس المفرد": int(dv_h), "عدد": f"{dv_n*2} ق", "مقاس المتقارب": "-", "عدد ": "-"})
                        alum_rows.append({"البند": "عوارض فاصل (عمق)", "مقاس المفرد": int(dv_d), "عدد": f"{dv_n*2} ق", "مقاس المتقارب": "-", "عدد ": "-"})
                    if dr_n > 0:
                        alum_rows.append({"البند": "إطار درج (عرض)", "مقاس المفرد": int(dr_w-2.5), "عدد": f"{dr_n*2} ق", "مقاس المتقارب": "-", "عدد ": "-"})
                        alum_rows.append({"البند": "إطار درج (عمق)", "مقاس المفرد": int(dr_d), "عدد": f"{dr_n*2} ق", "مقاس المتقارب": "-", "عدد ": "-"})

                    # جدول الفيبر
                    fiber_rows = [
                        {"القطعة": "فيبر ضهرية", "المقاس": f"{w_b} x {h_b}", "العدد": "1"},
                        {"القطعة": "فيبر أجناب", "المقاس": f"{h_b} x {d_b}", "العدد": "2"},
                        {"القطعة": "فيبر أرضية/سقف", "المقاس": f"{w_b} x {d_b}", "العدد": "1" if u_type=="سفلية" else "2"}
                    ]
                    if sh_n > 0: fiber_rows.append({"القطعة": "فيبر رف", "المقاس": f"{int(sh_w-5)} x {int(sh_d-5)}", "العدد": sh_n})
                    if dv_n > 0: fiber_rows.append({"القطعة": "فيبر فاصل", "المقاس": f"{int(dv_h-5)} x {int(dv_d-5)}", "العدد": dv_n})

                    # حساب الجرد
                    m_m = (h_b*h_m) + (w_b*w_m) + (d_b*d_m) + (sh_w*2 + sh_d*2)*sh_n + (dv_h*2 + dv_d*2)*dv_n + ((dr_w-2.5)*2 + dr_d*2)*dr_n
                    m_t = (h_b*h_t) + (w_b*w_t) + (d_b*d_t)
                    f_a = (w_b*h_b) + (h_b*d_b*2) + (w_b*d_b*(1 if u_type=="سفلية" else 2)) + (sh_w-5)*(sh_d-5)*sh_n + (dv_h-5)*(dv_d-5)*dv_n

                    st.session_state.project_list.append({
                        "name": u_name, "type": u_type, "dims": f"{w}x{h}x{d}",
                        "alum": pd.DataFrame(alum_rows), "fiber": pd.DataFrame(fiber_rows),
                        "m_m": m_m, "m_t": m_t, "f_a": f_a, "notes": u_notes
                    })
                    st.rerun()

    # السايد بار (الجرد)
    if st.session_state.project_list:
        tm = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        tt = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        tf = sum([x['f_a'] for x in st.session_state.project_list]) / (280*130)
        st.sidebar.metric("🪵 أعواد مفرد", f"{round(tm,1)} عود")
        st.sidebar.metric("🪵 أعواد متقارب", f"{round(tt,1)} عود")
        st.sidebar.metric("💎 ألواح فيبر", f"{round(tf,1)} لوح")
        if st.sidebar.button("🗑️ مسح الكل"): st.session_state.project_list = []; st.rerun()

    # عرض النتائج
    for idx, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><h3>#{idx+1} {item["name"]}</h3>', unsafe_allow_html=True)
        st.markdown(f'<div class="table-header">⚔️ ألومنيوم ({item["type"]})</div>', unsafe_allow_html=True)
        st.table(item['alum'])
        st.markdown(f'<div class="table-header">🪵 فيبر ({item["type"]})</div>', unsafe_allow_html=True)
        st.table(item['fiber'])
        if item['notes']: st.info(item['notes'])
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='text-align:center; padding:20px; font-weight:bold;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</div>", unsafe_allow_html=True)
