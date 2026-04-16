import streamlit as st
import pandas as pd
import time

# ==========================================
# 1. إعدادات المنظومة وحماية مجهود المهندس ياسين
# ==========================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. تهيئة مخزن البيانات (Session State)
# ==========================================
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# ==========================================
# 3. نظام الألوان المتغير (Dark/Light Mode)
# ==========================================
if st.session_state.dark_mode:
    primary_bg = "#1e272e"
    secondary_bg = "#2d3436"
    text_color = "#ffffff"
    accent_color = "#f1c40f"
else:
    primary_bg = "#ffffff"
    secondary_bg = "#f8f9fa"
    text_color = "#1e272e"
    accent_color = "#d4ac0d"

# ==========================================
# 4. واجهة المستخدم الرسومية (CSS) - حماية كاملة
# ==========================================
st.markdown(f"""
    <style>
    header {{visibility: hidden !important;}}
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    [data-testid="stActionButtonIcon"] {{ display: none !important; }}
    
    body {{
        background-color: {primary_bg} !important;
        color: {text_color} !important;
        -webkit-user-select: none;
        user-select: none;
    }}

    .unit-card {{
        background-color: {secondary_bg};
        padding: 30px;
        border-radius: 20px;
        border-right: 15px solid {accent_color};
        margin-bottom: 35px;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4);
    }}
    
    .stTable td {{ 
        color: {text_color} !important; 
        font-weight: bold !important; 
        font-size: 17px !important;
        border: 1px solid {accent_color} !important;
        text-align: center !important;
    }}
    .stTable th {{ 
        background-color: {accent_color} !important; 
        color: #1e272e !important; 
        font-size: 18px !important;
    }}

    .header-box {{
        background-color: #1e272e;
        padding: 40px;
        border-radius: 25px;
        border: 4px solid {accent_color};
        border-bottom: 15px solid {accent_color};
        text-align: center;
        margin-bottom: 50px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 5. القائمة الجانبية (Sidebar) - مركز التحكم والمخزن
# ==========================================
with st.sidebar:
    st.markdown(f"<h1 style='color:{accent_color}; text-align:center;'>DOGGA 2026</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; color:{text_color};'>المهندس ياسين علاء</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid #f1c40f;'>", unsafe_allow_html=True)
    
    st.subheader("⚙️ أدوات التحكم")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()
    with c2:
        icon = "☀️" if st.session_state.dark_mode else "🌙"
        if st.button(icon, use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    if st.session_state.project_list:
        st.markdown("<hr style='border: 1px solid #f1c40f;'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{accent_color}; text-align:center;'>📦 مخزن الخامات</h3>", unsafe_allow_html=True)
        
        total_mufard = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        total_motaqareb = sum([x['m_t'] for x in st.session_state.project_list]) / 600
        total_fiber = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
        
        st.metric("🪵 أعواد مفرد", f"{round(total_mufard, 1)}")
        st.metric("🪵 أعواد متقارب", f"{round(total_motaqareb, 1)}")
        st.metric("💎 ألواح فيبر", f"{round(total_fiber, 1)}")
        
        if st.button("🗑️ تفريغ المخزن", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

# ==========================================
# 6. إدارة الشاشات
# ==========================================

if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div class="header-box">
            <h1 style="color:{accent_color}; font-size:4.5em; margin:0; font-weight:900;">DOGGA SYSTEM</h1>
            <p style="color:white; font-size:1.8em; font-weight:bold;">برمجة المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    c_w1, c_w2, c_w3 = st.columns([1, 2, 1])
    with c_w2:
        if st.button("🚀 دخول نظام التخصيم", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

elif st.session_state.page == 'app':
    st.markdown(f"<h2 style='color:{accent_color};'>📋 إدخال المقاسات</h2>", unsafe_allow_html=True)
    
    with st.expander("➕ إضافة وحدة جديدة", expanded=True):
        col_in1, col_in2, col_in3 = st.columns(3)
        
        with col_in1:
            name = st.text_input("اسم القطعة")
            u_type = st.selectbox("النوع", ["سفلية (13سم)", "علوية (5سم)", "دولاب (13سم)"])
            # تم إزالة الصفر الافتراضي باستخدام value=None لجعل الخانة فارغة
            width = st.number_input("العرض (W)", value=None, placeholder="0.0")
            height = st.number_input("الارتفاع (H)", value=None, placeholder="0.0")
            depth = st.number_input("العمق (D)", value=None, placeholder="0.0")
            
        with col_in2:
            st.markdown(f"<b style='color:{accent_color};'>🧱 الرفوف والفواصل</b>")
            sh_w = st.number_input("عرض الرف", value=None, placeholder="0.0")
            sh_d = st.number_input("عمق الرف", value=None, placeholder="0.0")
            sh_n = st.number_input("عدد الرفوف", value=0)
            st.markdown("---")
            dv_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="0.0")
            dv_d = st.number_input("عمق الفاصل", value=None, placeholder="0.0")
            dv_n = st.number_input("عدد الفواصل", value=0)
            
        with col_in3:
            st.markdown(f"<b style='color:{accent_color};'>🗄️ الأدراج</b>")
            dr_w = st.number_input("عرض الدرج", value=None, placeholder="0.0")
            dr_d = st.number_input("عمق الدرج", value=None, placeholder="0.0")
            dr_n = st.number_input("عدد الأدراج", value=0)
            
            if st.button("✅ حفظ وتحسيب", use_container_width=True):
                if width and height:
                    ded = 13 if "13" in u_type else 5
                    h_n, w_n, d_n = int(height - ded), int(width - 5), int(depth - 5)
                    
                    alum = [
                        {"البيان": "قوايم", "المقاس": h_n, "العدد": "4 ق"},
                        {"البيان": "عوارض", "المقاس": w_n, "العدد": "4 ق"},
                        {"البيان": "أجناب", "المقاس": d_n, "العدد": "4 ق"}
                    ]
                    
                    if sh_n > 0: alum.append({"البيان": "رفوف", "المقاس": f"{int(sh_w)}x{int(sh_d)}", "العدد": f"{sh_n*4}ق"})
                    if dv_n > 0: alum.append({"البيان": "فواصل", "المقاس": f"{int(dv_h)}x{int(dv_d)}", "العدد": f"{dv_n*4}ق"})
                    if dr_n > 0: alum.append({"البيان": "درج", "المقاس": f"{int(dr_w-2.5)}x{int(dr_d)}", "العدد": f"{dr_n*4}ق"})

                    # كشف الفيبر
                    fiber = [
                        {"القطعة": "ظهر", "المقاس": f"{w_n}x{h_n}"},
                        {"القطعة": "أجناب", "المقاس": f"{h_n}x{d_n}"},
                        {"القطعة": "أرضية", "المقاس": f"{w_n}x{d_n}"}
                    ]

                    st.session_state.project_list.append({
                        "name": name, "dims": f"{width}x{height}", 
                        "alum": pd.DataFrame(alum), "fiber": pd.DataFrame(fiber),
                        "m_m": (h_n*4 + w_n*4 + d_n*4) + (sh_w or 0)*4*sh_n,
                        "m_t": (h_n*2 + w_n*2), "f_a": (w_n*h_n) + (h_n*d_n*2)
                    })
                    st.rerun()

    for i, item in enumerate(st.session_state.project_list):
        st.markdown(f'<div class="unit-card"><h3>#{i+1} {item["name"]} ({item["dims"]})</h3>', unsafe_allow_html=True)
        c_res1, c_res2 = st.columns([2, 1])
        with c_res1: st.table(item['alum'])
        with c_res2: st.table(item['fiber'])
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center; color:{accent_color}; font-weight:bold;'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
