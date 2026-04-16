import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات المنظومة (العرض الكامل)
# ==========================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    page_icon="📐",
    layout="wide", # دي اللي بتخلي الكلام مفرود بعرض الشاشة
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. تهيئة مخزن البيانات والوضع الليلي
# ==========================================
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'

# ==========================================
# 3. تفعيل الألوان بناءً على حالة الزرار
# ==========================================
if st.session_state.dark_mode:
    bg_color = "#121212"
    card_color = "#1e1e1e"
    text_color = "#ffffff"
    accent_color = "#f1c40f"
else:
    bg_color = "#f4f4f4"
    card_color = "#ffffff"
    text_color = "#121212"
    accent_color = "#d4ac0d"

# تطبيق الاستايل (CSS)
st.markdown(f"""
    <style>
    /* إخفاء الأدوات الافتراضية */
    header {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    
    /* ضبط الخلفية والاتجاه */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        direction: rtl;
    }}
    
    /* كروت الوحدات - مفرودة بالعرض */
    .unit-card {{
        background-color: {card_color};
        padding: 20px;
        border-radius: 15px;
        border-right: 10px solid {accent_color};
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }}

    /* العناوين الكبيرة */
    .main-title {{
        text-align: center;
        color: {accent_color};
        font-size: 3em;
        font-weight: 900;
        margin-bottom: 30px;
    }}
    
    /* الجداول */
    .stTable {{
        width: 100% !important;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. القائمة الجانبية (Sidebar) - تفعيل الزرار
# ==========================================
with st.sidebar:
    st.markdown(f"<h2 style='text-align:center; color:{accent_color};'>DOGGA 2026</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>المهندس ياسين علاء</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # زرار الدرك مود (شغال الآن)
    label = "🌙 تفعيل الوضع الليلي" if not st.session_state.dark_mode else "☀️ تفعيل الوضع النهاري"
    if st.button(label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun() # لإعادة تحميل الصفحة بالألوان الجديدة
        
    if st.button("🏠 العودة للرئيسية", use_container_width=True):
        st.session_state.page = 'welcome'
        st.rerun()

    # مخزن الخامات التراكمي
    if st.session_state.project_list:
        st.markdown("---")
        st.markdown("### 📦 إجمالي المشروع")
        total_alum = sum([x['m_m'] for x in st.session_state.project_list]) / 600
        total_fiber = sum([x['f_a'] for x in st.session_state.project_list]) / (280*122)
        st.metric("أعواد ألومنيوم", f"{round(total_alum, 1)}")
        st.metric("ألواح فيبر", f"{round(total_fiber, 1)}")
        if st.button("🗑️ تفريغ المشروع", use_container_width=True):
            st.session_state.project_list = []
            st.rerun()

# ==========================================
# 5. محتوى الصفحات
# ==========================================

if st.session_state.page == 'welcome':
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">DOGGA SYSTEM</h1>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="text-align:center; color:white;">برمجية التخصيم الفني - م/ ياسين علاء</h3>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("🚀 ابدأ العمل الآن", use_container_width=True):
            st.session_state.page = 'app'
            st.rerun()

elif st.session_state.page == 'app':
    st.markdown(f"<h2 style='color:{accent_color};'>📋 إضافة وحدة جديدة</h2>", unsafe_allow_html=True)
    
    # مدخلات المقاسات - موزعة بالعرض
    with st.container():
        # تقسيم المدخلات لـ 3 أعمدة بالعرض عشان ميبقاش الكلام بالطول
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📏 المقاسات الأساسية")
            name = st.text_input("اسم الوحدة")
            u_type = st.selectbox("نوع التخصيم", ["سفلية (13سم)", "علوية (5سم)", "دولاب (13سم)"])
            w = st.number_input("العرض (سم)", value=None, placeholder="اكتب العرض")
            h = st.number_input("الارتفاع (سم)", value=None, placeholder="اكتب الارتفاع")
            d = st.number_input("العمق (سم)", value=None, placeholder="اكتب العمق")
            
        with col2:
            st.subheader("🧱 الرفوف والفواصل")
            sh_w = st.number_input("عرض الرف", value=None, placeholder="0.0")
            sh_d = st.number_input("عمق الرف", value=None, placeholder="0.0")
            sh_n = st.number_input("عدد الرفوف", value=None, placeholder="0")
            st.markdown("---")
            dv_h = st.number_input("ارتفاع الفاصل", value=None, placeholder="0.0")
            dv_d = st.number_input("عمق الفاصل", value=None, placeholder="0.0")
            dv_n = st.number_input("عدد الفواصل", value=None, placeholder="0")
            
        with col3:
            st.subheader("🗄️ الأدراج")
            dr_w = st.number_input("عرض الدرج", value=None, placeholder="0.0")
            dr_d = st.number_input("عمق الدرج", value=None, placeholder="0.0")
            dr_n = st.number_input("عدد الأدراج", value=None, placeholder="0")
            st.markdown("---")
            if st.button("✅ حفظ وتخصيم الوحدة", use_container_width=True):
                if w and h:
                    ded = 13 if "13" in u_type else 5
                    h_n, w_n, d_n = int(h - ded), int(w - 5), int((d or 0) - 5)
                    
                    # جداول الألومنيوم والفيبر
                    alum = [
                        {"البيان": "قوايم رئيسية", "المقاس": h_n, "العدد": "4"},
                        {"البيان": "عوارض عرض", "المقاس": w_n, "العدد": "4"},
                        {"البيان": "عوارض عمق", "المقاس": d_n, "العدد": "4"}
                    ]
                    if dv_n: alum.append({"البيان": "فواصل", "المقاس": f"{int(dv_h)}x{int(dv_d)}", "العدد": f"{int(dv_n)*4}"})
                    
                    st.session_state.project_list.append({
                        "name": name, "dims": f"{w}x{h}x{d}",
                        "alum": pd.DataFrame(alum),
                        "m_m": (h_n*4 + w_n*4 + d_n*4) + (int(dv_h or 0)*4*int(dv_n or 0)),
                        "m_t": (h_n*2 + w_n*2),
                        "f_a": (w_n*h_n) + (h_n*d_n*2)
                    })
                    st.rerun()

    # عرض النتائج في كروت عريضة
    st.markdown("---")
    for i, item in enumerate(st.session_state.project_list):
        with st.container():
            st.markdown(f"""
            <div class="unit-card">
                <h3>#{i+1} {item['name']} - مقاس {item['dims']}</h3>
            </div>
            """, unsafe_allow_html=True)
            res_col1, res_col2 = st.columns([2, 1])
            with res_col1:
                st.write("**⚒️ تخصيم الألومنيوم:**")
                st.table(item['alum'])
            with res_col2:
                st.write("**🪵 مساحات الفيبر:**")
                st.info(f"المساحة المحسوبة: {item['f_a']} سم مربع")

# تذييل الصفحة
st.markdown(f"<p style='text-align:center; color:{accent_color};'>DOGGA SYSTEM 2026 | م/ ياسين علاء</p>", unsafe_allow_html=True)
