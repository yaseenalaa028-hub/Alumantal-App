import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية وحماية الواجهة
st.set_page_config(page_title="DOGGA SYSTEM | م/ ياسين علاء", layout="wide")

# 2. تهيئة مخزن البيانات والحالات (Session State)
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'project_list' not in st.session_state: st.session_state.project_list = []
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = True

# 3. إعدادات الألوان بناءً على وضع الإضاءة المختار
bg = "#1e272e" if st.session_state.dark_mode else "#ffffff"
txt = "#ffffff" if st.session_state.dark_mode else "#1e272e"
card = "#2d3436" if st.session_state.dark_mode else "#f8f9fa"

# 4. تنسيق CSS لإخفاء القطة وحماية مجهود المهندس
st.markdown(f"""
    <style>
    /* إخفاء علامة القطة (GitHub) والمنيو العلوي تماماً */
    header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    [data-testid="stActionButtonIcon"] {{ display: none !important; }}
    
    /* حماية النصوص من النسخ والتحديد */
    body {{
        background-color: {bg} !important;
        color: {txt} !important;
        -webkit-user-select: none;
        user-select: none;
    }}

    /* تنسيق كروت الوحدات والجداول */
    .unit-card {{
        background-color: {card};
        padding: 25px;
        border-radius: 15px;
        border-right: 12px solid #f1c40f;
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }}
    .stTable td {{ color: {txt} !important; font-weight: bold; border: 1px solid #f1c40f !important; }}
    .stTable th {{ background-color: #f1c40f !important; color: #1e272e !important; }}
    
    .header-box {{
        background-color: #1e272e; padding: 25px; border-radius: 15px;
        border: 3px solid #f1c40f; text-align: center; margin-bottom: 30px;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. القائمة الجانبية (Sidebar) - أزرار التحكم والجرد
with st.sidebar:
    st.markdown("<h1 style='color:#f1c40f; text-align:center;'>DOGGA 2026</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{txt};'>م/ ياسين علاء</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # أزرار التحكم (الرجوع للرئيسية وتبديل الإضاءة)
    c_side1, c_side2 = st.columns(2)
    with c_side1:
        if st.button("🏠 الرئيسية"):
            st.session_state.page = 'welcome'
            st.rerun()
    with c_side2:
        mode_label = "☀️" if st.session_state.dark_mode else "🌙"
        if st.button(mode_label):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    # قسم جرد الخامات (يظهر فقط إذا كان هناك بيانات)
    if st.session_state.project_list:
        st.markdown("---")
        st.markdown("<h3 style='color:#f1c40f;'>📊 إجمالي الخامات</h3>", unsafe_allow_html=True)
        total_m = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        total_t = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        total_f = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
        st.metric("🪵 أعواد مفرد", f"{round(total_m,1)}")
        st.metric("🪵 أعواد متقارب", f"{round(total_t,1)}")
        st.metric("💎 ألواح فيبر", f"{round(total_f,1)}")
        if st.button("🗑️ مسح المشروع"):
            st.session_state.project_list = []
            st.rerun()

# 6. عرض الشاشات (Navigation)

# --- شاشة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown("""
        <div class="header-box">
            <h1 style="color:#f1c40f; font-size:3em; margin:0;">DOGGA SYSTEM</h1>
            <p style="color:white; font-size:1.2em;">المنظومة الاحترافية لتخصيمات المطابخ الحديثة</p>
            <p style="color:#f1c40f; font-weight:bold;">برمجة المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        if st.button("🚀 دخول النظام", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- شاشة التطبيق الرئيسية ---
elif st.session_state.page == 'app':
    with st.expander("📝 إضافة وحدة جديدة", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("اسم الوحدة")
            u_type = st.selectbox("النوع", ["سفلية", "علوية", "دولاب خزين"])
            w = st.number_input("العرض (سم)", value=0.0)
            h = st.number_input("الارتفاع (سم)", value=0.0)
            d = st.number_input("العمق (سم)", value=0.0)
        with c2:
            st.write("**🧱 الرفوف**")
            sh_w = st.number_input("عرض الرف", value=0.0)
            sh_d = st.number_input("عمق الرف", value=0.0)
            sh_n = st.number_input("عدد الرفوف", value=0)
        with c3:
            st.write("**🗄️ الأدراج والملاحظات**")
            dr_w = st.number_input("عرض الدرج", value=0.0)
            dr_d = st.number_input("عمق الدرج", value=0.0)
            dr_n = st.number_input("عدد الأدراج", value=0)
            if st.button("✅ تحسيب وحفظ", use_container_width=True):
                if w > 0 and h > 0:
                    # معادلات التخصيم: 13 سم للسفلي و 5 سم للعالي
                    h_calc = int(h - 13) if u_type in ["سفلية", "دولاب خزين"] else int(h - 5)
                    w_calc, d_calc = int(w - 5), int(d - 5)
                    
                    # جداول الألومنيوم
                    alum_data = [
                        {"البند": "قوايم الارتفاع", "المقاس": h_calc, "العدد": "4 ق"},
                        {"البند": "عوارض العرض", "المقاس": w_calc, "العدد": "4 ق"},
                        {"البند": "عوارض العمق", "المقاس": d_calc, "العدد": "4 ق"}
                    ]
                    if sh_n > 0: alum_data.append({"البند": "عوارض رف", "المقاس": f"{int(sh_w)}x{int(sh_d)}", "العدد": f"{sh_n*4} ق"})
                    if dr_n > 0: alum_data.append({"البند": "إطار درج", "المقاس": f"{int(dr_w-2.5)}x{int(dr_d)}", "العدد": f"{dr_n*4} ق"})

                    st.session_state.project_list.append({
                        "name": name, "dims": f"{w}x{h}x{d}", "alum": pd.DataFrame(alum_data),
                        "m_m": (h_calc*4 + w_calc*4 + d_calc*4) + (sh_w*4*sh_n) + (dr_w*4*dr_n),
                        "m_t": (h_calc*2 + w_calc*2), "f_a": (w_calc*h_calc + h_calc*d_calc*2 + w_calc*d_calc)
                    })
                    st.rerun()

    # عرض كشوف التقطيع المحفوظة
    for idx, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><h3>#{idx+1} {item["name"]} ({item["dims"]})</h3>', unsafe_allow_html=True)
        st.table(item['alum'])
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#f1c40f; padding:20px;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
