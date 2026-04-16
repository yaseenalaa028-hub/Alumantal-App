import streamlit as st
import pandas as pd
import time

# =========================================================
# 1. إعدادات المنظومة (أهم سطر لفرش الشاشة بالعرض)
# =========================================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    page_icon="📐",
    layout="wide",  # فرش المحتوى بعرض الشاشة بالكامل
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. إدارة الحالة (الوضع الليلي، الصفحات، المخزن)
# =========================================================
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# =========================================================
# 3. محرك الألوان المتغير (Logic)
# =========================================================
if st.session_state.dark_mode:
    bg = "#0e1117"  # أسود غامق احترافي
    card = "#161b22"
    txt = "#ffffff"
    accent = "#f1c40f"
    table_edge = "#30363d"
else:
    bg = "#ffffff"
    card = "#f6f8fa"
    txt = "#0e1117"
    accent = "#d4ac0d"
    table_edge = "#d0d7de"

# =========================================================
# 4. التنسيق المتقدم (CSS) - حل مشكلة "الكلام بالطول"
# =========================================================
st.markdown(f"""
    <style>
    /* إجبار Streamlit على استغلال 95% من عرض الشاشة */
    .block-container {{
        max-width: 95% !important;
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }}
    
    /* ضبط الخلفية والخطوط */
    .stApp {{
        background-color: {bg} !important;
        color: {txt} !important;
        direction: rtl !important;
    }}
    
    /* تصميم الكروت العريضة جداً للنتائج */
    .unit-card {{
        background-color: {card};
        padding: 25px;
        border-radius: 15px;
        border-right: 12px solid {accent};
        margin-bottom: 25px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }}

    /* تجميل الجداول لتملأ العرض */
    .stTable {{
        width: 100% !important;
    }}
    
    /* إخفاء الزوائد */
    header, footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 5. القائمة الجانبية (Sidebar) - مركز التحكم
# =========================================================
with st.sidebar:
    st.markdown(f"<h1 style='text-align:center; color:{accent};'>DOGGA 2026</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-weight:bold;'>المهندس: ياسين علاء</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # تشغيل زرار الـ Dark Mode فعلياً
    mode_text = "☀️ تفعيل الوضع النهاري" if st.session_state.dark_mode else "🌙 تفعيل الوضع الليلي"
    if st.button(mode_text, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    if st.button("🏠 العودة للرئيسية", use_container_width=True):
        st.session_state.page = 'welcome'
        st.rerun()

    # مخزن المشروع (حساب تراكمي)
    if st.session_state.project_list:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"### 📦 مخزن المشروع ({len(st.session_state.project_list)} قطع)")
        t_m = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        t_f = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
        st.metric("أعواد ألومنيوم (6م)", f"{round(t_m, 1)}")
        st.metric("ألواح فيبر", f"{round(t_f, 1)}")
        if st.button("🗑️ مسح المشروع", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

# =========================================================
# 6. إدارة الشاشات والمحتوى
# =========================================================

# --- شاشة الترحيب ---
if st.session_state.page == 'welcome':
    st.markdown(f"""
        <div style="text-align:center; padding-top:100px;">
            <h1 style="color:{accent}; font-size:6em; font-weight:900; margin-bottom:0;">DOGGA SYSTEM</h1>
            <h2 style="color:{txt}; font-size:2.5em;">نظام التخصيم الفني الشامل</h2>
            <p style="font-size:1.8em; color:{accent};">برمجة المهندس ياسين علاء</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_w1, col_w2, col_w3 = st.columns([1, 1, 1])
    with col_w2:
        if st.button("🚀 ابدأ العمل الآن", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

# --- شاشة التطبيق الرئيسية ---
elif st.session_state.page == 'app':
    st.markdown(f"<h2 style='color:{accent};'>📋 لوحة إضافة الوحدات والتخصيم</h2>", unsafe_allow_html=True)
    
    # توزيع الخانات بالعرض لمنع "المط" الطولي
    with st.container():
        c1, c2, c3 = st.columns([1, 1, 1])
        
        with c1:
            st.markdown(f"<b style='color:{accent};'>📏 المقاسات الأساسية</b>", unsafe_allow_html=True)
            u_name = st.text_input("اسم الوحدة (كود)")
            u_type = st.selectbox("نوع التخصيم", ["سفلية (خصم 13سم)", "علوية (خصم 5سم)", "دولاب (خصم 13سم)"])
            # الخانات جاهزة بدون أصفار تعيق الكتابة
            w = st.number_input("العرض الكلي (W)", value=None, placeholder="0.0")
            h = st.number_input("الارتفاع الكلي (H)", value=None, placeholder="0.0")
            d = st.number_input("العمق الكلي (D)", value=None, placeholder="0.0")
            
        with c2:
            st.markdown(f"<b style='color:{accent};'>🧱 الرفوف والفواصل</b>", unsafe_allow_html=True)
            sh_w, sh_d, sh_n = st.columns(3)
            with sh_w: s_w = st.number_input("عرض الرف", value=None, placeholder="0.0")
            with sh_d: s_d = st.number_input("عمق الرف", value=None, placeholder="0.0")
            with sh_n: s_n = st.number_input("عدد الرفوف", value=None, placeholder="0")
            
            st.write("---")
            dv_h, dv_d, dv_n = st.columns(3)
            with dv_h: d_h = st.number_input("ارتفاع فاصل", value=None, placeholder="0.0")
            with dv_d: d_d = st.number_input("عمق فاصل", value=None, placeholder="0.0")
            with dv_n: d_n = st.number_input("عدد فواصل", value=None, placeholder="0")

        with c3:
            st.markdown(f"<b style='color:{accent};'>🗄️ الأدراج والإضافات</b>", unsafe_allow_html=True)
            dr_w, dr_d, dr_n = st.columns(3)
            with dr_w: r_w = st.number_input("عرض درج", value=None, placeholder="0.0")
            with dr_d: r_d = st.number_input("عمق درج", value=None, placeholder="0.0")
            with dr_n: r_n = st.number_input("عدد أدراج", value=None, placeholder="0")
            
            st.write("---")
            note = st.text_area("ملاحظات فنية للورشة")
            
            if st.button("✅ تنفيذ التخصيم وجرد الخامات", use_container_width=True):
                if w and h:
                    # معادلات التخصيم
                    ded = 13 if "13" in u_type else 5
                    h_n, w_n, d_n = int(h - ded), int(w - 5), int((d or 0) - 5)
                    
                    # كشوفات الألومنيوم
                    alum = [
                        {"البيان": "قوايم الارتفاع", "المقاس": h_n, "العدد": "4 ق"},
                        {"البيان": "عوارض العرض", "المقاس": w_n, "العدد": "4 ق"},
                        {"البيان": "عوارض العمق", "المقاس": d_n, "العدد": "4 ق"}
                    ]
                    # تفاصيل إضافية
                    if s_n: alum.append({"البيان": "أعواد رفوف", "المقاس": f"{int(s_w)}x{int(s_d)}", "العدد": f"{int(s_n)*4} ق"})
                    if d_n: alum.append({"البيان": "أعواد فواصل", "المقاس": f"{int(d_h)}x{int(d_d)}", "العدد": f"{int(d_n)*4} ق"})
                    if r_n: alum.append({"البيان": "إطارات أدراج", "المقاس": f"{int(r_w-2.5)}x{int(r_d)}", "العدد": f"{int(r_n)*4} ق"})

                    # كشف الفيبر
                    fiber = [
                        {"القطعة": "فيبر ظهر", "المقاس": f"{w_n}x{h_n}", "العدد": "1"},
                        {"القطعة": "فيبر أجناب", "المقاس": f"{h_n}x{d_n}", "العدد": "2"},
                        {"القطعة": "أرضية/سقف", "المقاس": f"{w_n}x{d_n}", "العدد": "2"}
                    ]

                    # حسابات الجرد الكلية
                    m_m = (h_n*4 + w_n*4 + d_n*4) + (int(s_w or 0)*4*int(s_n or 0)) + (int(d_h or 0)*4*int(d_n or 0))
                    f_a = (w_n*h_n) + (h_n*d_n*2) + (w_n*d_n*2)

                    st.session_state.project_list.append({
                        "name": u_name, "dims": f"{w}x{h}x{d}", "type": u_type,
                        "alum_df": pd.DataFrame(alum), "fiber_df": pd.DataFrame(fiber),
                        "m_m": m_m, "f_a": f_a, "note": note
                    })
                    st.rerun()

    # --- عرض النتائج في كروت عريضة ---
    st.markdown("---")
    for i, item in enumerate(st.session_state.project_list):
        st.markdown(f"""
            <div class="unit-card">
                <h2 style="color:{accent}; margin:0;">#{i+1} {item['name']} | مقاس {item['dims']} | ({item['type']})</h2>
            </div>
        """, unsafe_allow_html=True)
        
        r1, r2 = st.columns([2.5, 1])
        with r1:
            st.write("**⚒️ جدول تقطيع الألومنيوم:**")
            st.table(item['alum_df'])
        with r2:
            st.write("**🪵 جدول مقاسات الفيبر:**")
            st.table(item['fiber_df'])
            if item['note']: st.warning(f"📌 {item['note']}")

# تذييل المنظومة
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:{accent}; font-weight:bold; font-size:1.2em;'>DOGGA SYSTEM 2026 | تطوير المهندس ياسين علاء</p>", unsafe_allow_html=True)
