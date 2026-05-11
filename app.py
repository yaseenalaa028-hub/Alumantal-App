import streamlit as st
import pandas as pd
import math
import json
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="DOGGA SYSTEM - تخصيم الدرف والمقابض", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #0d1117, #050505, #020c1b);
        color: #d9a066;
    }
    div.stTextArea textarea {
        background-color: #0d1117 !important;
        color: #0096ff !important;
        border: 1px solid #0096ff !important;
        border-radius: 10px !important;
        min-height: 120px !important;
    }
    .main-btn-container div.stButton > button {
        background: rgba(0, 150, 255, 0.05) !important;
        border: 2px solid #0096ff !important;
        color: #0096ff !important;
        border-radius: 20px !important;
        padding: 15px 20px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        transition: 0.5s !important;
        margin-bottom: 15px !important;
    }
    .main-btn-container div.stButton > button:hover {
        background: #d9a066 !important;
        color: #1a1614 !important;
        border-color: #d9a066 !important;
    }
    h1 { color: #0096ff !important; text-align: center; }
    h2, h3 { color: #d9a066 !important; text-align: center; }
    .stNumberInput input, .stTextInput input {
        background-color: #0d1117 !important;
        color: #0096ff !important;
        border: 1px solid #0096ff !important;
        border-radius: 10px !important;
    }
    label { color: #d9a066 !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# ========== دوال الحفظ والتحميل التلقائي ==========
def save_project():
    """حفظ المشروع في localStorage عبر Session State"""
    if 'project_data' in st.session_state:
        st.session_state['saved_project'] = st.session_state.project_data.copy()
        st.session_state['last_saved'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_saved_project():
    """تحميل المشروع المحفوظ"""
    if 'saved_project' in st.session_state and st.session_state.saved_project:
        st.session_state.project_data = st.session_state.saved_project.copy()

# ========== تهيئة المتغيرات ==========
if 'project_data' not in st.session_state:
    st.session_state.project_data = []
if 'page' not in st.session_state:
    st.session_state.page = 'main_menu'
if 'saved_project' not in st.session_state:
    st.session_state.saved_project = []
if 'notes' not in st.session_state:
    st.session_state.notes = ""

# تحميل المشروع المحفوظ تلقائياً
load_saved_project()

def add_to_project(unit_name, category, item_name, length, qty, unit_type="-", width=None, height=None):
    """إضافة قطعة للمشروع مع دعم الأبعاد"""
    st.session_state.project_data.append({
        "اسم الوحدة": unit_name,
        "الخامة": category,
        "اسم القطعة": item_name,
        "المقاس (سم)": length,
        "العرض (سم)": width if width else length,
        "الارتفاع (سم)": height if height else "-",
        "العدد": qty,
        "نوع التخصيم": unit_type
    })
    save_project()  # حفظ تلقائي

# ========== دالة تخصيم الدرف والمقابض ==========
def calculate_darf_handles(unit_name, shelf_width, shelf_height, shelf_qty, is_balti=False):
    """
    تخصيم الدرف والمقابض
    - البلتي إن: إضافة 2 سم على العرض وتقسيم الناتج على 2، بدون هالك
    - الدرف: يضاف 7 سم هالك لكل قطعة
    """
    results = []
    
    for i in range(shelf_qty):
        if is_balti:
            # البلتي إن: زيادة 2 سم وتقسيم على 2
            handle_width = (shelf_width + 2) / 2
            # البلتي إن بدون هالك
            results.append({
                "القطعة": f"مقبض بلتي إن {i+1}",
                "المقاس": round(handle_width, 1),
                "الخامة": "بلتي إن",
                "عدد القطع": 2
            })
        else:
            # الدرف: زيادة 7 سم هالك
            handle_length = shelf_width + 7
            results.append({
                "القطعة": f"مقبض درف {i+1}",
                "المقاس": round(handle_length, 1),
                "الخامة": "درف",
                "عدد القطع": 2
            })
    
    return results

# ========== الواجهة الرئيسية ==========
if st.session_state.page == 'main_menu':
    st.markdown("<h1>⚡ DOGGA SYSTEM - تخصيم الدرف والمقابض</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d9a066;'>إدارة المشاريع | حفظ تلقائي | تخصيم دقيق</p>", unsafe_allow_html=True)
    
    # عرض معلومات الحفظ
    if 'last_saved' in st.session_state:
        st.info(f"💾 آخر حفظ: {st.session_state['last_saved']} | عدد القطع: {len(st.session_state.project_data)}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📦 تخصيم المشروع", use_container_width=True):
            st.session_state.page = 'deduction'
            st.rerun()
    with col2:
        if st.button("📊 المشاريع المحفوظة", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()
    with col3:
        if st.button("🔧 تخصيم الدرف والمقابض", use_container_width=True):
            st.session_state.page = 'handles'
            st.rerun()
    
    # ملاحظات مطولة
    st.divider()
    st.subheader("📝 ملاحظات المشروع")
    st.session_state.notes = st.text_area("اكتب ملاحظاتك هنا (تدوم مع حفظ المشروع)", 
                                           value=st.session_state.notes, 
                                           height=150,
                                           placeholder="يمكنك كتابة أي ملاحظات عن المشروع...")

# ========== صفحة تخصيم الدرف والمقابض ==========
elif st.session_state.page == 'handles':
    st.markdown("<h1>🔧 تخصيم الدرف والمقابض</h1>", unsafe_allow_html=True)
    
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'main_menu'
        st.rerun()
    
    st.info("""
    **ملاحظات التخصيم:**
    - 📏 **الدرف**: يضاف 7 سم هالك على كل قطعة
    - 🔩 **البلتي إن**: يضاف 2 سم على العرض ثم يقسم على 2، بدون هالك
    - 🪵 **الكلادينج**: على مقاس الدرفة بدون أي إضافات
    """)
    
    with st.form("handles_form"):
        unit_name = st.text_input("اسم الوحدة/الرف", placeholder="مثال: رف سفلي 120 سم")
        
        col1, col2 = st.columns(2)
        with col1:
            shelf_width = st.number_input("📏 عرض الرف (سم)", min_value=0.0, step=1.0, value=100.0)
            shelf_qty = st.number_input("🔢 عدد الأرفف", min_value=0, step=1, value=1)
        with col2:
            shelf_height = st.number_input("📐 ارتفاع الرف (سم) - للكلادينج", min_value=0.0, step=1.0, value=50.0)
        
        st.divider()
        st.subheader("🔩 اختيار نوع المقابض")
        
        col_handles = st.columns(2)
        with col_handles[0]:
            darf_qty = st.number_input("عدد مقابض درف (سوستة)", min_value=0, step=1, value=1)
        with col_handles[1]:
            balti_qty = st.number_input("عدد مقابض بلتي إن", min_value=0, step=1, value=1)
        
        st.divider()
        st.subheader("🪵 الكلادينج (على مقاس الدرفة)")
        cladding_qty = st.number_input("عدد ألواح الكلادينج", min_value=0, step=1, value=0)
        
        submitted = st.form_submit_button("✅ حساب وإضافة للمشروع", use_container_width=True)
    
    if submitted:
        if darf_qty > 0:
            darf_handles = calculate_darf_handles(unit_name, shelf_width, shelf_height, darf_qty, is_balti=False)
            for h in darf_handles:
                add_to_project(unit_name, h["الخامة"], h["القطعة"], h["المقاس"], h["عدد القطع"], "درف")
            st.success(f"✅ تم إضافة {darf_qty * 2} قطعة درف")
        
        if balti_qty > 0:
            balti_handles = calculate_darf_handles(unit_name, shelf_width, shelf_height, balti_qty, is_balti=True)
            for h in balti_handles:
                add_to_project(unit_name, h["الخامة"], h["القطعة"], h["المقاس"], h["عدد القطع"], "بلتي إن")
            st.success(f"✅ تم إضافة {balti_qty * 2} قطعة بلتي إن")
        
        if cladding_qty > 0:
            # الكلادينج على مقاس الدرفة (العرض × الارتفاع)
            for i in range(cladding_qty):
                add_to_project(unit_name, "كلادينج", f"لوح كلادينج {i+1}", f"{shelf_width}×{shelf_height}", 1, "كلادينج", shelf_width, shelf_height)
            st.success(f"✅ تم إضافة {cladding_qty} لوح كلادينج")
        
        st.rerun()
    
    # عرض ملخص المقابض المحفوظة
    if st.session_state.project_data:
        st.divider()
        handles_df = pd.DataFrame([x for x in st.session_state.project_data if x["الخامة"] in ["درف", "بلتي إن", "كلادينج"]])
        if not handles_df.empty:
            st.subheader("📋 ملخص المقابض المضافة")
            st.dataframe(handles_df, use_container_width=True)

# ========== التخصيم الرئيسي ==========
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
        st.subheader("📦 الأرفف (خانتين منفصلتين)")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("**🟢 فيبر**")
            s1_w = st.number_input("عرض الرف فيبر", value=0.0, key="fibre_w")
            s1_d = st.number_input("عمق الرف فيبر", value=0.0, key="fibre_d")
            s1_q = st.number_input("عدد الأرفف فيبر", min_value=0, key="fibre_q")
        with col_s2:
            st.markdown("**🟡 أمونيا**")
            s2_w = st.number_input("عرض الرف أمونيا", value=0.0, key="ammonia_w")
            s2_d = st.number_input("عمق الرف أمونيا", value=0.0, key="ammonia_d")
            s2_q = st.number_input("عدد الأرفف أمونيا", min_value=0, key="ammonia_q")

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
            h_ded = 13.0 if u_kind in ["سفلي", "دولاب خزين"] else 5.0
            f_h, f_w, f_d = H - h_ded, W - 5.0, D - 5.0

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
            add_to_project(name, "فيبر", "ضهرية", f"{f_w}×{f_h}", 1, "لوح")
            add_to_project(name, "فيبر", "أرضية", f"{f_w}×{f_d}", 1, "لوح")
            if u_kind != "سفلي":
                add_to_project(name, "فيبر", "سقفية", f"{f_w}×{f_d}", 1, "لوح")
            add_to_project(name, "فيبر", "أجناب", f"{f_h}×{f_d}", 2, "لوح")

            # أرفف الفيبر (خانة منفصلة)
            if s1_q > 0:
                add_to_project(name, "ألومنيوم", "عرض رف فيبر", s1_w, s1_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "عمق رف فيبر", s1_d, s1_q*2, "مفرد")
                add_to_project(name, "فيبر", "حشو رف فيبر", f"{s1_w-5}×{s1_d-5}", s1_q, "لوح")
            
            # أرفف الأمونيا (خانة منفصلة)
            if s2_q > 0:
                add_to_project(name, "ألومنيوم", "عرض رف أمونيا", s2_w, s2_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "عمق رف أمونيا", s2_d, s2_q*2, "مفرد")
                add_to_project(name, "أمونيا", "حشو رف أمونيا", f"{s2_w-5}×{s2_d-5}", s2_q, "لوح")

            # فواصل
            if v_q > 0:
                add_to_project(name, "ألومنيوم", "ارتفاع فاصل", v_h, v_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "عمق فاصل", v_d, v_q*2, "مفرد")
                add_to_project(name, "فيبر", "حشو فاصل", f"{v_h-5}×{v_d-5}", v_q, "لوح")

            # أدراج
            if dr_q > 0:
                add_to_project(name, "ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q*2, "علبه درج")
                add_to_project(name, "ألومنيوم", "جنب درج", dr_d, dr_q*2, "علبه درج")
                add_to_project(name, "فيبر", "أرضية درج", f"{dr_w-7.5}×{dr_d-5}", dr_q, "لوح")

            st.success(f"✅ تمت إضافة {name} للمشروع")
            st.rerun()

    # عرض المشروع الحالي
    if st.session_state.project_data:
        st.divider()
        df = pd.DataFrame(st.session_state.project_data)
        for n, g in df.groupby("اسم الوحدة"):
            with st.expander(f"📍 {n} - {len(g)} قطعة"):
                st.dataframe(g.drop(columns=["اسم الوحدة"]), use_container_width=True)
        
        if st.button("💰 عرض استهلاك الخامات", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()

# ========== صفحة الجرد والمخزون ==========
elif st.session_state.page == 'inventory':
    st.markdown("<h1>📊 استهلاك خامات المشروع</h1>", unsafe_allow_html=True)
    
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = 'main_menu'
        st.rerun()
    
    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        
        # حساب أعواد الألومنيوم
        alum = df[df["الخامة"] == "ألومنيوم"].copy()
        alum["المقاس (سم)"] = pd.to_numeric(alum["المقاس (سم)"], errors='coerce')
        
        if not alum.empty:
            st.subheader("🥢 أعواد الألومنيوم (6 متر)")
            summary = alum.groupby("نوع التخصيم").apply(
                lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()
            ).reset_index(name="إجمالي سم")
            summary["الأعواد"] = summary["إجمالي سم"].apply(lambda x: math.ceil(x / 600))
            st.dataframe(summary, use_container_width=True)
        
        # حساب ألواح الفيبر
        fibre_df = df[df["الخامة"] == "فيبر"]
        total_fibre_area = 0
        for _, row in fibre_df.iterrows():
            dims = str(row["المقاس (سم)"]).split('×')
            if len(dims) == 2:
                try:
                    total_fibre_area += float(dims[0]) * float(dims[1]) * row["العدد"]
                except:
                    pass
        fibre_sheets = math.ceil(total_fibre_area / (280 * 130)) if total_fibre_area > 0 else 0
        st.metric("🟢 ألواح الفيبر", f"{fibre_sheets} لوح")
        
        # حساب ألواح الأمونيا
        ammonia_df = df[df["الخامة"] == "أمونيا"]
        total_ammonia_area = 0
        for _, row in ammonia_df.iterrows():
            dims = str(row["المقاس (سم)"]).split('×')
            if len(dims) == 2:
                try:
                    total_ammonia_area += float(dims[0]) * float(dims[1]) * row["العدد"]
                except:
                    pass
        ammonia_sheets = math.ceil(total_ammonia_area / (280 * 130)) if total_ammonia_area > 0 else 0
        st.metric("🟡 ألواح الأمونيا", f"{ammonia_sheets} لوح")
        
        # حساب أعواد الدرف والبلتي إن والكلادينج
        st.divider()
        st.subheader("🪵 أعواد وخامات إضافية")
        
        darf_items = df[df["الخامة"] == "درف"]
        balti_items = df[df["الخامة"] == "بلتي إن"]
        cladding_items = df[df["الخامة"] == "كلادينج"]
        
        # الدرف (عود 6 متر)
        total_darf_len = 0
        for _, row in darf_items.iterrows():
            try:
                total_darf_len += float(row["المقاس (سم)"]) * row["العدد"]
            except:
                pass
        darf_sticks = math.ceil(total_darf_len / 600) if total_darf_len > 0 else 0
        st.metric("🥢 عود درف (سوستة)", f"{darf_sticks} عود")
        
        # البلتي إن (عود 6 متر - بدون هالك)
        total_balti_len = 0
        for _, row in balti_items.iterrows():
            try:
                total_balti_len += float(row["المقاس (سم)"]) * row["العدد"]
            except:
                pass
        balti_sticks = math.ceil(total_balti_len / 600) if total_balti_len > 0 else 0
        st.metric("🔩 عود بلتي إن", f"{balti_sticks} عود")
        
        # الكلادينج (على مقاس الدرفة)
        cladding_count = cladding_items["العدد"].sum() if not cladding_items.empty else 0
        st.metric("🪵 لوح كلادينج", f"{cladding_count} لوح (على مقاس الدرفة)")
        
        # عرض الملاحظات
        if st.session_state.notes:
            st.divider()
            st.subheader("📝 ملاحظات المشروع")
            st.info(st.session_state.notes)
        
        # خيارات التفريغ
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ تفريغ المشروع", use_container_width=True):
                st.session_state.project_data = []
                st.session_state.saved_project = []
                st.session_state.notes = ""
                save_project()
                st.success("تم تفريغ المشروع")
                st.rerun()
        with col2:
            if st.button("📥 تحميل تقرير CSV", use_container_width=True):
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("اضغط للتحميل", data=csv, file_name="project_report.csv", use_container_width=True)
    else:
        st.warning("⚠️ لا توجد بيانات في المشروع")
        if st.button("الرجوع للتخصيم"):
            st.session_state.page = 'deduction'
            st.rerun()
