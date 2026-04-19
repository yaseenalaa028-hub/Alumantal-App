import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة الفضائية
st.set_page_config(page_title="DOGGA SYSTEM - ULTIMATE", layout="wide")

# --- محرك التصميم (CSS الشامل لضمان الشكل المتناسق والسرعة) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    /* الأزرار الرئيسية الثلاثة */
    .main-btn-container div.stButton > button {
        background: rgba(0, 242, 254, 0.05);
        border: 2px solid #00f2fe;
        color: #00f2fe;
        border-radius: 20px;
        padding: 50px 20px;
        font-size: 26px;
        font-weight: bold;
        transition: 0.4s ease;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
        width: 100%;
    }
    .main-btn-container div.stButton > button:hover {
        background: #00f2fe;
        color: #000;
        box-shadow: 0 0 40px #00f2fe;
        transform: scale(1.05);
    }
    /* تنسيق الكروت والجداول */
    div[data-testid="stForm"], .stTable, .stDataFrame, div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        backdrop-filter: blur(15px);
    }
    h1, h2, h3 { color: #00f2fe !important; text-align: center; text-shadow: 0 0 10px #00f2fe; }
    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background-color: rgba(0, 0, 0, 0.4) !important;
        color: #00f2fe !important;
        border: 1px solid #302b63 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة حالة التطبيق (Session State)
if 'project_data' not in st.session_state:
    st.session_state.project_data = [] 
if 'page' not in st.session_state:
    st.session_state.page = 'main_menu'

# وظيفة إضافة البيانات للمشروع (المحرك الأساسي)
def add_to_project(unit_name, category, item_name, length, qty, unit_type="-"):
    st.session_state.project_data.append({
        "اسم الوحدة": unit_name,
        "الخامة": category,
        "اسم القطعة": item_name,
        "المقاس (سم)": length,
        "العدد": qty,
        "نوع التخصيم": unit_type
    })

# ==========================================
# 🌌 الصفحة الأولى: القائمة الرئيسية (واجهة من كوكب آخر)
# ==========================================
if st.session_state.page == 'main_menu':
    st.markdown("<h1>🚀 DOGGA SMART KITCHEN SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>بواسطة المهندس ياسين علاء | مصنع DED EL KASR</p>", unsafe_allow_html=True)
    st.write("##")
    
    st.markdown('<div class="main-btn-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✨ ابدأ التخصيم"):
            st.session_state.page = 'deduction'
            st.rerun()
    with c2:
        if st.button("🥁 تخصيم الدرف"):
            st.toast("خوارزمية الدف قيد المعالجة...")
    with c3:
        if st.button("📁 المشاريع"):
            st.session_state.page = 'inventory'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🏗️ الصفحة الثانية: التخصيم التفصيلي (المنطق الكامل)
# ==========================================
elif st.session_state.page == 'deduction':
    st.markdown("### 🏗️ تخصيم مشروع متكامل - ورشة DED EL KASR")
    if st.button("🏠 العودة للقائمة الرئيسية"):
        st.session_state.page = 'main_menu'
        st.rerun()

    with st.form("complete_logic_form", clear_on_submit=True):
        st.subheader("📏 إدخال بيانات الوحدة الأساسية")
        c_name, c_kind = st.columns(2)
        u_label = c_name.text_input("اسم الوحدة (مثلاً: سفلي 80 سم)", placeholder="وحدة 1")
        u_kind = c_kind.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])

        c1, c2, c3 = st.columns(3)
        W = c1.number_input("العرض الكلي (W)", min_value=0.0)
        H = c2.number_input("ارتفاع القطعة الكلي (H)", min_value=0.0)
        D = c3.number_input("عمق القطعة الكلي (D)", min_value=0.0)

        st.divider()
        st.subheader("📦 الأرفف والفواصل والأدراج")
        
        # أرفف
        cs1, cs2, cs3 = st.columns(3)
        s_w = cs1.number_input("عرض الرف الصافي", value=0.0)
        s_d = cs2.number_input("عمق الرف الصافي", value=0.0)
        s_q = cs3.number_input("عدد الأرفف", min_value=0, step=1)

        # فواصل
        cv1, cv2, cv3 = st.columns(3)
        v_h = cv1.number_input("ارتفاع الفاصل الصافي", value=0.0)
        v_d = cv2.number_input("عمق الفاصل الصافي", value=0.0)
        v_q = cv3.number_input("عدد الفواصل", min_value=0, step=1)

        # أدراج
        cd1, cd2, cd3 = st.columns(3)
        dr_w = cd1.number_input("عرض الدرج", value=0.0)
        dr_d = cd2.number_input("عمق الدرج ثابت", value=0.0)
        dr_q = cd3.number_input("عدد الأدراج", min_value=0, step=1)

        submit = st.form_submit_button("🚀 إضافة الوحدة للمشروع")

    if submit and W > 0 and H > 0:
        name = u_label if u_label else f"وحدة {u_kind}"
        
        # --- [ أ ] منطق التخصيم الهندسي (الكامل) ---
        h_ded = 13 if u_kind in ["سفلي", "دولاب خزين"] else 5
        f_h, f_w, f_d = H - h_ded, W - 5, D - 5

        # ألومنيوم الهيكل
        if u_kind == "سفلي":
            add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
            add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
            add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 3, "مفرد")
            add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 1, "متقارب")
            add_to_project(name, "ألومنيوم", "رباط عمق", f_d, 2, "مفرد")
            add_to_project(name, "ألومنيوم", "رباط عمق", f_d, 2, "متقارب")
        else:
            add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
            add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
            add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 2, "مفرد")
            add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 2, "متقارب")
            add_to_project(name, "ألومنيوم", "رباط عمق", f_d, 4, "متقارب")

        # فيبر الهيكل
        add_to_project(name, "فيبر", "ضهرية الوحدة", f"{f_w}×{f_h}", 1, "حشو")
        add_to_project(name, "فيبر", "أرضية الوحدة", f"{f_w}×{f_d}", 1, "حشو")
        add_to_project(name, "فيبر", "أجناب الوحدة", f"{f_h}×{f_d}", 2, "حشو")

        # حسابات الأرفف
        if s_q > 0:
            add_to_project(name, "ألومنيوم", "عرض الرف", s_w, s_q*2, "مفرد")
            add_to_project(name, "ألومنيوم", "عمق الرف", s_d, s_q*2, "مفرد")
            add_to_project(name, "فيبر", "حشو رف", f"{s_w-5}×{s_d-5}", s_q, "خصم 5 سم")

        # حسابات الفواصل
        if v_q > 0:
            add_to_project(name, "ألومنيوم", "ارتفاع فاصل", v_h, v_q*2, "مفرد")
            add_to_project(name, "ألومنيوم", "عمق فاصل", v_d, v_q*2, "مفرد")
            add_to_project(name, "فيبر", "حشو فاصل", f"{v_h-5}×{v_d-5}", v_q, "خصم 5 سم")

        # حسابات الأدراج
        if dr_q > 0:
            add_to_project(name, "ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q*2, "علبة درج")
            add_to_project(name, "ألومنيوم", "جنب درج", dr_d, dr_q*2, "علبة درج")
            add_to_project(name, "فيبر", "أرضية درج", f"{dr_w-7.5}×{dr_d-5}", dr_q, "حشو")

        st.balloons()
        st.success(f"تمت إضافة {name} بنجاح!")

    # عرض البيانات الحالية
    if st.session_state.project_data:
        st.divider()
        df = pd.DataFrame(st.session_state.project_data)
        for n, g in df.groupby("اسم الوحدة"):
            with st.expander(f"📍 مراجعة تخصيم {n}"):
                st.table(g.drop(columns=["اسم الوحدة"]))
        
        if st.button("💰 حساب استهلاك الخامات والتسعير ⬅️", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()

# ==========================================
# 📊 الصفحة الثالثة: الاستهلاك والفاتورة
# ==========================================
elif st.session_state.page == 'inventory':
    st.markdown("## 📊 استهلاك خامات المشروع - DOGGA SYSTEM")
    if st.button("🏠 العودة للقائمة"):
        st.session_state.page = 'main_menu'; st.rerun()

    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        
        # 1. حساب أعواد الألومنيوم (6 متر)
        alum = df[df["الخامة"] == "ألومنيوم"].copy()
        alum["المقاس (سم)"] = pd.to_numeric(alum["المقاس (سم)"], errors='coerce')
        summary = alum.groupby("نوع التخصيم").apply(lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()).reset_index(name="إجمالي سم")
        summary["الأعواد"] = summary["إجمالي سم"].apply(lambda x: math.ceil(x / 600))
        
        st.subheader("🥢 تقدير أعواد الألومنيوم")
        st.table(summary)

        # 2. حساب ألواح الفيبر
        total_area = 0
        for _, row in df[df["الخامة"] == "فيبر"].iterrows():
            dims = str(row["المقاس (سم)"]).split('×')
            if len(dims) == 2:
                try:
                    total_area += float(dims[0]) * float(dims[1]) * row["العدد"]
                except: continue
        sheets = math.ceil(total_area / (280 * 130))
        st.metric("عدد ألواح الفيبر المطلوبة (280x130)", f"{sheets} لوح")

        st.divider()
        st.subheader("💵 فاتورة المشتريات المفتوحة")
        
        base_bill = [{"الصنف": f"ألومنيوم {r['نوع التخصيم']}", "الكمية": r["الأعواد"], "السعر": 0.0} for _, r in summary.iterrows()]
        base_bill.append({"الصنف": "لوح فيبر كامل", "الكمية": sheets, "السعر": 0.0})
        
        final_bill = st.data_editor(pd.DataFrame(base_bill), num_rows="dynamic", use_container_width=True)
        total = (final_bill["الكمية"] * final_bill["السعر"]).sum()
        st.markdown(f"<h2 style='color:#00f2fe'>💰 التكلفة الإجمالية: {total:,.2f} ج.م</h2>", unsafe_allow_html=True)

        # خيارات التحكم
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⬅️ إضافة وحدات أخرى"):
                st.session_state.page = 'deduction'; st.rerun()
        with c2:
            csv = final_bill.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل الفاتورة (Excel)", data=csv, file_name="DOGGA_Invoice.csv")
        with c3:
            if st.button("🗑️ مسح المشروع بالكامل"):
                st.session_state.project_data = []; st.session_state.page = 'main_menu'; st.rerun()
    else:
        st.error("⚠️ لا توجد بيانات.")
