import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات النظام والتنسيق الكامل
# ==========================================
st.set_page_config(
    page_title="دجة سمارت سستيم", 
    page_icon="🔨",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# تهيئة Session State كاملة
if "projects" not in st.session_state:
    st.session_state.projects = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "last_unit_id" not in st.session_state:
    st.session_state.last_unit_id = None
if "df_invoice" not in st.session_state:
    st.session_state.df_invoice = None

# وظيفة تنظيف الأرقام المتقدمة
@st.cache_data
def clean_numbers(df):
    def format_num(x):
        if pd.isna(x) or x is None:
            return ""
        if isinstance(x, (int, float)):
            return f"{float(x):g}"
        return str(x)
    return df.map(format_num)

# ==========================================
# 2. الصفحة الرئيسية الكاملة
# ==========================================
if st.session_state.current_page == "home":
    st.markdown("""
        <div style='text-align:center; padding: 5rem 2rem; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); border-radius: 20px; margin: 2rem 0;'>
            <h1 style='color:#f39c12; font-size: 4.5em; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>دجة سمارت</h1>
            <h2 style='color:#ecf0f1; font-size: 2em; margin: 1rem 0;'>نظام التخصيم الفني المتكامل</h2>
            <p style='color:#bdc3c7; font-size: 1.4em; margin: 2rem 0;'>حسابات دقيقة للألمنيوم والفيبرجلاس بأعلى سرعة ودقة</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    if col1.button("🚀 **ابدأ التخصيم**", use_container_width=True, type="primary"):
        st.session_state.current_page = "calc"
        st.rerun()
    
    st.info("📋 **المميزات:**\n• حسابات تلقائية كاملة\n• جرد تفصيلي\n• فاتورة جاهزة للطباعة\n• تصدير Excel")

# ==========================================
# 3. صفحة الفاتورة الكاملة
# ==========================================
elif st.session_state.current_page == "invoice":
    st.markdown("### 📄 **فاتورة الخامات النهائية**")
    
    col_back, col_reset = st.columns([1, 1])
    if col_back.button("⬅️ **العودة للتخصيم**", use_container_width=True):
        st.session_state.current_page = "calc"
        st.rerun()
    
    if col_reset.button("🔄 **إعادة حساب الفاتورة**", use_container_width=True):
        if "df_invoice" in st.session_state:
            del st.session_state.df_invoice
        st.rerun()

    if st.session_state.projects:
        total_mufred = total_motaqarib = total_fiber = 0
        
        for project in st.session_state.projects:
            for item in project["alum_items"]:
                length = item.get("الطول (سم)", 0)
                count = item.get("العدد", 0)
                if item.get("النوع") == "مفرد":
                    total_mufred += length * count
                else:
                    total_motaqarib += length * count
            
            for item in project["fiber_items"]:
                width = item.get("العرض", 0)
                height = item.get("الارتفاع", 0)
                qty = item.get("الكمية", 0)
                total_fiber += width * height * qty

        qty_alum_m = round(total_mufred / 600, 2)
        qty_alum_t = round(total_motaqarib / 600, 2)
        qty_fiber = round(total_fiber / (280 * 130), 2)

        invoice_data = {
            "البيان": ["أعواد ألمنيوم (مفرد)", "أعواد ألمنيوم (متقارب)", "ألواح فيبرجلاس"],
            "الكمية": [qty_alum_m, qty_alum_t, qty_fiber],
            "سعر الوحدة": [0.0, 0.0, 0.0],
            "الإجمالي": [0.0, 0.0, 0.0]
        }
        
        df_invoice = pd.DataFrame(invoice_data)
        st.session_state.df_invoice = df_invoice
        
        st.markdown("### ✏️ **تحرير الأسعار والكميات**")
        edited_df = st.data_editor(
            st.session_state.df_invoice,
            column_config={
                "سعر الوحدة": st.column_config.NumberColumn("سعر الوحدة", format="%.2f"),
                "الكمية": st.column_config.NumberColumn("الكمية", format="%.3f")
            },
            num_rows="fixed",
            use_container_width=True,
            hide_index=True
        )
        
        edited_df["الإجمالي"] = edited_df["الكمية"] * edited_df["سعر الوحدة"]
        st.dataframe(clean_numbers(edited_df), use_container_width=True)
        
        total_amount = edited_df["الإجمالي"].sum()
        st.markdown(f"""
            <div style='background: linear-gradient(90deg, #27ae60, #2ecc71); color: white; padding: 2rem; border-radius: 15px; text-align: center;'>
                <h2 style='margin: 0;'>💰 إجمالي الفاتورة: {total_amount:,.2f} جنيه</h2>
            </div>
        """, unsafe_allow_html=True)
        
        csv_data = edited_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📥 تحميل الفاتورة", data=csv_data, file_name="invoice.csv", mime="text/csv")
    else:
        st.warning("⚠️ لا توجد وحدات في الجرد.")

# ==========================================
# 4. صفحة التخصيم الكاملة (كل الخانات)
# ==========================================
else: 
    st.markdown("### 🛠️ **لوحة التخصيم المتقدمة**")
    
    col_home, col_invoice, col_clear, col_stats = st.columns(4)
    if col_home.button("🏠 الرئيسية", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()
    if col_invoice.button("📄 الفاتورة", use_container_width=True, type="primary"):
        st.session_state.current_page = "invoice"
        st.rerun()
    if col_clear.button("🗑️ مسح الجرد", use_container_width=True):
        st.session_state.projects = []
        st.session_state.last_unit_id = None
        st.rerun()
    if st.session_state.projects:
        col_stats.metric("📦 عدد الوحدات", len(st.session_state.projects))

    # عرض الجرد الحالي (خانات التخصيم التفصيلية)
    if st.session_state.projects:
        st.markdown("### 📋 **الجرد التفصيلي ومقاسات القطع**")
        for i, project in enumerate(st.session_state.projects):
            with st.expander(f"وحدة {i+1}: {project['client_name']} - {project['unit_type']}", expanded=False):
                col_a, col_f = st.columns(2)
                with col_a:
                    st.write("📐 **تخصيم الألمنيوم:**")
                    st.table(pd.DataFrame(project['alum_items']))
                with col_f:
                    st.write("🖼️ **تخصيم الفيبر:**")
                    st.table(pd.DataFrame(project['fiber_items']))

    # النموذج الكامل بكل خاناتك
    with st.form(key="complete_calc_form"):
        st.markdown("---")
        col_client, col_unit = st.columns([2, 1])
        client_name = col_client.text_input("👤 اسم العميل", placeholder="اكتب اسم العميل")
        unit_type = col_unit.selectbox("📦 نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزينة"])

        st.markdown("### 📐 المقاسات الأساسية (سم)")
        col_w, col_h, col_d = st.columns(3)
        width = col_w.number_input("العرض الكلي", value=None, min_value=0.0, step=0.5)
        height = col_h.number_input("الارتفاع الكلي", value=None, min_value=0.0, step=0.5)
        depth = col_d.number_input("العمق الكلي", value=None, min_value=0.0, step=0.5)

        st.markdown("### 🗄️ الأرفف")
        col_sh1, col_sh2, col_sh3 = st.columns(3)
        shelves_count = col_sh1.number_input("عدد الأرفف", value=None, min_value=0, step=1)
        shelf_width = col_sh2.number_input("عرض الرف", value=None, min_value=0.0)
        shelf_depth = col_sh3.number_input("عمق الرف", value=None, min_value=0.0)

        st.markdown("### 🔀 الفواصل")
        col_v1, col_v2, col_v3 = st.columns(3)
        dividers_count = col_v1.number_input("عدد الفواصل", value=None, min_value=0, step=1)
        divider_height = col_v2.number_input("ارتفاع الفاصل", value=None, min_value=0.0)
        divider_depth = col_v3.number_input("عمق الفاصل", value=None, min_value=0.0)

        st.markdown("### 📂 الأدراج")
        col_dr1, col_dr2, col_dr3 = st.columns(3)
        drawers_count = col_dr1.number_input("عدد الأدراج", value=None, min_value=0, step=1)
        drawer_width = col_dr2.number_input("عرض الدرج", value=None, min_value=0.0)
        drawer_depth = col_dr3.number_input("عمق الدرج", value=None, min_value=0.0)

        st.markdown("### ➕ إضافات")
        col_e1, col_e2, col_e3 = st.columns(3)
        extra_v = col_e1.number_input("أعواد رأسية إضافية", value=None, min_value=0)
        extra_h = col_e2.number_input("أعواد أفقية إضافية", value=None, min_value=0)
        extra_l = col_e3.number_input("طول العود الإضافي", value=None, min_value=0.0)

        submit_btn = st.form_submit_button("🔨 احسب وأضف للجرد", use_container_width=True, type="primary")

    if submit_btn:
        if width and height and depth:
            unit_id = f"{client_name}_{width}_{height}_{depth}"
            if st.session_state.last_unit_id != unit_id:
                # معادلات التخصيم
                f_h = height - (13 if unit_type != "وحدة علوية" else 5)
                f_w = width - 5
                f_d = depth - 5
                
                alum_items = [
                    {"القطعة": "قائم رئيسي", "الطول (سم)": f_h, "العدد": 2, "النوع": "مفرد"},
                    {"القطعة": "قائم متقارب", "الطول (سم)": f_h, "العدد": 2, "النوع": "متقارب"},
                    {"القطعة": "عرض أفقي", "الطول (سم)": f_w, "العدد": 4, "النوع": "مفرد"}
                ]
                
                fiber_items = [
                    {"اللوح": "جوانب", "العرض": f_h, "الارتفاع": f_d, "الكمية": 2},
                    {"اللوح": "أرضية", "العرض": f_w, "الارتفاع": f_d, "الكمية": 1},
                    {"اللوح": "ظهر", "العرض": f_h, "الارتفاع": f_w, "الكمية": 1}
                ]

                # معالجة الأرفف
                if shelves_count and shelf_width and shelf_depth:
                    alum_items.append({"القطعة": "إطار رف", "الطول (سم)": shelf_width, "العدد": int(shelves_count)*2, "النوع": "متقارب"})
                    fiber_items.append({"اللوح": "رف", "العرض": shelf_width, "الارتفاع": shelf_depth, "الكمية": int(shelves_count)})

                # معالجة الفواصل
                if dividers_count and divider_height:
                    alum_items.append({"القطعة": "قائم فاصل", "الطول (سم)": divider_height, "العدد": int(dividers_count)*2, "النوع": "متقارب"})
                    fiber_items.append({"اللوح": "فاصل", "العرض": divider_height, "الارتفاع": divider_depth, "الكمية": int(dividers_count)})

                # معالجة الأدراج
                if drawers_count and drawer_width:
                    alum_items.append({"القطعة": "جنب درج", "الطول (سم)": drawer_depth, "العدد": int(drawers_count)*2, "النوع": "مفرد"})
                    fiber_items.append({"اللوح": "قاع درج", "العرض": drawer_width, "الارتفاع": drawer_depth, "الكمية": int(drawers_count)})

                # معالجة الإضافات
                if extra_v and extra_l: alum_items.append({"القطعة": "إضافي رأسي", "الطول (سم)": extra_l, "العدد": int(extra_v), "النوع": "مفرد"})
                if extra_h and extra_l: alum_items.append({"القطعة": "إضافي أفقي", "الطول (سم)": extra_l, "العدد": int(extra_h), "النوع": "متقارب"})

                st.session_state.projects.append({
                    "client_name": client_name, "unit_type": unit_type,
                    "alum_items": alum_items, "fiber_items": fiber_items
                })
                st.session_state.last_unit_id = unit_id
                st.success("✅ تمت الإضافة للجرد!")
                st.rerun()
