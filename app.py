import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="DOGGA SMART KITCHEN - INDUSTRIAL", layout="wide")

# --- تصميم النحاس المشغول (Industrial Copper) ---
st.markdown("""
    <style>
    .stApp {
        background: #1a1614;
        color: #d9a066;
    }
    /* تصميم الأزرار الرئيسية الثلاثة */
    .main-btn-container div.stButton > button {
        background: rgba(217, 160, 102, 0.05);
        border: 2px solid #d9a066;
        color: #d9a066;
        border-radius: 10px;
        padding: 45px 20px;
        font-size: 24px;
        font-weight: bold;
        transition: 0.4s;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .main-btn-container div.stButton > button:hover {
        background: #d9a066;
        color: #1a1614;
        box-shadow: 0 0 30px rgba(217, 160, 102, 0.5);
        transform: translateY(-5px);
    }
    /* تنسيق الجداول والكروت */
    div[data-testid="stForm"], .stTable, .stDataFrame, div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(217, 160, 102, 0.3) !important;
        padding: 20px !important;
    }
    h1, h2, h3 { 
        color: #d9a066 !important; 
        text-align: center; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5); 
    }
    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background-color: #26211e !important;
        color: #d9a066 !important;
        border: 1px solid #d9a066 !important;
    }
    label { color: #d9a066 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة حالة التطبيق (Session State)
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
# 🌌 الصفحة الأولى: القائمة الرئيسية
# ==========================================
if st.session_state.page == 'main_menu':
    st.markdown("<h1>🏭 DOGGA SMART KITCHEN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #827e7c;'>برمجة المهندس ياسين علاء | مصنع DED EL KASR</p>", unsafe_allow_html=True)
    st.write("##")
    
    st.markdown('<div class="main-btn-container">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("✨ ابدأ التخصيم"): 
            st.session_state.page = 'deduction'; st.rerun()
    with c2:
        if st.button("📏 تخصيم الدرف"): 
            st.toast("خوارزمية الدف قيد المعالجة...")
    with c3:
        if st.button("📁 المشاريع"): 
            st.session_state.page = 'inventory'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🏗️ الصفحة الثانية: التخصيم (المنطق الكامل)
# ==========================================
elif st.session_state.page == 'deduction':
    st.markdown("### 🏗️ تخصيم الوحدات التفصيلي")
    if st.button("🏠 العودة للقائمة الرئيسية"): 
        st.session_state.page = 'main_menu'; st.rerun()

    with st.form("industrial_logic_form", clear_on_submit=True):
        col_header1, col_header2 = st.columns(2)
        u_label = col_header1.text_input("اسم الوحدة (اختياري)")
        u_kind = col_header2.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])

        st.subheader("📏 أبعاد الوحدة الأساسية")
        c1, c2, c3 = st.columns(3)
        W = c1.number_input("العرض الكلي (W)", min_value=0)
        H = c2.number_input("الارتفاع الكلي (H)", min_value=0)
        D = c3.number_input("العمق الكلي (D)", min_value=0)

        st.divider()
        st.subheader("📦 الأرفف والفواصل والأدراج")
        # الأرفف
        cs1, cs2, cs3 = st.columns(3)
        s_w = cs1.number_input("عرض الرف الصافي", value=0)
        s_d = cs2.number_input("عمق الرف الصافي", value=0)
        s_q = cs3.number_input("عدد الأرفف", min_value=0, step=1)
        # الفواصل
        cv1, cv2, cv3 = st.columns(3)
        v_h = cv1.number_input("ارتفاع الفاصل الصافي", value=0)
        v_d = cv2.number_input("عمق الفاصل الصافي", value=0)
        v_q = cv3.number_input("عدد الفواصل", min_value=0, step=1)
        # الأدراج
        cd1, cd2, cd3 = st.columns(3)
        dr_w = cd1.number_input("عرض الدرج", value=0)
        dr_d = cd2.number_input("عمق الدرج ثابت", value=0)
        dr_q = cd3.number_input("عدد الأدراج", min_value=0, step=1)

        submit = st.form_submit_button("🚀 إضافة الوحدة ومكوناتها")

    if submit and W > 0 and H > 0:
        name = u_label if u_label else f"وحدة {u_kind}"
        
        # --- [ أ ] منطق التخصيم الهندسي ---
        h_ded = 13 if u_kind in ["سفلي", "دولاب خزين"] else 5
        f_h, f_w, f_d = H - h_ded, W - 5, D - 5

        # 1. تخصيم الألومنيوم
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

        # 2. تخصيم الفيبر (تطبيق قاعدة الأرضية والسقفية)
        add_to_project(name, "فيبر", "ضهرية الوحدة", f"{f_w}×{f_h}", 1, "حشو")
        add_to_project(name, "فيبر", "أرضية الوحدة", f"{f_w}×{f_d}", 1, "حشو")
        
        # الشرط المطلوب: لو مش سفلي ضيف سقفية
        if u_kind != "سفلي":
            add_to_project(name, "فيبر", "سقفية الوحدة", f"{f_w}×{f_d}", 1, "حشو")
            
        add_to_project(name, "فيبر", "أجناب الوحدة", f"{f_h}×{f_d}", 2, "حشو")

        # 3. الأرفف
        if s_q > 0:
            add_to_project(name, "ألومنيوم", "عرض الرف", s_w, s_q*2, "مفرد")
            add_to_project(name, "ألومنيوم", "عمق الرف", s_d, s_q*2, "مفرد")
            add_to_project(name, "فيبر", "حشو رف", f"{s_w-5}×{s_d-5}", s_q, "خصم 5 سم")

        # 4. الفواصل
        if v_q > 0:
            add_to_project(name, "ألومنيوم", "ارتفاع فاصل", v_h, v_q*2, "مفرد")
            add_to_project(name, "ألومنيوم", "عمق فاصل", v_d, v_q*2, "مفرد")
            add_to_project(name, "فيبر", "حشو فاصل", f"{v_h-5}×{v_d-5}", v_q, "خصم 5 سم")

        # 5. الأدراج (معادلات دقيقة)
        if dr_q > 0:
            add_to_project(name, "ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q*2, "علبة درج")
            add_to_project(name, "ألومنيوم", "جنب درج", dr_d, dr_q*2, "علبة درج")
            add_to_project(name, "فيبر", "أرضية درج", f"{dr_alum_w}×{dr_d}", dr_q, "حشو")

        st.toast(f"✅ تمت إضافة {name} بنجاح!")

    if st.session_state.project_data:
        st.divider()
        df = pd.DataFrame(st.session_state.project_data)
        for n, g in df.groupby("اسم الوحدة"):
            with st.expander(f"📍 مراجعة تخصيم وحدة: {n}"):
                st.table(g.drop(columns=["اسم الوحدة"]))
        
        if st.button("💰 حساب استهلاك الخامات والتسعير ⬅️", use_container_width=True):
            st.session_state.page = 'inventory'; st.rerun()

# ==========================================
# 📊 الصفحة الثالثة: الجرد والفاتورة
# ==========================================
elif st.session_state.page == 'inventory':
    st.markdown("## 📊 استهلاك خامات المشروع الكلي")
    if st.button("🏠 العودة للقائمة"): 
        st.session_state.page = 'main_menu'; st.rerun()

    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        
        # حساب أعواد الألومنيوم (6 متر)
        alum = df[df["الخامة"] == "ألومنيوم"].copy()
        alum["المقاس (سم)"] = pd.to_numeric(alum["المقاس (سم)"], errors='coerce')
        summary = alum.groupby("نوع التخصيم").apply(lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()).reset_index(name="إجمالي سم")
        summary["الأعواد"] = summary["إجمالي سم"].apply(lambda x: math.ceil(x / 600))
        
        st.subheader("🥢 تقدير أعواد الألومنيوم")
        st.table(summary)

        # حساب ألواح الفيبر (2.80 * 1.30)
        total_area = 0
        for _, row in df[df["الخامة"] == "فيبر"].iterrows():
            try:
                dims = str(row["المقاس (سم)"]).split('×')
                if len(dims) == 2:
                    total_area += float(dims[0]) * float(dims[1]) * row["العدد"]
            except: continue
        sheets = math.ceil(total_area / (280 * 130))
        st.metric("عدد ألواح الفيبر المطلوبة", f"{sheets} لوح")

        st.divider()
        st.subheader("💵 فاتورة المشتريات المفتوحة")
        
        base_bill = [{"الصنف": f"ألومنيوم {r['نوع التخصيم']}", "الكمية": r["الأعواد"], "السعر": 0.0} for _, r in summary.iterrows()]
        base_bill.append({"الصنف": "لوح فيبر كامل", "الكمية": sheets, "السعر": 0.0})
        
        final_bill = st.data_editor(pd.DataFrame(base_bill), num_rows="dynamic", use_container_width=True)
        total = (final_bill["الكمية"] * final_bill["السعر"]).sum()
        st.markdown(f"<h2>💰 التكلفة الإجمالية: {total:,.2f} ج.م</h2>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            csv = final_bill.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل الفاتورة", data=csv, file_name="DOGGA_Invoice.csv")
        with c2:
            if st.button("🗑️ مسح كل بيانات المشروع"):
                st.session_state.project_data = []; st.session_state.page = 'main_menu'; st.rerun()
    else:
        st.error("⚠️ لا توجد بيانات مسجلة حالياً.")
