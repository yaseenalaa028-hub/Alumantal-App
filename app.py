import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة الفضائية
st.set_page_config(page_title="DOGGA SYSTEM - COMPLETE", layout="wide")

# --- محرك التصميم (CSS الشامل) ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        color: #ffffff;
    }
    .main-btn-container div.stButton > button {
        background: rgba(0, 242, 254, 0.05);
        border: 2px solid #00f2fe;
        color: #00f2fe;
        border-radius: 20px;
        padding: 50px 20px;
        font-size: 26px;
        font-weight: bold;
        transition: all 0.4s ease;
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
    div[data-testid="stForm"], .stTable, .stDataFrame, div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        backdrop-filter: blur(10px);
    }
    h1, h2, h3 { color: #00f2fe !important; text-align: center; }
    .stNumberInput input, .stTextInput input {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: #00f2fe !important;
        border: 1px solid #00f2fe !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة الحالة (Session State)
if 'project_data' not in st.session_state:
    st.session_state.project_data = [] 
if 'page' not in st.session_state:
    st.session_state.page = 'main_menu'

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
# 🌌 الصفحة الرئيسية
# ==========================================
if st.session_state.page == 'main_menu':
    st.markdown("<h1>🛸 DOGGA SMART KITCHEN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Engineered by: Yassin Alaa | Workshop: DED EL KASR</p>", unsafe_allow_html=True)
    st.write("##")
    
    st.markdown('<div class="main-btn-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✨ ابدأ التخصيم"):
            st.session_state.page = 'deduction'; st.rerun()
    with c2:
        if st.button("📏 تخصيم الدف"):
            st.toast("خوارزمية الدف قيد التطوير...")
    with c3:
        if st.button("📁 المشاريع"):
            st.session_state.page = 'inventory'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 📏 صفحة التخصيم (المنطق الكامل)
# ==========================================
elif st.session_state.page == 'deduction':
    st.markdown("### 🏗️ تخصيم الوحدات التفصيلي")
    if st.button("🏠 عودة"): st.session_state.page = 'main_menu'; st.rerun()

    with st.form("complete_form", clear_on_submit=True):
        col_header1, col_header2 = st.columns(2)
        u_label = col_header1.text_input("اسم الوحدة", placeholder="مثلاً: مطبخ سفلي")
        u_kind = col_header2.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])

        c1, c2, c3 = st.columns(3)
        W = c1.number_input("العرض الكلي (W)", min_value=0.0)
        H = c2.number_input("الارتفاع الكلي (H)", min_value=0.0)
        D = c3.number_input("العمق الكلي (D)", min_value=0.0)

        st.markdown("---")
        st.subheader("📦 الأرفف والفواصل والأدراج")
        cs1, cs2, cs3 = st.columns(3)
        s_w = cs1.number_input("عرض الرف الصافي", value=0.0)
        s_d = cs2.number_input("عمق الرف الصافي", value=0.0)
        s_q = cs3.number_input("عدد الأرفف", min_value=0)

        cv1, cv2, cv3 = st.columns(3)
        v_h = cv1.number_input("ارتفاع الفاصل الصافي", value=0.0)
        v_d = cv2.number_input("عمق الفاصل الصافي", value=0.0)
        v_q = cv3.number_input("عدد الفواصل", min_value=0)

        cd1, cd2, cd3 = st.columns(3)
        dr_w = cd1.number_input("عرض الدرج", value=0.0)
        dr_d = cd2.number_input("عمق الدرج ثابت", value=0.0)
        dr_q = cd3.number_input("عدد الأدراج", min_value=0)

        submit = st.form_submit_button("🚀 إضافة الوحدة ومكوناتها")

    if submit and W > 0 and H > 0:
        name = u_label if u_label else f"وحدة {u_kind}"
        h_ded = 13 if u_kind in ["سفلي", "دولاب خزين"] else 5
        f_h, f_w, f_d = H - h_ded, W - 5, D - 5

        # 1. ألومنيوم الهيكل
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

        # 2. فيبر الهيكل
        add_to_project(name, "فيبر", "ضهرية", f"{f_w}×{f_h}", 1, "لوح")
        add_to_project(name, "فيبر", "أرضية", f"{f_w}×{f_d}", 1, "لوح")
        add_to_project(name, "فيبر", "أجناب", f"{f_h}×{f_d}", 2, "لوح")

        # 3. الأرفف
        if s_q > 0:
            add_to_project(name, "ألومنيوم", "عرض رف", s_w, s_q*2, "مفرد")
            add_to_project(name, "ألومنيوم", "عمق رف", s_d, s_q*2, "مفرد")
            add_to_project(name, "فيبر", "حشو رف", f"{s_w-5}×{s_d-5}", s_q, "لوح")

        # 4. الفواصل
        if v_q > 0:
            add_to_project(name, "ألومنيوم", "ارتفاع فاصل", v_h, v_q*2, "مفرد")
            add_to_project(name, "ألومنيوم", "عمق فاصل", v_d, v_q*2, "مفرد")
            add_to_project(name, "فيبر", "حشو فاصل", f"{v_h-5}×{v_d-5}", v_q, "لوح")

        # 5. الأدراج
        if dr_q > 0:
            add_to_project(name, "ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q*2, "علبة درج")
            add_to_project(name, "ألومنيوم", "جنب درج", dr_d, dr_q*2, "علبة درج")
            add_to_project(name, "فيبر", "أرضية درج", f"{dr_w-7.5}×{dr_d-5}", dr_q, "لوح")

        st.balloons(); st.success(f"تمت إضافة {name}")

    if st.session_state.project_data:
        st.write("---")
        df = pd.DataFrame(st.session_state.project_data)
        for n, g in df.groupby("اسم الوحدة"):
            with st.expander(f"📍 مراجعة تخصيم: {n}"):
                st.table(g.drop(columns=["اسم الوحدة"]))
        
        if st.button("💰 انتقل لحساب الخامات والتسعير", use_container_width=True):
            st.session_state.page = 'inventory'; st.rerun()

# ==========================================
# 📊 صفحة الجرد والفاتورة المفتوحة
# ==========================================
elif st.session_state.page == 'inventory':
    st.markdown("## 📊 استهلاك الخامات والمشتريات")
    if st.button("🏠 عودة"): st.session_state.page = 'main_menu'; st.rerun()

    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        
        # حساب أعواد الألومنيوم
        alum = df[df["الخامة"] == "ألومنيوم"].copy()
        alum["المقاس (سم)"] = pd.to_numeric(alum["المقاس (سم)"], errors='coerce')
        summary = alum.groupby("نوع التخصيم").apply(lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()).reset_index(name="إجمالي سم")
        summary["الأعواد"] = summary["إجمالي سم"].apply(lambda x: math.ceil(x / 600))
        
        # حساب ألواح الفيبر
        total_area = 0
        for _, row in df[df["الخامة"] == "فيبر"].iterrows():
            try:
                dims = str(row["المقاس (سم)"]).split('×')
                if len(dims) == 2:
                    total_area += float(dims[0]) * float(dims[1]) * row["العدد"]
            except: continue
        sheets = math.ceil(total_area / (280 * 130))
        
        col_m1, col_m2 = st.columns(2)
        with col_m1: st.table(summary)
        with col_m2: st.metric("عدد ألواح الفيبر (280x130)", f"{sheets} لوح")

        st.write("### 💵 فاتورة المشتريات المفتوحة")
        base_bill = [{"الصنف": f"ألومنيوم {r['نوع التخصيم']}", "الكمية": r["الأعواد"], "السعر": 0.0} for _, r in summary.iterrows()]
        base_bill.append({"الصنف": "لوح فيبر كامل", "الكمية": sheets, "السعر": 0.0})
        
        final_bill = st.data_editor(pd.DataFrame(base_bill), num_rows="dynamic", use_container_width=True)
        total = (final_bill["الكمية"] * final_bill["السعر"]).sum()
        st.markdown(f"<h2 style='color:#00f2fe'>💰 التكلفة الكلية: {total:,.2f} ج.م</h2>", unsafe_allow_html=True)

        c_opt = st.columns(3)
        with c_opt[0]:
            if st.button("⬅️ إضافة وحدات"): st.session_state.page = 'deduction'; st.rerun()
        with c_opt[1]:
            st.download_button("📥 تحميل PDF/Excel", data=final_bill.to_csv().encode('utf-8-sig'), file_name="invoice.csv")
        with c_opt[2]:
            if st.button("🗑️ مسح المشروع"): st.session_state.project_data = []; st.session_state.page = 'main_menu'; st.rerun()
