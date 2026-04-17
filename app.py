import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات النظام
# ==========================================
st.set_page_config(page_title="دجة سمارت سستيم", layout="wide", initial_sidebar_state="collapsed")

if "projects" not in st.session_state: st.session_state.projects = []
if "current_page" not in st.session_state: st.session_state.current_page = "home"
if "last_unit_id" not in st.session_state: st.session_state.last_unit_id = None

@st.cache_data
def clean_numbers(df):
    def format_num(x):
        if pd.isna(x) or x is None: return ""
        if isinstance(x, (int, float)): return f"{float(x):g}"
        return str(x)
    return df.map(format_num)

# ==========================================
# 2. الصفحة الرئيسية
# ==========================================
if st.session_state.current_page == "home":
    st.markdown("""
        <div style='text-align:center; padding: 5rem 2rem;'>
            <h1 style='color:#f39c12; font-size: 4em; font-weight: bold;'>دجة سمارت</h1>
            <h2 style='color:#ecf0f1; font-size: 1.8em;'>نظام التخصيم الفني المتكامل</h2>
            <p style='color:#bdc3c7; font-size: 1.3em;'>حسابات دقيقة للألمنيوم والفيبرجلاس</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 ابدأ التخصيم", use_container_width=True, type="primary"):
        st.session_state.current_page = "calc"
        st.rerun()

# ==========================================
# 3. صفحة الفاتورة
# ==========================================
elif st.session_state.current_page == "invoice":
    st.markdown("## 📄 **فاتورة الخامات النهائية**")
    
    col_back, col_export = st.columns([1, 3])
    if col_back.button("⬅️ العودة", use_container_width=True): 
        st.session_state.current_page = "calc"; st.rerun()
    
    # حساب الإجمالي
    total_mufred = total_motaqarib = total_fiber = 0
    for project in st.session_state.projects:
        for item in project["alum_items"]:
            total_mufred += item.get("length", 0) * item.get("count", 0) if item["type"] == "مفرد" else 0
            total_motaqarib += item.get("length", 0) * item.get("count", 0) if item["type"] != "مفرد" else 0
        
        for item in project["fiber_items"]:
            total_fiber += item.get("width", 0) * item.get("height", 0) * item.get("qty", 0)

    invoice_data = {
        "البيان": ["أعواد ألمنيوم مفرد", "أعواد ألمنيوم متقارب", "ألواح فيبرجلاس"],
        "الكمية": [round(total_mufred/600, 2), round(total_motaqarib/600, 2), round(total_fiber/(280*130), 2)],
        "سعر الوحدة": [0.0, 0.0, 0.0]
    }
    
    invoice_df = pd.DataFrame(invoice_data)
    edited_df = st.data_editor(invoice_df, column_config={
        "سعر الوحدة": st.column_config.NumberColumn(format="%.2f")
    }, use_container_width=True)
    
    edited_df["الإجمالي"] = edited_df["الكمية"] * edited_df["سعر الوحدة"]
    st.success(f"**💰 إجمالي الفاتورة: {edited_df['الإجمالي'].sum():,.2f} جنيه**")
    
    csv = edited_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button("📥 تحميل الفاتورة", csv, "فاتورة.csv", "text/csv")

# ==========================================
# 4. صفحة التخصيم مع خانات إضافية كاملة
# ==========================================
else:
    st.markdown("## 🛠️ **لوحة التخصيم المتقدمة**")
    
    # أزرار التحكم
    col1, col2, col3 = st.columns(3)
    if col1.button("🏠 الرئيسية", use_container_width=True): 
        st.session_state.current_page = "home"; st.rerun()
    if col2.button("📄 الفاتورة", use_container_width=True, type="primary"): 
        st.session_state.current_page = "invoice"; st.rerun()
    if col3.button("🗑️ مسح الجرد", use_container_width=True): 
        st.session_state.projects = []; st.session_state.last_unit_id = None; st.rerun()

    # ===== النموذج الكامل مع كل الخانات =====
    with st.form("advanced_calc", clear_on_submit=False):
        st.markdown("---")
        
        # معلومات أساسية
        col_client, col_type = st.columns(2)
        client_name = col_client.text_input("👤 **اسم العميل**")
        unit_type = col_type.selectbox("📦 **نوع الوحدة**", ["وحدة سفلية", "وحدة علوية", "دولاب خزينة"])

        st.markdown("### 📐 **المقاسات الأساسية**")
        col_w, col_h, col_d = st.columns(3)
        width = col_w.number_input("**العرض الكلي (سم)**", min_value=10.0, step=0.5)
        height = col_h.number_input("**الارتفاع الكلي (سم)**", min_value=10.0, step=0.5)
        depth = col_d.number_input("**العمق الكلي (سم)**", min_value=10.0, step=0.5)

        st.markdown("### 🗄️ **الأرفف**")
        col_sh1, col_sh2, col_sh3 = st.columns(3)
        shelves_count = col_sh1.number_input("**عدد الأرفف**", min_value=0, step=1)
        shelf_width = col_sh2.number_input("**عرض الرف (سم)**", min_value=0.0, step=0.5)
        shelf_depth = col_sh3.number_input("**عمق الرف (سم)**", min_value=0.0, step=0.5)

        st.markdown("### 🔀 **الفواصل**")
        col_v1, col_v2, col_v3 = st.columns(3)
        dividers_count = col_v1.number_input("**عدد الفواصل**", min_value=0, step=1)
        divider_height = col_v2.number_input("**ارتفاع الفاصل (سم)**", min_value=0.0, step=0.5)
        divider_depth = col_v3.number_input("**عمق الفاصل (سم)**", min_value=0.0, step=0.5)

        st.markdown("### 📂 **الأدراج**")
        col_dr1, col_dr2, col_dr3 = st.columns(3)
        drawers_count = col_dr1.number_input("**عدد الأدراج**", min_value=0, step=1)
        drawer_width = col_dr2.number_input("**عرض الدرج (سم)**", min_value=0.0, step=0.5)
        drawer_depth = col_dr3.number_input("**عمق الدرج (سم)**", min_value=0.0, step=0.5)

        # ===== خانات إضافية حسب طلبك =====
        st.markdown("### ➕ **إضافات اختيارية**")
        col_extra1, col_extra2, col_extra3 = st.columns(3)
        extra_vertical = col_extra1.number_input("**أعواد رأسية إضافية**", min_value=0, step=1)
        extra_horizontal = col_extra2.number_input("**أعواد أفقية إضافية**", min_value=0, step=1)
        extra_length = col_extra3.number_input("**طول العود الإضافي (سم)**", min_value=0.0, step=0.5)

        submit = st.form_submit_button("🔨 **حسّب كل حاجة وأضف**", use_container_width=True, type="primary")

    # ===== الحسابات المتقدمة =====
    if submit and width and height and depth:
        unit_id = f"{client_name}_{width:.1f}_{height:.1f}_{depth:.1f}"
        if st.session_state.last_unit_id != unit_id:
            
            # المقاسات النهائية
            final_h = height - (13 if unit_type in ["وحدة سفلية", "دولاب خزينة"] else 5)
            final_w = width - 5
            final_d = depth - 5
            
            alum_items = []
            fiber_items = []
            
            # ===== الألمنيوم الأساسي =====
            base_alum = [
                {"name": "ارتفاع رئيسي", "length": final_h, "count": 2, "type": "مفرد"},
                {"name": "ارتفاع متقارب", "length": final_h, "count": 2, "type": "متقارب"}
            ]
            
            if unit_type == "وحدة سفلية":
                base_alum.extend([
                    {"name": "عرض أمامي", "length": final_w, "count": 3, "type": "مفرد"},
                    {"name": "عرض خلفي", "length": final_w, "count": 1, "type": "متقارب"},
                    {"name": "عمق أمامي", "length": final_d, "count": 2, "type": "مفرد"},
                    {"name": "عمق خلفي", "length": final_d, "count": 2, "type": "متقارب"}
                ])
            else:
                base_alum.extend([
                    {"name": "عرض", "length": final_w, "count": 2, "type": "مفرد"},
                    {"name": "عرض متقارب", "length": final_w, "count": 2, "type": "متقارب"},
                    {"name": "عمق متقارب", "length": final_d, "count": 4, "type": "متقارب"}
                ])
            
            alum_items.extend(base_alum)

            # ===== الأرفف =====
            if shelves_count > 0 and shelf_width > 0 and shelf_depth > 0:
                alum_items.extend([
                    {"name": "رفوف عرض", "length": shelf_width, "count": shelves_count * 2, "type": "مفرد"},
                    {"name": "رفوف عمق", "length": shelf_depth, "count": shelves_count * 2, "type": "مفرد"}
                ])
                fiber_items.append({"name": "لوح رف", "width": shelf_width-5, "height": shelf_depth-5, "qty": shelves_count})

            # ===== الفواصل =====
            if dividers_count > 0 and divider_height > 0 and divider_depth > 0:
                alum_items.extend([
                    {"name": "فواصل ارتفاع", "length": divider_height, "count": dividers_count * 2, "type": "مفرد"},
                    {"name": "فواصل عمق", "length": divider_depth, "count": dividers_count * 2, "type": "مفرد"}
                ])
                fiber_items.append({"name": "لوح فاصل", "width": divider_height-5, "height": divider_depth-5, "qty": dividers_count})

            # ===== الأدراج =====
            if drawers_count > 0 and drawer_width > 0 and drawer_depth > 0:
                alum_items.extend([
                    {"name": "درج عرض", "length": drawer_width-2.5, "count": drawers_count * 2, "type": "2x8"},
                    {"name": "درج عمق", "length": drawer_depth, "count": drawers_count * 2, "type": "2x8"}
                ])
                fiber_items.append({"name": "لوح درج", "width": drawer_width, "height": drawer_depth, "qty": drawers_count})

            # ===== الإضافات الاختيارية =====
            if extra_vertical > 0:
                alum_items.append({"name": "رأسي إضافي", "length": extra_length, "count": extra_vertical, "type": "مفرد"})
            if extra_horizontal > 0:
                alum_items.append({"name": "أفقي إضافي", "length": extra_length, "count": extra_horizontal, "type": "مفرد"})

            # ===== الفيبر الأساسي =====
            fiber_items.extend([
                {"name": "ظهرية", "width": final_w, "height": final_h, "qty": 1},
                {"name": "أرضية", "width": final_w, "height": final_d, "qty": 1},
                {"name": "أجنحة", "width": final_h, "height": final_d, "qty": 2}
            ])

            # حفظ المشروع
            st.session_state.projects.append({
                "client": client_name or "غير محدد",
                "unit_type": unit_type,
                "alum_items": alum_items,
                "fiber_items": fiber_items,
                "dimensions": {"W": width, "H": height, "D": depth}
            })
            
            st.session_state.last_unit_id = unit_id
            st.balloons()
            st.success("🎉 تم التخصيم الكامل بنجاح!")
        else:
            st.warning("⚠️ هذه الوحدة موجودة بالفعل!")

    # ===== عرض الجرد =====
    if st.session_state.projects:
        st.markdown("---")
        for i, project in enumerate(st.session_state.projects):
            with st.expander(f"#{i+1} {project['unit_type']} - {project['client']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**🧱 الألمنيوم**")
                    st.dataframe(clean_numbers(pd.DataFrame(project["alum_items"])), hide_index=True)
                with col2:
                    st.markdown("**🪵 الفيبر**")
                    st.dataframe(clean_numbers(pd.DataFrame(project["fiber_items"])), hide_index=True)
