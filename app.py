Here's the **complete corrected code** with all syntax errors fixed:

```python
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

    # حساب الجرد الكامل
    if st.session_state.projects:
        total_mufred = total_motaqarib = total_fiber = 0
        
        for project in st.session_state.projects:
            # الألمنيوم
            for item in project["alum_items"]:
                length = item.get("length", 0) or 0
                count = item.get("count", 0) or 0
                if item.get("type") == "مفرد":
                    total_mufred += length * count
                else:
                    total_motaqarib += length * count
            
            # الفيبر
            for item in project["fiber_items"]:
                width = item.get("width", 0) or 0
                height = item.get("height", 0) or 0
                qty = item.get("qty", 0) or 0
                total_fiber += width * height * qty

        # الكميات النهائية
        qty_alum_m = round(total_mufred / 600, 2)
        qty_alum_t = round(total_motaqarib / 600, 2)
        qty_fiber = round(total_fiber / (280 * 130), 2)

        # إنشاء جدول الفاتورة
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
            <div style='background: linear-gradient(90deg, #27ae60, #2ecc71); 
                        color: white; padding: 2rem; border-radius: 15px; text-align: center;'>
                <h2 style='margin: 0; font-size: 2.5em;'>💰 إجمالي الفاتورة</h2>
                <h1 style='margin: 0.5rem 0; font-size: 3.5em;'>{total_amount:,.2f} جنيه</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # تصدير
        csv_data = edited_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 **تحميل الفاتورة Excel**",
            data=csv_data,
            file_name=f"فاتورة_دجة_سمارت_{len(st.session_state.projects)}_وحدة.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ لا توجد وحدات في الجرد. ارجع لصفحة التخصيم أولاً.")

# ==========================================
# 4. صفحة التخصيم الكاملة مع مربعات فاضية
# ==========================================
else:  # calc page
    st.markdown("### 🛠️ **لوحة التخصيم المتقدمة**")
    
    # أزرار التحكم الكاملة
    col_home, col_invoice, col_clear, col_stats = st.columns(4)
    
    if col_home.button("🏠 **الصفحة الرئيسية**", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()
        
    if col_invoice.button("📄 **الفاتورة النهائية**", use_container_width=True, type="primary"):
        st.session_state.current_page = "invoice"
        st.rerun()
        
    if col_clear.button("🗑️ **مسح الجرد كاملاً**", use_container_width=True):
        st.session_state.projects = []
        st.session_state.last_unit_id = None
        if "df_invoice" in st.session_state:
            del st.session_state.df_invoice
        st.success("✅ تم مسح الجرد!")
        st.rerun()
    
    if st.session_state.projects:
        col_stats.metric("📦 **عدد الوحدات في الجرد**", len(st.session_state.projects))

    # عرض الجرد الحالي
    if st.session_state.projects:
        st.markdown("### 📋 **الجرد الحالي**")
        for i, project in enumerate(st.session_state.projects):
            with st.expander(f"وحدة {i+1}: {project.get('client_name', 'غير محدد')} - {project.get('unit_type', 'غير محدد')}"):
                st.write(f"**الألمنيوم:** {len(project['alum_items'])} قطعة")
                st.write(f"**الفيبر:** {len(project['fiber_items'])} قطعة")

    # ===== النموذج الكامل مع كل الخانات فاضية =====
    with st.form(key="complete_calc_form", clear_on_submit=False):
        st.markdown("---")
        
        # معلومات العميل والوحدة
        col_client, col_unit = st.columns([2, 1])
        client_name = col_client.text_input(
            "👤 **اسم العميل**", 
            value="", 
            placeholder="اكتب اسم العميل هنا",
            help="اسم العميل سيظهر في الجرد والفاتورة"
        )
        unit_type = col_unit.selectbox(
            "📦 **نوع الوحدة**", 
            ["وحدة سفلية", "وحدة علوية", "دولاب خزينة"],
            help="اختر نوع الوحدة للحسابات التلقائية"
        )

        st.markdown("### 📐 **المقاسات الأساسية (الكلية)**")
        col_w, col_h, col_d = st.columns(3)
        width = col_w.number_input(
            "🟢 **العرض الكلي (سم)**", 
            value=None, 
            min_value=0.0, 
            step=0.5, 
            format="%.1f",
            help="قيس العرض الكلي للوحدة"
        )
        height = col_h.number_input(
            "🔴 **الارتفاع الكلي (سم)**", 
            value=None, 
            min_value=0.0, 
            step=0.5, 
            format="%.1f",
            help="قيس الارتفاع الكلي للوحدة"
        )
        depth = col_d.number_input(
            "🔵 **العمق الكلي (سم)**", 
            value=None, 
            min_value=0.0, 
            step=0.5, 
            format="%.1f",
            help="قيس العمق الكلي للوحدة"
        )

        st.markdown("### 🗄️ **الأرفف**")
        col_sh1, col_sh2, col_sh3 = st.columns(3)
        shelves_count = col_sh1.number_input(
            "📊 **عدد الأرفف**", 
            value=None, 
            min_value=0, 
            step=1, 
            format="%d",
            help="اترك فاضي إذا لم يوجد أرفف"
        )
        shelf_width = col_sh2.number_input(
            "📏 **عرض الرف (سم)**", 
            value=None, 
            min_value=0.0, 
            step=0.5, 
            format="%.1f",
            help="اترك فاضي إذا لم يوجد أرفف"
        )
        shelf_depth = col_sh3.number_input(
            "📐 **عمق الرف (سم)**", 
            value=None, 
            min_value=0.0, 
            step=0.5, 
            format="%.1f",
            help="اترك فاضي إذا لم يوجد أرفف"
        )

        st.markdown("### 🔀 **الفواصل**")
        col_v1, col_v2, col_v3 = st.columns(3)
        dividers_count = col_v1.number_input(
            "📊 **عدد الفواصل**", 
            value=None, 
            min_value=0, 
            step=1, 
            format="%d",
            help="اترك فاضي إذا لم توجد فواصل"
        )
        divider_height = col_v2.number_input(
            "📏 **ارتفاع الفاصل (سم)**", 
            value=None, 
            min_value=0.0, 
            step=0.5, 
            format="%.1f",
            help="اترك فاضي إذا لم توجد فواصل"
        )
        divider_depth = col_v3.number_input(
            "📐 **عمق الفاصل (سم)**", 
            value=None, 
            min_value=0.0, 
            step=0.5, 
            format="%.1f",
            help="اترك فاضي إذا لم توجد فواصل"
        )

        st.markdown("### 📂 **الأدراج**")
        col_dr1, col_dr2, col_dr3 = st.columns(3)
        drawers_count = col_dr1.number_input(
            "📊 **عدد الأدراج**", 
            value=None, 
            min_value=0, 
            step=1, 
            format="%d",
            help="اترك فاضي إذا لم توجد أدراج"
        )
        drawer_width = col_dr2.number_input(
            "📏 **عرض الدرج (سم)**", 
            value=None, 
            min_value=0.0, 
            step=0.5, 
            format="%.1f",
            help="اترك فاضي إذا لم توجد أدراج"
        )
        drawer_depth = col_dr3.number_input(
            "📐 **عمق الدرج (سم)**", 
            value=None, 
            min_value=0.0, 
            step=0.5, 
            format="%.1f",
            help="اترك فاضي إذا لم توجد أدراج"
        )

        st.markdown("### ➕ **إضافات اختيارية**")
        col_e1, col_e2, col_e3 = st.columns(3)
        extra_vertical = col_e1.number_input(
            "🔽 **أعواد رأسية إضافية**", 
            value=None, 
            min_value=0, 
            step=1, 
            format="%d",
            help="عدد الأعواد الرأسية الإضافية"
        )
        extra_horizontal = col_e2.number_input(
            "➡️ **أعواد أفقية إضافية**", 
            value=None, 
            min_value=0, 
            step=1, 
            format="%d",
            help="عدد الأعواد الأفقية الإضافية"
        )
        extra_length = col_e3.number_input(
            "📏 **طول العود الإضافي (سم)**", 
            value=None, 
            min_value=0.0, 
            step=0.5, 
            format="%.1f",
            help="طول الأعواد الإضافية"
        )

        st.markdown("---")
        submit_btn = st.form_submit_button(
            "🔨 **حسّب كل شيء وأضف للجرد**", 
            use_container_width=True, 
            type="primary"
        )

    # ===== معالجة الحسابات الكاملة =====
    if submit_btn:
        if width is not None and height is not None and depth is not None:
            # منع التكرار
            unit_id = f"{client_name or 'غير محدد'}_{width:.1f}_{height:.1f}_{depth:.1f}"
            if st.session_state.last_unit_id != unit_id:
                
                # حساب المقاسات النهائية
                final_height = height - (13 if unit_type in ["وحدة سفلية", "دولاب خزينة"] else 5)
                final_width = width - 5
                final_depth = depth - 5
                
                # قوائم الألمنيوم والفيبر
                alum_items = []
                fiber_items = []
                
                # ===== الألمنيوم الأساسي =====
                alum_items.extend([
                    {"name": "ارتفاع رئيسي", "length": final_height, "count": 2, "type": "مفرد"},
                    {"name": "ارتفاع متقارب", "length": final_height, "count": 2, "type": "متقارب"}
                ])
                
                if unit_type == "وحدة سفلية":
                    alum_items.extend([
                        {"name": "عرض أمامي", "length": final_width, "count": 3, "type": "مفرد"},
                        {"name": "عرض خلفي", "length": final_width, "count": 1, "type": "متقارب"},
                        {"name": "عمق أمامي", "length": final_depth, "count": 2, "type": "مفرد"},
                        {"name": "عمق خلفي", "length": final_depth, "count": 2, "type": "متقارب"}
                    ])
                else:
                    alum_items.extend([
                        {"name": "عرض جانبي", "length": final_width, "count": 2, "type": "مفرد"},
                        {"name": "عرض متقارب", "length": final_width, "count": 2, "type": "متقارب"},
                        {"name": "عمق متقارب", "length": final_depth, "count": 
