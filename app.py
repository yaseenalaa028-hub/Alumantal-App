import streamlit as st
import pandas as pd
import math
import json

# ========== إعدادات الصفحة ==========
st.set_page_config(page_title="ضجة سيستم", layout="wide", page_icon="🎯")

# ========== CSS ==========
st.markdown("""
    <style>
    .stApp {
        background: #f0f2f5;
    }
    .main-header {
        background: linear-gradient(135deg, #1e3a5f, #0f2b3d);
        border-radius: 30px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .main-header h1 {
        color: white;
        font-size: 1.8rem;
    }
    .main-header p {
        color: rgba(255,255,255,0.8);
        font-size: 0.8rem;
    }
    .stButton button {
        background: linear-gradient(135deg, #1e3a5f, #0f2b3d) !important;
        color: white !important;
        border-radius: 25px !important;
        height: auto !important;
        padding: 12px !important;
        font-weight: bold !important;
    }
    .stButton button:hover {
        opacity: 0.9;
        transform: scale(1.01);
    }
    .stNumberInput input, .stTextInput input, .stSelectbox div {
        background-color: #fff9e6 !important;
        border: 1px solid #ffc107 !important;
        border-radius: 12px !important;
    }
    label {
        color: #1e3a5f !important;
        font-weight: bold !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1e3a5f !important;
    }
    .stDataFrame {
        background: white !important;
        border-radius: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ========== تهيئة Session State ==========
if 'project_data' not in st.session_state:
    st.session_state.project_data = []
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'prices' not in st.session_state:
    st.session_state.prices = {}
if 'shelf_count' not in st.session_state:
    st.session_state.shelf_count = 1

# ========== دوال مساعدة ==========
def add_to_project(unit_name, material, item_name, dimensions, qty, item_type):
    st.session_state.project_data.append({
        "الوحدة": unit_name,
        "الخامة": material,
        "القطعة": item_name,
        "المقاس": dimensions,
        "العدد": qty,
        "النوع": item_type
    })

def save_prices():
    st.session_state.prices = st.session_state.get('prices', {})

# ========== حساب الإحصائيات ==========
def get_stats():
    stats = {
        "مفرد": 0, "متقارب": 0, "علبه درج": 0, "درف": 0, "بلتي إن": 0,
        "fibre_area": 0, "ammonia_area": 0, "cladding_area": 0
    }
    sheet_size = 280 * 130
    
    for item in st.session_state.project_data:
        if item["الخامة"] == "مونتال":
            val = float(item["المقاس"].split()[0]) if item["المقاس"].split()[0].replace('.','',1).isdigit() else 0
            stats[item["النوع"]] += val * item["العدد"]
        elif item["الخامة"] == "درف":
            val = float(item["المقاس"].split()[0]) if item["المقاس"].split()[0].replace('.','',1).isdigit() else 0
            stats["درف"] += val * item["العدد"]
        elif item["الخامة"] == "بلتي إن":
            val = float(item["المقاس"].split()[0]) if item["المقاس"].split()[0].replace('.','',1).isdigit() else 0
            stats["بلتي إن"] += val * item["العدد"]
        elif item["الخامة"] == "فيبر" and "×" in item["المقاس"]:
            parts = item["المقاس"].split("×")
            w = float(parts[0]) if parts[0].replace('.','',1).isdigit() else 0
            h = float(parts[1].split()[0]) if parts[1].split()[0].replace('.','',1).isdigit() else 0
            stats["fibre_area"] += w * h * item["العدد"]
        elif item["الخامة"] == "أمونيا" and "×" in item["المقاس"]:
            parts = item["المقاس"].split("×")
            w = float(parts[0]) if parts[0].replace('.','',1).isdigit() else 0
            h = float(parts[1].split()[0]) if parts[1].split()[0].replace('.','',1).isdigit() else 0
            stats["ammonia_area"] += w * h * item["العدد"]
        elif item["الخامة"] == "كلادينج" and "×" in item["المقاس"]:
            parts = item["المقاس"].split("×")
            w = float(parts[0]) if parts[0].replace('.','',1).isdigit() else 0
            h = float(parts[1].split()[0]) if parts[1].split()[0].replace('.','',1).isdigit() else 0
            stats["cladding_area"] += w * h * item["العدد"]
    
    return stats

# ========== الهيدر ==========
st.markdown(f"""
<div class="main-header">
    <h1>🎯 ضجة سيستم</h1>
    <p>نظام تخصيص المونتال والفيبر والدرف والكلادينج</p>
</div>
""", unsafe_allow_html=True)

# ========== الصفحة الرئيسية ==========
if st.session_state.page == 'main':
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📦 تخصيص الوحدات", use_container_width=True):
            st.session_state.page = 'deduction'
            st.rerun()
    with col2:
        if st.button("🔧 تخصيم الدرف", use_container_width=True):
            st.session_state.page = 'handles'
            st.rerun()
    with col3:
        if st.button("📊 حساب الخامات", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()
    
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #6c757d;'>برمجة المهندس ياسين علاء © 2025<br>جميع الحقوق محفوظة - ضجة سيستم</p>", unsafe_allow_html=True)

# ========== تخصيص الوحدات ==========
elif st.session_state.page == 'deduction':
    st.markdown("## 📦 تخصيص الوحدات")
    
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'main'
        st.rerun()
    
    with st.form("unit_form"):
        st.markdown("### 📏 بيانات الوحدة")
        col1, col2 = st.columns(2)
        with col1:
            unit_name = st.text_input("اسم الوحدة", placeholder="مثال: مطبخ سفلي")
            unit_type = st.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])
        with col2:
            W = st.number_input("العرض الكلي (سم)", value=0.0, step=0.1)
            H = st.number_input("الارتفاع الكلي (سم)", value=0.0, step=0.1)
            D = st.number_input("العمق الكلي (سم)", value=0.0, step=0.1)
        
        st.markdown("---")
        st.markdown("### 📦 الأرفف")
        
        # عرض الأرفف الديناميكية
        for i in range(1, st.session_state.shelf_count + 1):
            with st.expander(f"الرف رقم {i}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    sw = st.number_input(f"عرض الرف {i} (سم)", key=f"shelf_w_{i}", value=0.0, step=0.1)
                with col2:
                    sd = st.number_input(f"عمق الرف {i} (سم)", key=f"shelf_d_{i}", value=0.0, step=0.1)
                with col3:
                    sq = st.number_input(f"عدد الرفوف {i}", key=f"shelf_q_{i}", value=0, step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("➕ إضافة رف", use_container_width=True):
                st.session_state.shelf_count += 1
                st.rerun()
        with col2:
            if st.form_submit_button("🗑️ حذف آخر رف", use_container_width=True) and st.session_state.shelf_count > 1:
                st.session_state.shelf_count -= 1
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 📐 الفواصل")
        col1, col2, col3 = st.columns(3)
        with col1:
            v_h = st.number_input("ارتفاع الفاصل (سم)", value=0.0, step=0.1)
        with col2:
            v_d = st.number_input("عمق الفاصل (سم)", value=0.0, step=0.1)
        with col3:
            v_q = st.number_input("عدد الفواصل", value=0, step=1)
        
        st.markdown("---")
        st.markdown("### 🗄️ الأدراج")
        col1, col2, col3 = st.columns(3)
        with col1:
            dr_w = st.number_input("عرض الدرج (سم)", value=0.0, step=0.1)
        with col2:
            dr_d = st.number_input("عمق الدرج (سم)", value=0.0, step=0.1)
        with col3:
            dr_q = st.number_input("عدد الأدراج", value=0, step=1)
        
        submitted = st.form_submit_button("✅ حفظ الوحدة", use_container_width=True)
    
    if submitted and W > 0 and H > 0:
        name = unit_name if unit_name else f"وحدة {unit_type}"
        h_ded = 13.0 if unit_type in ["سفلي", "دولاب خزين"] else 5.0
        f_h, f_w, f_d = H - h_ded, W - 5.0, D - 5.0
        
        # مونتال الهيكل
        if unit_type == "سفلي":
            add_to_project(name, "مونتال", "قائم ارتفاع", f"{f_h} سم", 2, "مفرد")
            add_to_project(name, "مونتال", "قائم ارتفاع", f"{f_h} سم", 2, "متقارب")
            add_to_project(name, "مونتال", "عارضة عرض", f"{f_w} سم", 3, "مفرد")
            add_to_project(name, "مونتال", "عارضة عرض", f"{f_w} سم", 1, "متقارب")
            add_to_project(name, "مونتال", "رباط عمق", f"{f_d} سم", 2, "مفرد")
            add_to_project(name, "مونتال", "رباط عمق", f"{f_d} سم", 2, "متقارب")
        else:
            add_to_project(name, "مونتال", "قائم ارتفاع", f"{f_h} سم", 2, "مفرد")
            add_to_project(name, "مونتال", "قائم ارتفاع", f"{f_h} سم", 2, "متقارب")
            add_to_project(name, "مونتال", "عارضة عرض", f"{f_w} سم", 2, "مفرد")
            add_to_project(name, "مونتال", "عارضة عرض", f"{f_w} سم", 2, "متقارب")
            add_to_project(name, "مونتال", "رباط عمق", f"{f_d} سم", 4, "متقارب")
        
        # فيبر الهيكل
        add_to_project(name, "فيبر", "ضهرية", f"{f_w}×{f_h} سم", 1, "لوح")
        add_to_project(name, "فيبر", "أرضية", f"{f_w}×{f_d} سم", 1, "لوح")
        if unit_type != "سفلي":
            add_to_project(name, "فيبر", "سقفية", f"{f_w}×{f_d} سم", 1, "لوح")
        add_to_project(name, "فيبر", "أجناب", f"{f_h}×{f_d} سم", 2, "لوح")
        
        # الأرفف
        for i in range(1, st.session_state.shelf_count + 1):
            sw = st.session_state.get(f"shelf_w_{i}", 0)
            sd = st.session_state.get(f"shelf_d_{i}", 0)
            sq = st.session_state.get(f"shelf_q_{i}", 0)
            if sq > 0 and sw > 0 and sd > 0:
                add_to_project(name, "مونتال", f"عرض رف {i}", f"{sw} سم", sq * 2, "مفرد")
                add_to_project(name, "مونتال", f"عمق رف {i}", f"{sd} سم", sq * 2, "مفرد")
                add_to_project(name, "فيبر", f"حشو رف {i} (فيبر)", f"{sw-5}×{sd-5} سم", sq, "لوح")
                add_to_project(name, "أمونيا", f"حشو رف {i} (أمونيا)", f"{sw-5}×{sd-5} سم", sq, "لوح")
        
        # الفواصل
        if v_q > 0 and v_h > 0 and v_d > 0:
            add_to_project(name, "مونتال", "ارتفاع فاصل", f"{v_h} سم", v_q * 2, "مفرد")
            add_to_project(name, "مونتال", "عمق فاصل", f"{v_d} سم", v_q * 2, "مفرد")
            add_to_project(name, "فيبر", "حشو فاصل", f"{v_h-5}×{v_d-5} سم", v_q, "لوح")
        
        # الأدراج
        if dr_q > 0 and dr_w > 0 and dr_d > 0:
            add_to_project(name, "مونتال", "وش/ضهر درج", f"{dr_w-2.5} سم", dr_q * 2, "علبه درج")
            add_to_project(name, "مونتال", "جنب درج", f"{dr_d} سم", dr_q * 2, "علبه درج")
            add_to_project(name, "فيبر", "أرضية درج", f"{dr_w-7.5}×{dr_d-5} سم", dr_q, "لوح")
        
        st.success(f"✅ تمت إضافة {name}")
        st.rerun()

# ========== تخصيم الدرف ==========
elif st.session_state.page == 'handles':
    st.markdown("## 🔧 تخصيم الدرف والكلادينج")
    
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'main'
        st.rerun()
    
    with st.form("handles_form"):
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("📏 ارتفاع الدرفة (سم)", value=0.0, step=0.1)
            count = st.number_input("🔢 عدد الدرف", value=1, step=1, min_value=1)
        with col2:
            width = st.number_input("📐 عرض الدرفة (سم)", value=0.0, step=0.1)
            project_name = st.text_input("🏷️ اسم المشروع", placeholder="مثال: درفة مطبخ")
        
        submitted = st.form_submit_button("✅ حساب وإضافة", use_container_width=True)
    
    if submitted and height > 0 and width > 0:
        name = project_name if project_name else "درفة جديدة"
        sheet_size = 280 * 130
        total_cladding = 0
        
        for i in range(count):
            add_to_project(name, "أمونيا", "جنب أمونيا", f"{height} سم", 2, "أمونيا")
            add_to_project(name, "بلتي إن", "مقبض بلتي إن", f"{width} سم", 1, "بلتي إن")
            add_to_project(name, "درف", "درفة عدية (سوستة)", f"{width} سم", 1, "درف")
            total_cladding += height * width
            add_to_project(name, "كلادينج", "لوح كلادينج", f"{height}×{width} سم", 1, "كلادينج")
        
        required_sheets = math.ceil(total_cladding / sheet_size)
        st.success(f"✅ تمت إضافة {count * 4} قطعة")
        st.info(f"📦 ألواح الكلادينج المطلوبة: {required_sheets} لوح (مقاس 280×130 سم)")
        st.rerun()

# ========== حساب الخامات ==========
elif st.session_state.page == 'inventory':
    st.markdown("## 📊 حساب الخامات")
    
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'main'
        st.rerun()
    
    stats = get_stats()
    sheet_size = 280 * 130
    
    # إحصائيات
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("عود مفرد", math.ceil(stats["مفرد"] / 600))
        st.metric("عود درف", math.ceil(stats["درف"] / 600))
    with col2:
        st.metric("عود متقارب", math.ceil(stats["متقارب"] / 600))
        st.metric("عود بلتي إن", math.ceil(stats["بلتي إن"] / 600))
    with col3:
        st.metric("عود علبة درج", math.ceil(stats["علبه درج"] / 600))
        st.metric("لوح فيبر", math.ceil(stats["fibre_area"] / sheet_size))
    with col4:
        st.metric("لوح أمونيا", math.ceil(stats["ammonia_area"] / sheet_size))
        st.metric("لوح كلادينج", math.ceil(stats["cladding_area"] / sheet_size))
    
    st.markdown("---")
    
    # جدول التسعير
    st.markdown("### 💰 جدول التسعير (مفتوح للتعديل)")
    
    sheet_items = [
        {"الصنف": "مونتال مفرد", "الكمية": math.ceil(stats["مفرد"] / 600), "الوحدة": "عود"},
        {"الصنف": "مونتال متقارب", "الكمية": math.ceil(stats["متقارب"] / 600), "الوحدة": "عود"},
        {"الصنف": "مونتال علبة درج", "الكمية": math.ceil(stats["علبه درج"] / 600), "الوحدة": "عود"},
        {"الصنف": "عود درف", "الكمية": math.ceil(stats["درف"] / 600), "الوحدة": "عود"},
        {"الصنف": "عود بلتي إن", "الكمية": math.ceil(stats["بلتي إن"] / 600), "الوحدة": "عود"},
        {"الصنف": "لوح فيبر", "الكمية": math.ceil(stats["fibre_area"] / sheet_size), "الوحدة": "لوح"},
        {"الصنف": "لوح أمونيا", "الكمية": math.ceil(stats["ammonia_area"] / sheet_size), "الوحدة": "لوح"},
        {"الصنف": "لوح كلادينج", "الكمية": math.ceil(stats["cladding_area"] / sheet_size), "الوحدة": "لوح"},
    ]
    
    df_prices = pd.DataFrame(sheet_items)
    df_prices["السعر"] = df_prices["الصنف"].apply(lambda x: st.session_state.prices.get(x, 0))
    df_prices["الإجمالي"] = df_prices["الكمية"] * df_prices["السعر"]
    
    edited_df = st.data_editor(df_prices, use_container_width=True, hide_index=True, num_rows="dynamic")
    
    if st.button("💾 حفظ الأسعار"):
        for _, row in edited_df.iterrows():
            st.session_state.prices[row["الصنف"]] = row["السعر"]
        st.success("✅ تم حفظ الأسعار")
    
    total_cost = edited_df["الإجمالي"].sum()
    st.markdown(f"<p style='font-size: 1.5rem; font-weight: bold; color: #1e3a5f; text-align: center; background: #fff9e6; padding: 15px; border-radius: 20px;'>💰 التكلفة الإجمالية: {total_cost:,.2f} ج.م</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # عرض القطع المحفوظة
    st.markdown(f"### 📁 القطع المحفوظة ({len(st.session_state.project_data)})")
    
    if st.session_state.project_data:
        df_items = pd.DataFrame(st.session_state.project_data)
        st.dataframe(df_items, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            csv = df_items.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 تحميل تقرير CSV", csv, "doga_report.csv", use_container_width=True)
        with col2:
            if st.button("🗑️ مسح كل البيانات", use_container_width=True):
                st.session_state.project_data = []
                st.session_state.prices = {}
                st.rerun()
    else:
        st.info("لا توجد بيانات محفوظة")
