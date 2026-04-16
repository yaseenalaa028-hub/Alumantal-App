import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وتنسيق الألوان والخطوط (CSS)
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

st.markdown("""
    <style>
    /* تكبير الخط جداً ليكون واضح في الورشة وعلى الموبايل */
    .stTable td { 
        font-size: 24px !important; 
        font-weight: bold !important; 
        color: #1e272e !important;
        padding: 15px !important;
        text-align: center !important;
        border-bottom: 2px solid #ecf0f1 !important;
    }
    .stTable th { 
        background-color: #2c3e50 !important; 
        color: white !important; 
        font-size: 20px !important; 
        text-align: center !important;
    }
    /* تنسيق الكروت والهيدر */
    .header-box { background-color: #1e272e; padding: 25px; border-radius: 15px; border-bottom: 8px solid #f1c40f; text-align: center; margin-bottom: 25px; }
    .unit-card { background-color: #ffffff; padding: 25px; border-radius: 20px; border-right: 15px solid #f1c40f; margin-bottom: 35px; box-shadow: 0px 8px 20px rgba(0,0,0,0.15); }
    .footer-text { text-align: center; color: #2c3e50; padding: 15px; font-weight: bold; background: #f1c40f; border-radius: 10px; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []

# --- صفحة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="header-box">
            <h1 style="color: #f1c40f; font-size: 5em; margin:0; font-family: 'Arial Black';">DOGGA SYSTEM</h1>
            <h2 style="color: white; margin:0;">نظام التخصيم الفني المتكامل</h2>
            <p style="color: #bdc3c7; font-size: 1.8em; margin-top: 15px; font-weight: bold;">برمجة المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 دخول للنظام الاحترافي"):
            st.session_state.page = 'app'
            st.rerun()

# --- صفحة التطبيق الرئيسي ---
elif st.session_state.page == 'app':
    st.sidebar.markdown("<h2 style='text-align:center; color:#f1c40f;'>📊 جرد الخامات</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align:center; font-weight:bold;'>م/ ياسين علاء</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    with st.expander("➕ إضافة وحدة جديدة للمشروع (أدخل المقاسات)", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            u_name = st.text_input("اسم الوحدة", placeholder="مثلاً: وحدة حوض")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "أخرى"])
            w = st.number_input("العرض (سم)", value=None)
            h = st.number_input("الارتفاع (سم)", value=None)
            d = st.number_input("العمق (سم)", value=None)
        with c2:
            st.write("**🧱 الرفوف والفواصل**")
            sh_w = st.number_input("عرض الرف", value=None)
            sh_d = st.number_input("عمق الرف", value=None)
            sh_n = st.number_input("عدد الرفوف", value=0, step=1)
            dv_h = st.number_input("ارتفاع الفاصل", value=None)
            dv_d = st.number_input("عمق الفاصل", value=None)
            dv_n = st.number_input("عدد الفواصل", value=0, step=1)
        with c3:
            st.write("**🗄️ الأدراج**")
            dr_w = st.number_input("عرض الدرج", value=None)
            dr_d = st.number_input("عمق الدرج", value=None)
            dr_n = st.number_input("عدد الأدراج", value=0, step=1)
            u_notes = st.text_area("ملاحظات إضافية")
            
            if st.button("✅ تحسيب وحفظ"):
                if w and h:
                    # معادلات التخصيم الأساسية (تحويل لـ int لإلغاء الأصفار 77.0000)
                    h_b = int(h - 13) if u_type in ["سفلية", "دولاب خزين"] else int(h - 5)
                    w_b, d_b = int(w - 5), int(d - 5)
                    
                    # منطق توزيع (مفرد / متقارب) في أعمدة منفصلة
                    if u_type == "سفلية":
                        h_m, h_t = 2, 2   # الارتفاع
                        w_m, w_t = 3, 1   # العرض
                        d_m, d_t = 2, 2   # العمق
                    else:
                        h_m, h_t = 2, 2
                        w_m, w_t = 2, 2
                        d_m, d_t = 0, 4   # العلوية غالباً عمقها متقارب بالكامل

                    # بناء قائمة الألومنيوم بالأعمدة الجديدة
                    alum_data = [
                        {"البند": "قوايم الارتفاع", "المقاس": h_b, "مفرد": f"{h_m} ق", "متقارب": f"{h_t} ق"},
                        {"البند": "عوارض العرض", "المقاس": w_b, "مفرد": f"{w_m} ق", "متقارب": f"{w_t} ق"},
                        {"البند": "عوارض العمق", "المقاس": d_b, "مفرد": f"{d_m} ق", "متقارب": f"{d_t} ق"}
                    ]
                    
                    if sh_n > 0:
                        alum_data.append({"البند": "عوارض رف (عرض)", "المقاس": int(sh_w), "مفرد": f"{sh_n*2} ق", "متقارب": "-"})
                        alum_data.append({"البند": "عوارض رف (عمق)", "المقاس": int(sh_d), "مفرد": f"{sh_n*2} ق", "متقارب": "-"})
                    if dv_n > 0:
                        alum_data.append({"البند": "عوارض فاصل (ارتفاع)", "المقاس": int(dv_h), "مفرد": f"{dv_n*2} ق", "متقارب": "-"})
                        alum_data.append({"البند": "عوارض فاصل (عمق)", "المقاس": int(dv_d), "مفرد": f"{dv_n*2} ق", "متقارب": "-"})
                    if dr_n > 0:
                        alum_data.append({"البند": "إطار درج (عرض-2.5)", "المقاس": int(dr_w-2.5), "مفرد": f"{dr_n*2} ق", "متقارب": "-"})
                        alum_data.append({"البند": "إطار درج (عمق)", "المقاس": int(dr_d), "مفرد": f"{dr_n*2} ق", "متقارب": "-"})

                    # بناء قائمة الفيبر
                    fiber_data = [
                        {"القطعة": "فيبر ضهرية", "المقاس": f"{w_b} x {h_b}", "العدد": "1"},
                        {"القطعة": "فيبر أجناب", "المقاس": f"{h_b} x {d_b}", "العدد": "2"},
                        {"القطعة": "أرضية/سقف", "المقاس": f"{w_b} x {d_b}", "العدد": "1" if u_type=="سفلية" else "2"}
                    ]
                    if sh_n > 0: fiber_data.append({"القطعة": "فيبر رف", "المقاس": f"{int(sh_w-5)} x {int(sh_d-5)}", "العدد": int(sh_n)})
                    if dv_n > 0: fiber_data.append({"القطعة": "فيبر فاصل", "المقاس": f"{int(dv_h-5)} x {int(dv_d-5)}", "العدد": int(dv_n)})

                    # حساب الجرد التراكمي
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
                        "alum_df": pd.DataFrame(alum_data), "fiber_df": pd.DataFrame(fiber_data),
                        "m_m": m_m, "m_t": m_t, "f_a": f_area, "notes": u_notes
                    })
                    st.rerun()

    # تحديث السايد بار بالجرد المستمر
    if st.session_state.project_list:
        tot_m = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        tot_t = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        tot_f = sum([x['f_a'] for x in st.session_state.project_list]) / (280*130)
        
        st.sidebar.metric("🪵 أعواد مفرد (6م)", f"{round(tot_m, 1)} عود")
        st.sidebar.metric("🪵 أعواد متقارب (6م)", f"{round(tot_t, 1)} عود")
        st.sidebar.metric("💎 ألواح فيبر", f"{round(tot_f, 1)} لوح")
        if st.sidebar.button("🗑️ مسح المشروع بالكامل"):
            st.session_state.project_list = []
            st.rerun()

    # عرض كشوف التقطيع النهائية بشكل احترافي
    for idx, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><h2>#{idx+1} {item["name"]} ({item["dims"]} سم)</h2>', unsafe_allow_html=True)
        
        st.markdown('<p style="font-size:1.4em; color:#2c3e50; font-weight:bold; border-right: 10px solid #2980b9; padding-right:10px;">⚔️ تقطيع الألومنيوم (DOGGA):</p>', unsafe_allow_html=True)
        st.table(item['alum_df']) # الجداول دلوقتي فيها (مفرد) و (متقارب) في أعمدة منفصلة
        
        st.markdown('<p style="font-size:1.4em; color:#2c3e50; font-weight:bold; border-right: 10px solid #27ae60; padding-right:10px;">🪵 تقطيع الفيبر الصافي:</p>', unsafe_allow_html=True)
        st.table(item['fiber_df'])
        
        if item['notes']:
            st.info(f"📌 ملاحظات الفني: {item['notes']}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="footer-text">برمجة المهندس ياسين علاء - DOGGA SYSTEM 2026</div>', unsafe_allow_html=True)
