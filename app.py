import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وحماية الواجهة
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

# 2. تهيئة المخزن والحالات
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = True

# 3. نظام الألوان الديناميكي
bg = "#1e272e" if st.session_state.dark_mode else "#ffffff"
txt = "#ffffff" if st.session_state.dark_mode else "#1e272e"
card = "#2d3436" if st.session_state.dark_mode else "#f8f9fa"

st.markdown(f"""
    <style>
    /* إخفاء علامة القطة (GitHub) والمنيو واللوجو تماماً لحماية الشغل */
    header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    [data-testid="stActionButtonIcon"] {{ display: none !important; }}
    
    /* منع التحديد وحماية التصميم */
    body {{
        background-color: {bg} !important;
        color: {txt} !important;
        -webkit-user-select: none;
        user-select: none;
    }}

    .unit-card {{
        background-color: {card};
        padding: 25px;
        border-radius: 15px;
        border-right: 15px solid #f1c40f;
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }}
    
    .stTable td {{ color: {txt} !important; font-weight: bold; border: 1px solid #f1c40f !important; text-align: center; }}
    .stTable th {{ background-color: #f1c40f !important; color: #1e272e !important; }}
    </style>
""", unsafe_allow_html=True)

# 4. القائمة الجانبية (الأزرار + مخزن المشروع الكامل)
with st.sidebar:
    st.markdown("<h1 style='color:#f1c40f; text-align:center;'>DOGGA 2026</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{txt};'>برمجة: م/ ياسين علاء</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # أزرار التنقل والتحكم
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        if st.button("🏠 الرئيسية"):
            st.session_state.page = 'welcome'
            st.rerun()
    with c_s2:
        icon = "☀️" if st.session_state.dark_mode else "🌙"
        if st.button(icon):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # مخزن المشروع (حسابات الجرد الكلية)
    if st.session_state.project_list:
        st.markdown("---")
        st.markdown("<h3 style='color:#f1c40f;'>📊 إجمالي مخزن المشروع</h3>", unsafe_allow_html=True)
        total_mufard = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        total_motaqareb = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        total_fiber = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
        
        st.metric("🪵 أعواد مفرد", f"{round(total_mufard, 1)} عود")
        st.metric("🪵 أعواد متقارب", f"{round(total_motaqareb, 1)} عود")
        st.metric("💎 ألواح فيبر", f"{round(total_fiber, 1)} لوح")
        
        if st.button("🗑️ تفريغ المخزن", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

# 5. عرض الصفحات
if st.session_state.page == 'welcome':
    st.markdown('<div style="background-color:#1e272e; padding:40px; border-radius:15px; border:3px solid #f1c40f; text-align:center;">'
                '<h1 style="color:#f1c40f; margin:0; font-size:3.5em;">DOGGA SYSTEM</h1>'
                '<p style="color:white; font-size:1.5em;">المنظومة الاحترافية لتخصيمات المطابخ</p></div>', unsafe_allow_html=True)
    
    c_w1, c_w2, c_w3 = st.columns([1, 2, 1])
    with c_w2:
        st.write("\n")
        if st.button("🚀 دخول النظام", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

elif st.session_state.page == 'app':
    with st.expander("📝 إضافة تفاصيل ومقاسات الوحدة", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("اسم الوحدة")
            u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب"])
            w = st.number_input("العرض الكلي (سم)", value=0.0)
            h = st.number_input("الارتفاع الكلي (سم)", value=0.0)
            d = st.number_input("العمق الكلي (سم)", value=0.0)
        with col2:
            st.write("**🧱 الرفوف والفواصل**")
            sh_w = st.number_input("عرض الرف", value=0.0)
            sh_d = st.number_input("عمق الرف", value=0.0)
            sh_n = st.number_input("عدد الرفوف", value=0)
            dv_h = st.number_input("ارتفاع الفاصل", value=0.0) # خانة ارتفاع الفاصل
            dv_d = st.number_input("عمق الفاصل", value=0.0)    # خانة عمق الفاصل
            dv_n = st.number_input("عدد الفواصل", value=0)    # خانة عدد الفواصل
        with col3:
            st.write("**🗄️ الأدراج**")
            dr_w = st.number_input("عرض الدرج", value=0.0)
            dr_d = st.number_input("عمق الدرج", value=0.0)
            dr_n = st.number_input("عدد الأدراج", value=0)
            
            if st.button("✅ حفظ وتحسيب التخصيم", use_container_width=True):
                if w > 0 and h > 0:
                    # معادلات التخصيم الأساسية (13 سم للسفلي/الدولاب و 5 سم للعالي)
                    h_calc = int(h - 13) if u_type != "علوية" else int(h - 5)
                    w_calc, d_calc = int(w - 5), int(d - 5)
                    
                    # جداول الألومنيوم
                    alum_data = [
                        {"البند": "قوايم الارتفاع", "المقاس": h_calc, "العدد": "4 ق"},
                        {"البند": "عوارض العرض", "المقاس": w_calc, "العدد": "4 ق"},
                        {"البند": "عوارض العمق", "المقاس": d_calc, "العدد": "4 ق"}
                    ]
                    # إضافة الرفوف والفواصل والأدراج للجداول
                    if sh_n > 0: alum_data.append({"البند": "عوارض رف", "المقاس": f"{int(sh_w)}x{int(sh_d)}", "العدد": f"{sh_n*4} ق"})
                    if dv_n > 0: alum_data.append({"البند": "فواصل داخلية", "المقاس": f"{int(dv_h)}x{int(dv_d)}", "العدد": f"{dv_n*4} ق"})
                    if dr_n > 0: alum_data.append({"البند": "إطار درج", "المقاس": f"{int(dr_w-2.5)}x{int(dr_d)}", "العدد": f"{dr_n*4} ق"})

                    # تخزين البيانات في المخزن
                    st.session_state.project_list.append({
                        "name": name, "dims": f"{w}x{h}x{d}", "alum": pd.DataFrame(alum_data),
                        "m_m": (h_calc*4 + w_calc*4 + d_calc*4) + (sh_w*4*sh_n) + (dr_w*4*dr_n) + (dv_h*4*dv_n),
                        "m_t": (h_calc*2 + w_calc*2), "f_a": (w_calc*h_calc + h_calc*d_calc*2 + w_calc*d_calc)
                    })
                    st.rerun()

    # عرض كشوف تقطيع الوحدات المضافة
    for idx, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><h3>#{idx+1} {item["name"]} ({item["dims"]})</h3>', unsafe_allow_html=True)
        st.table(item['alum'])
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#f1c40f; padding:20px;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
