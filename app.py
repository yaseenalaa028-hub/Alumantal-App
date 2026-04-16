import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات المنظومة (Eng. Yassin Alaa)
# ==========================================
st.set_page_config(
    page_title="DOGGA SYSTEM | م/ ياسين علاء",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. ذاكرة النظام (لضمان عدم فقدان أي بيان)
# ==========================================
if 'project_list' not in st.session_state:
    st.session_state.project_list = []
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# ==========================================
# 3. التصميم (CSS) - اللوجو الصغير والأناقة
# ==========================================
st.markdown("""
    <style>
    .stApp { direction: rtl !important; text-align: right; background-color: #0e1117; color: white; }
    .mini-logo {
        border: 2px solid #f1c40f;
        padding: 5px 15px;
        border-radius: 8px;
        display: inline-block;
        font-weight: bold;
        color: #f1c40f;
        margin-bottom: 20px;
    }
    .main-card {
        background: #1c1f26;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #f1c40f;
        text-align: center;
        margin-bottom: 20px;
    }
    .unit-box {
        background: #262730;
        border-right: 8px solid #f1c40f;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .stTable { background-color: #1c1f26; border-radius: 10px; }
    header, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# اللوجو الثابت في كل الصفحات
st.markdown('<div class="mini-logo">DOGGA SYSTEM | م/ ياسين علاء</div>', unsafe_allow_html=True)

# ==========================================
# 4. التنقل بين الصفحات
# ==========================================

# --- الصفحة الأولى: اللوحة الرئيسية (Dashboard) ---
if st.session_state.page == 'dashboard':
    st.markdown('<div class="main-card"><h1>📊 لوحة تحكم المشروعات</h1><p>المهندس ياسين علاء - إصدار 2026</p></div>', unsafe_allow_html=True)
    
    # إحصائيات سريعة
    c1, c2, c3 = st.columns(3)
    total_units = len(st.session_state.project_list)
    total_cm = sum([x['raw_m'] for x in st.session_state.project_list])
    total_rods = total_cm / 600
    
    with c1: st.metric("عدد الوحدات", total_units)
    with c2: st.metric("إجمالي الألومنيوم (عود)", round(total_rods, 1))
    with c3: st.metric("حالة المشروع", "نشط" if total_units > 0 else "فارغ")

    st.divider()
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("➕ إضافة مقاسات جديدة", use_container_width=True):
            st.session_state.page = 'input'
            st.rerun()
    with col_btn2:
        if st.button("📄 عرض الشيتات التفصيلية", use_container_width=True):
            st.session_state.page = 'report'
            st.rerun()

    # القائمة الخارجية المختصرة
    if total_units > 0:
        st.subheader("📋 قائمة الوحدات الحالية")
        summary_df = pd.DataFrame([
            {"العميل/الوحدة": x['client'], "النوع": x['type'], "المقاسات": x['dims']} 
            for x in st.session_state.project_list
        ])
        st.table(summary_df)

# --- الصفحة الثانية: إدخال البيانات والتخصيم ---
elif st.session_state.page == 'input':
    if st.button("⬅️ عودة للرئيسية"):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown("### 📝 إدخال بيانات التخصيم الفني")
    
    with st.form("input_form"):
        # الترتيب: العميل -> النوع -> المقاسات
        row1_col1, row1_col2 = st.columns(2)
        with row1_col1: u_client = st.text_input("اسم العميل / كود الوحدة")
        with row1_col2: u_type = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية / أخرى", "دولاب خزين"])
        
        row2_col1, row2_col2, row2_col3 = st.columns(3)
        with row2_col1: w_in = st.number_input("العرض الكلي (سم)", value=0.0)
        with row2_col2: h_in = st.number_input("الارتفاع الكلي (سم)", value=0.0)
        with row2_col3: d_in = st.number_input("العمق الكلي (سم)", value=0.0)
        
        st.write("---")
        # الإضافات الفنية
        row3_col1, row3_col2, row3_col3 = st.columns(3)
        with row3_col1:
            st.write("**الأرفف**")
            sh_n = st.number_input("العدد", value=0)
            sh_w = st.number_input("عرض الرف", value=0.0)
            sh_d = st.number_input("عمق الرف", value=0.0)
        with row3_col2:
            st.write("**الفواصل**")
            v_n = st.number_input("عدد الفواصل", value=0)
            v_h = st.number_input("ارتفاع الفاصل", value=0.0)
            v_d = st.number_input("عمق الفاصل", value=0.0)
        with row3_col3:
            st.write("**الأدراج**")
            dr_n = st.number_input("عدد الأدراج", value=0)
            dr_w = st.number_input("عرض برواز الدرج", value=0.0)
            dr_d = st.number_input("عمق الدرج", value=0.0)
            
        submitted = st.form_submit_state = st.form_submit_button("✅ تنفيذ التخصيم وحفظ البيانات", use_container_width=True)
        
        if submitted:
            if w_in > 0 and h_in > 0:
                # منطق التخصيم (المهندس ياسين علاء)
                h_ded = 13 if (u_type == "وحدة سفلية" or u_type == "دولاب خزين") else 5
                h_net, w_net, d_net = int(h_in - h_ded), int(w_in - 5), int(d_in - 5)

                # 1. الألومنيوم
                if u_type == "وحدة سفلية":
                    alum = [["قوايم ارتفاع", h_net, 2, 2], ["عوارض عرض", w_net, 3, 1], ["عوارض عمق", d_net, 2, 2]]
                else:
                    alum = [["قوايم ارتفاع", h_net, 2, 2], ["عوارض عرض", w_net, 2, 2], ["عوارض عمق", d_net, 0, 4]]
                
                if sh_n > 0: alum.append([f"أعواد رف ({sh_n})", f"عرض {int(sh_w)} / عمق {int(sh_d)}", sh_n*4, 0])
                if v_n > 0: alum.append([f"أعواد فاصل ({v_n})", int(v_h), v_n*4, 0])
                if dr_n > 0: alum.append([f"براويز درج ({dr_n})", f"عرض {dr_w-2.5} / عمق {dr_d}", dr_n*4, 0])

                # 2. الفيبر
                fiber = [
                    ["الظهرية", f"{w_net}x{h_net}", 1],
                    ["الأرضية", f"{w_net}x{d_net}", 1],
                    ["الأجناب", f"{h_net}x{d_net}", 2]
                ]
                if sh_n > 0: fiber.append(["فيبر أرفف", f"{int(sh_w-5)}x{int(sh_d-5)}", sh_n])
                if v_n > 0: fiber.append(["فيبر فواصل", f"{int(v_h-5)}x{int(v_d-5)}", v_n])

                st.session_state.project_list.append({
                    "client": u_client, "type": u_type, "dims": f"{w_in}x{h_in}x{d_in}",
                    "alum_df": pd.DataFrame(alum, columns=["البيان", "المقاس", "مفرد", "متقارب"]),
                    "fiber_df": pd.DataFrame(fiber, columns=["القطعة", "المقاس", "العدد"]),
                    "raw_m": (h_net*4 + w_net*4 + d_net*4)
                })
                st.success("تم الحفظ بنجاح!")
                st.session_state.page = 'dashboard'
                st.rerun()

# --- الصفحة الثالثة: التقارير التفصيلية ---
elif st.session_state.page == 'report':
    if st.button("⬅️ عودة للرئيسية"):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown("### 📄 شيتات التفصيل والفيبر الكاملة")
    
    if not st.session_state.project_list:
        st.warning("لا توجد بيانات لعرضها.")
    else:
        for i, item in enumerate(st.session_state.project_list):
            with st.container():
                st.markdown(f'<div class="unit-box"><b>وحدة #{i+1}: {item["client"]} | {item["type"]} | {item["dims"]}</b></div>', unsafe_allow_html=True)
                col_a, col_f = st.columns([3, 2])
                with col_a:
                    st.write("**📐 الألومنيوم (مفرد/متقارب)**")
                    st.table(item['alum_df'])
                with col_f:
                    st.write("**✨ الفيبر**")
                    st.table(item['fiber_df'])
        
        st.divider()
        if st.button("🗑️ مسح المشروع بالكامل"):
            st.session_state.project_list = []
            st.session_state.page = 'dashboard'
            st.rerun()

st.markdown("<p style='text-align:center; font-size:0.8em; margin-top:50px;'>DOGGA SYSTEM 2026 | تطوير المهندس ياسين علاء</p>", unsafe_allow_html=True)
