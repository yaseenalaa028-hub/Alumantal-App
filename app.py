import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة والواجهة الفضائية (نحاسي + أزرق كهربائي)
st.set_page_config(page_title="DOGGA SYSTEM - الإدارة الهندسية", layout="wide")

st.markdown("""
    <style>
    /* الخلفية والكون */
    .stApp {
        background: radial-gradient(circle at top right, #0d1117, #050505, #020c1b);
        color: #d9a066;
    }
    
    /* تصميم الأزرار الرئيسية الثلاثة */
    .main-btn-container div.stButton > button {
        background: rgba(0, 150, 255, 0.05) !important;
        border: 2px solid #0096ff !important;
        color: #0096ff !important;
        border-radius: 20px !important;
        padding: 50px 20px !important;
        font-size: 26px !important;
        font-weight: bold !important;
        width: 100% !important;
        transition: 0.5s !important;
        text-shadow: 0 0 15px #0096ff !important;
        box-shadow: 0 0 10px rgba(0, 150, 255, 0.2) !important;
        margin-bottom: 25px !important;
    }
    .main-btn-container div.stButton > button:hover {
        background: #d9a066 !important;
        color: #1a1614 !important;
        border-color: #d9a066 !important;
        box-shadow: 0 0 40px #d9a066 !important;
        transform: scale(1.02) !important;
    }

    /* تنسيق الحاويات والجداول */
    div[data-testid="stForm"], .stTable, .stDataFrame, div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(217, 160, 102, 0.4) !important;
        backdrop-filter: blur(5px);
    }

    /* العناوين والخطوط */
    h1 { 
        color: #0096ff !important; 
        text-shadow: 0 0 30px #0096ff; 
        text-align: center;
        font-size: 3.5rem !important;
    }
    h2, h3 { color: #d9a066 !important; text-align: center; }

    /* تحسين شكل المدخلات */
    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background-color: #0d1117 !important;
        color: #0096ff !important;
        border: 1px solid #0096ff !important;
        border-radius: 10px !important;
        height: 50px !important;
    }
    label { 
        color: #d9a066 !important; 
        font-weight: bold !important; 
        font-size: 1.1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. تهيئة مخزن البيانات
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
# 🌌 الصفحة 0: الواجهة الرئيسية
# ==========================================
if st.session_state.page == 'main_menu':
    st.markdown("<h1>⚡ DOGGA GALAXY SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d9a066; font-size: 1.3rem;'>برمجة المهندس ياسين علاء | ضد الكسر </p>", unsafe_allow_html=True)
    st.write("##")
    
    st.markdown('<div class="main-btn-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("✨ ابدأ التخصيم"):
            st.session_state.page = 'deduction'
            st.rerun()
        
        if st.button("📏 تخصيم الدرف"):
            st.toast("🛸 جاري تجهيز محرك الدرف...")
            
        if st.button("📁 المشاريع المحفوظة"):
            st.session_state.page = 'inventory'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# الصفحة الأولى: التخصيم التفصيلي
# ==========================================
elif st.session_state.page == 'deduction':
    st.markdown("<h1>🏗️ تخصيم مشروع متكامل</h1>", unsafe_allow_html=True)
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'main_menu'
        st.rerun()
    
    with st.form("main_form", clear_on_submit=True):
        st.subheader("📏 إدخال بيانات الوحدة")
        u_label = st.text_input("اسم الوحدة (مثلاً: سفلي 80 سم)", placeholder="وحدة 1")
        u_kind = st.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])

        st.divider()
        W = st.number_input("العرض الكلي (W)", min_value=0.0, step=0.1)
        H = st.number_input("الارتفاع الكلي (H)", min_value=0.0, step=0.1)
        D = st.number_input("العمق الكلي (D)", min_value=0.0, step=0.1)

        st.divider()
        st.subheader("📦 الأرفف والفواصل والأدراج")
        
        col_s = st.columns(3)
        s_w = col_s[0].number_input("عرض الرف", value=0.0)
        s_d = col_s[1].number_input("عمق الرف", value=0.0)
        s_q = col_s[2].number_input("عدد الأرفف", min_value=0)

        st.write("---")
        col_v = st.columns(3)
        v_h = col_v[0].number_input("ارتفاع الفاصل", value=0.0)
        v_d = col_v[1].number_input("عمق الفاصل", value=0.0)
        v_q = col_v[2].number_input("عدد الفواصل", min_value=0)

        st.write("---")
        col_dr = st.columns(3)
        dr_w = col_dr[0].number_input("عرض الدرج", value=0.0)
        dr_d = col_dr[1].number_input("عمق الدرج", value=0.0)
        dr_q = col_dr[2].number_input("عدد الأدراج", min_value=0)

        submit = st.form_submit_button("✅ حفظ الوحدة في المشروع", use_container_width=True)

    if submit:
        if W > 0 and H > 0:
            name = u_label if u_label else f"وحدة {u_kind}"
            # قاعدة الـ 13 سم للسفلي والـ 5 سم للعلوي
            h_ded = 13.0 if u_kind in ["سفلي", "دولاب خزين"] else 5.0
            f_h, f_w, f_d = H - h_ded, W - 5.0, D - 5.0

            # --- ألومنيوم الهيكل ---
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

            # --- فيبر الهيكل ---
            add_to_project(name, "فيبر", "ضهرية", f"{f_w}×{f_h}", 1, "لوح")
            add_to_project(name, "فيبر", "أرضية", f"{f_w}×{f_d}", 1, "لوح")
            if u_kind != "سفلي":
                add_to_project(name, "فيبر", "سقفية", f"{f_w}×{f_d}", 1, "لوح")
            add_to_project(name, "فيبر", "أجناب", f"{f_h}×{f_d}", 2, "لوح")

            # --- حسابات الإضافات ---
            if s_q > 0:
                add_to_project(name, "ألومنيوم", "عرض رف", s_w, s_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "عمق رف", s_d, s_q*2, "مفرد")
                add_to_project(name, "فيبر", "حشو رف", f"{s_w-5}×{s_d-5}", s_q, "لوح")

            if v_q > 0:
                add_to_project(name, "ألومنيوم", "ارتفاع فاصل", v_h, v_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "عمق فاصل", v_d, v_q*2, "مفرد")
                add_to_project(name, "فيبر", "حشو فاصل", f"{v_h-5}×{v_d-5}", v_q, "لوح")

            if dr_q > 0:
                add_to_project(name, "ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q*2, "علبه درج")
                add_to_project(name, "ألومنيوم", "جنب درج", dr_d, dr_q*2, "علبه درج")
                add_to_project(name, "فيبر", "أرضية درج", f"{dr_w-7.5}×{dr_d-5}", dr_q, "لوح")

            st.success(f"تمت إضافة {name} للمشروع")

    if st.session_state.project_data:
        st.divider()
        df = pd.DataFrame(st.session_state.project_data)
        for n, g in df.groupby("اسم الوحدة"):
            with st.expander(f"📍 مراجعة تخصيم: {n}"):
                st.table(g.drop(columns=["اسم الوحدة"]))
        
        if st.button("💰 عرض المشاريع والجرد ⬅️", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()

# ==========================================
# الصفحة الثانية: الاستهلاك والفاتورة
# ==========================================
elif st.session_state.page == 'inventory':
    st.markdown("<h1>📊 استهلاك خامات المشروع</h1>", unsafe_allow_html=True)
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'main_menu'
        st.rerun()
    
    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        alum = df[df["الخامة"] == "ألومنيوم"].copy()
        alum["المقاس (سم)"] = pd.to_numeric(alum["المقاس (سم)"], errors='coerce')

        # 1. حساب الأعواد
        st.subheader("🥢 تقدير أعواد الألومنيوم (6 متر)")
        summary = alum.groupby("نوع التخصيم").apply(
            lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()
        ).reset_index(name="إجمالي سم")
        summary["الأعواد"] = summary["إجمالي سم"].apply(lambda x: math.ceil(x / 600))
        st.table(summary)

        # 2. حساب الفيبر
        total_area = 0
        for _, row in df[df["الخامة"] == "فيبر"].iterrows():
            dims = str(row["المقاس (سم)"]).split('×')
            if len(dims) == 2:
                total_area += float(dims[0]) * float(dims[1]) * row["العدد"]
        sheets = math.ceil(total_area / (280 * 130))
        st.metric("عدد ألواح الفيبر المطلوبة", f"{sheets} لوح")

        st.divider()
        st.subheader("💵 فاتورة المشتريات المفتوحة")
        
        base_bill = []
        for _, r in summary.iterrows():
            base_bill.append({"الصنف": f"ألومنيوم {r['نوع التخصيم']}", "الكمية": r["الأعواد"], "السعر": 0.0})
        base_bill.append({"الصنف": "لوح فيبر كامل", "الكمية": sheets, "السعر": 0.0})

        final_bill = st.data_editor(pd.DataFrame(base_bill), num_rows="dynamic", use_container_width=True)
        
        total = (final_bill["الكمية"] * final_bill["السعر"]).sum()
        st.header(f"💰 التكلفة الإجمالية: {total:,.2f} ج.م")

        # أزرار الإجراءات
        c_inv1, c_inv2, c_inv3 = st.columns(3)
        with c_inv1:
            if st.button("⬅️ إضافة وحدات أخرى", use_container_width=True):
                st.session_state.page = 'deduction'
                st.rerun()
        with c_inv2:
            csv_final = final_bill.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 تحميل الفاتورة", data=csv_final, file_name="DOGGA_Invoice.csv", use_container_width=True)
        with c_inv3:
            if st.button("🗑️ تفريغ المشروع", use_container_width=True):
                st.session_state.project_data = []
                st.session_state.page = 'main_menu'
                st.rerun()
