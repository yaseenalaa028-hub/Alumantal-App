import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة والتنسيق الفضائي (النحاسي + الأزرق الكهربائي)
st.set_page_config(page_title="DOGGA GALAXY SYSTEM", layout="wide")

st.markdown("""
    <style>
    /* الخلفية الكونية */
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

    /* تحسين شكل المدخلات (مرتبة رأسيًا) */
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

# 2. تهيئة مخزن البيانات ومنطق التنقل
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
# 🌌 الصفحة 1: الواجهة الرئيسية (3 زراير كبيرة)
# ==========================================
if st.session_state.page == 'main_menu':
    st.markdown("<h1>⚡ DOGGA GALAXY SYSTEM</h1>")
    st.markdown("<p style='text-align: center; color: #d9a066; font-size: 1.3rem;'>المهندس ياسين علاء | مصنع DED EL KASR</p>", unsafe_allow_html=True)
    st.write("##")
    
    st.markdown('<div class="main-btn-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("✨ ابدأ التخصيم"):
            st.session_state.page = 'deduction'
            st.rerun()
        
        if st.button("📏 تخصيم الدرف"):
            st.toast("🚀 جاري تجهيز معادلات الدف...")
            
        if st.button("📁 المشاريع"):
            st.session_state.page = 'inventory'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🏗️ الصفحة 2: التخصيم التفصيلي (الطلبات تحت بعضها)
# ==========================================
elif st.session_state.page == 'deduction':
    st.markdown("<h3>🏗️ تخصيم وحدة جديدة</h3>")
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'main_menu'
        st.rerun()

    with st.form("main_form", clear_on_submit=True):
        st.markdown("### 🏷️ بيانات الوحدة")
        u_label = st.text_input("اسم الوحدة (مثلاً: سفلي 80 سم)")
        u_kind = st.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])

        st.divider()
        st.markdown("### 📏 أبعاد الهيكل (W-H-D)")
        W = st.number_input("العرض الكلي (W)")
        H = st.number_input("الارتفاع الكلي (H)")
        D = st.number_input("العمق الكلي (D)")

        st.divider()
        st.markdown("### 📦 الأرفف والفواصل")
        s_w = st.number_input("عرض الرف الصافي")
        s_d = st.number_input("عمق الرف الصافي")
        s_q = st.number_input("عدد الأرفف", min_value=0)
        
        st.write("---")
        v_h = st.number_input("ارتفاع الفاصل الصافي")
        v_d = st.number_input("عمق الفاصل الصافي")
        v_q = st.number_input("عدد الفواصل", min_value=0)

        st.divider()
        st.markdown("### 🗄️ الأدراج")
        dr_w = st.number_input("عرض الدرج")
        dr_d = st.number_input("عمق الدرج")
        dr_q = st.number_input("عدد الأدراج", min_value=0)

        st.write("##")
        submit = st.form_submit_button("✅ إضافة الوحدة للمشروع", use_container_width=True)

    if submit and W > 0 and H > 0:
        name = u_label if u_label else f"وحدة {u_kind}"
        h_ded = 13 if u_kind in ["سفلي", "دولاب خزين"] else 5
        f_h, f_w, f_d = H - h_ded, W - 5, D - 5

        # منطق ألومنيوم الهيكل
        if u_kind == "سفلي":
            items = [("قائم ارتفاع", f_h, 2, "مفرد"), ("قائم ارتفاع", f_h, 2, "متقارب"),
                     ("عارضة عرض", f_w, 3, "مفرد"), ("عارضة عرض", f_w, 1, "متقارب"),
                     ("رباط عمق", f_d, 2, "مفرد"), ("رباط عمق", f_d, 2, "متقارب")]
        else:
            items = [("قائم ارتفاع", f_h, 2, "مفرد"), ("قائم ارتفاع", f_h, 2, "متقارب"),
                     ("عارضة عرض", f_w, 2, "مفرد"), ("عارضة عرض", f_w, 2, "متقارب"),
                     ("رباط عمق", f_d, 4, "متقارب")]
        for i in items: add_to_project(name, "ألومنيوم", i[0], i[1], i[2], i[3])

        # فيبر الهيكل
        add_to_project(name, "فيبر", "ضهرية", f"{f_w}×{f_h}", 1, "لوح")
        add_to_project(name, "فيبر", "أرضية", f"{f_w}×{f_d}", 1, "لوح")
        add_to_project(name, "فيبر", "أجناب", f"{f_h}×{f_d}", 2, "لوح")

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
        if st.button("💰 حساب الخامات النهائية والفاتورة ⬅️", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()

# ==========================================
# 📊 الصفحة 3: الاستهلاك والفاتورة
# ==========================================
elif st.session_state.page == 'inventory':
    st.markdown("<h2>📊 استهلاك خامات المشروع</h2>")
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'main_menu'
        st.rerun()
    
    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        
        # عرض تفاصيل المشروع
        with st.expander("🔍 مراجعة قطع الوحدات المضافة"):
            for n, g in df.groupby("اسم الوحدة"):
                st.write(f"**📍 {n}**")
                st.table(g.drop(columns=["اسم الوحدة"]))

        # حساب الأعواد
        alum = df[df["الخامة"] == "ألومنيوم"].copy()
        alum["المقاس (سم)"] = pd.to_numeric(alum["المقاس (سم)"], errors='coerce')
        summary = alum.groupby("نوع التخصيم").apply(lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()).reset_index(name="إجمالي سم")
        summary["الأعواد"] = summary["إجمالي سم"].apply(lambda x: math.ceil(x / 600))
        
        st.subheader("🥢 تقدير أعواد الألومنيوم")
        st.table(summary)

        # حساب الفيبر
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
        total_cost = (final_bill["الكمية"] * final_bill["السعر"]).sum()
        st.markdown(f"<h2>💰 التكلفة الإجمالية: {total_cost:,.2f} ج.م</h2>", unsafe_allow_html=True)
        
        # أزرار الإجراءات النهائية
        c_inv1, c_inv2 = st.columns(2)
        with c_inv1:
            csv_final = final_bill.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل الفاتورة", data=csv_final, file_name="DOGGA_Invoice.csv", use_container_width=True)
        with c_inv2:
            if st.button("🗑️ مسح المشروع بالكامل", type="secondary", use_container_width=True):
                st.session_state.project_data = []
                st.session_state.page = 'main_menu'
                st.rerun()
