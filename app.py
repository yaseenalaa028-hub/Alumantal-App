import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات الصفحة والتنسيق
# ==========================================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

# تهيئة مخزن البيانات
if "project_list" not in st.session_state:
    st.session_state.project_list = []

if "page" not in st.session_state:
    st.session_state.page = "home"

# وظيفة لتنظيف الأرقام من الأصفار الزائدة (للعرض فقط) لتبدو 2 بدلاً من 2.0000
def clean_num(df):
    return df.map(lambda x: f"{x:g}" if isinstance(x, (int, float)) else x)

# ==========================================
# 2. الصفحة الرئيسية
# ==========================================
if st.session_state.page == "home":
    st.markdown("""
        <div style='text-align:center;margin-top:10%;'>
            <h1 style='color:#f1c40f;'>ضجة سمارت</h1>
            <h2 style='color:#ffffff;'>نظام تخصيم المطابخ الاحترافي</h2>
            <h4 style='color:#bdc3c7;'>نحو دقة أعلى في التنفيذ 👌</h4>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🚀 ابدأ العمل الآن", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()

# ==========================================
# 3. صفحة الفاتورة (إكسيل تفاعلي)
# ==========================================
elif st.session_state.page == "invoice":
    st.title("📄 فاتورة خامات المشروع")
    
    if st.button("⬅️ العودة للتخصيم"):
        st.session_state.page = "calc"
        st.rerun()

    # حساب الجرد الإجمالي من قائمة المشاريع
    total_m = 0; total_t = 0; total_f = 0
    for u in st.session_state.project_list:
        for a in u["alum"]:
            if a[3] == "مفرد": total_m += a[1] * a[2]
            else: total_t += a[1] * a[2]
        for f in u["fiber"]:
            total_f += f[1] * f[2] * f[3]

    qty_m = round(total_m / 600, 2)
    qty_t = round(total_t / 600, 2)
    qty_f = round(total_f / (280*130), 2)

    # إنشاء أو استدعاء جدول الفاتورة
    if "df_invoice" not in st.session_state:
        st.session_state.df_invoice = pd.DataFrame([
            {"البيان": "أعواد ألمنيوم (مفرد)", "العدد": qty_m, "سعر الوحدة": 0.0},
            {"البيان": "أعواد ألمنيوم (متقارب)", "العدد": qty_t, "سعر الوحدة": 0.0},
            {"البيان": "ألواح فيبر", "العدد": qty_f, "سعر الوحدة": 0.0},
        ])

    st.info("💡 يمكنك إضافة بنود جديدة (مقابض، مفصلات...) في نهاية الجدول")
    
    # محرر البيانات التفاعلي (إكسيل)
    edited_df = st.data_editor(
        st.session_state.df_invoice,
        column_config={
            "البيان": st.column_config.TextColumn("الصنف / البيان", width="large"),
            "العدد": st.column_config.NumberColumn("الكمية", format="%.2f"),
            "سعر الوحدة": st.column_config.NumberColumn("السعر", format="%.2f"),
        },
        num_rows="dynamic",
        use_container_width=True,
        key="main_inv_editor"
    )
    
    # حساب الإجماليات
    edited_df["إجمالي الصنف"] = edited_df["العدد"] * edited_df["سعر الوحدة"]
    
    st.markdown("---")
    st.markdown("### 📊 عرض الفاتورة النهائي")
    # عرض الجدول النظيف
    st.table(clean_num(edited_df))

    grand_total = edited_df["إجمالي الصنف"].sum()
    st.markdown(f"""
        <div style='text-align:right; background-color:#1e272e; padding:15px; border-left: 5px solid #2ecc71;'>
            <h2 style='color:#2ecc71; margin:0;'>💰 الإجمالي الكلي للفاتورة: {grand_total:,.2f} جنيه</h2>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. صفحة التخصيم (الكود الكامل)
# ==========================================
else:
    st.title("🛠️ تخصيم وإضافة وحدات")
    
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    # --- نموذج الإدخال ---
    with st.form("main_entry_form"):
        c1, c2 = st.columns(2)
        client = c1.text_input("👤 اسم العميل / المشروع")
        unit_type = c2.selectbox("📦 نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

        d1, d2, d3 = st.columns(3)
        W = d1.number_input("العرض الكلي (W)", value=None)
        H = d2.number_input("الارتفاع الكلي (H)", value=None)
        D = d3.number_input("العمق الكلي (D)", value=None)

        st.markdown("#### 📏 ملحقات الأرفف")
        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.number_input("عدد الأرفف", value=None)
        sh_w = sh2.number_input("عرض الرف", value=None)
        sh_d = sh3.number_input("عمق الرف", value=None)

        st.markdown("#### 📏 ملحقات الفواصل")
        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", value=None)
        v_h = v2.number_input("ارتفاع الفاصل", value=None)
        v_d = v3.number_input("عمق الفاصل", value=None)

        st.markdown("#### 📏 ملحقات الأدراج")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", value=None)
        dr_w = dr2.number_input("عرض الدرج", value=None)
        dr_d = dr3.number_input("عمق الدرج", value=None)

        submit = st.form_submit_button("🔨 تخصيم وإضافة للعملية")

    # --- منطق التخصيم ---
    if submit and W and H and D:
        # حسابات الهيكل
        h_final = H - (13 if unit_type in ["وحدة سفلية", "دولاب خزين"] else 5)
        w_final = W - 5
        d_final = D - 5

        alum = []
        fiber = []

        # 1. تخصيم الألمنيوم الأساسي
        if unit_type == "وحدة سفلية":
            alum += [
                ["ارتفاع", h_final, 2, "مفرد"], ["ارتفاع", h_final, 2, "متقارب"],
                ["عرض", w_final, 3, "مفرد"], ["عرض", w_final, 1, "متقارب"],
                ["عمق", d_final, 2, "مفرد"], ["عمق", d_final, 2, "متقارب"]
            ]
        else: # علوية أو خزين
            alum += [
                ["ارتفاع", h_final, 2, "مفرد"], ["ارتفاع", h_final, 2, "متقارب"],
                ["عرض", w_final, 2, "مفرد"], ["عرض", w_final, 2, "متقارب"],
                ["عمق", d_final, 0, "مفرد"], ["عمق", d_final, 4, "متقارب"]
            ]

        # 2. تخصيم الأرفف
        if sh_n and sh_n > 0:
            alum.append(["رف عرض", sh_w, sh_n * 2, "مفرد"])
            alum.append(["رف عمق", sh_d, sh_n * 2, "مفرد"])
            fiber.append(["لوح رف", sh_w - 5, sh_d - 5, sh_n])

        # 3. تخصيم الفواصل
        if v_n and v_n > 0:
            alum.append(["فاصل ارتفاع", v_h, v_n * 2, "مفرد"])
            alum.append(["فاصل عمق", v_d, v_n * 2, "مفرد"])
            fiber.append(["لوح فاصل", v_h - 5, v_d - 5, v_n])

        # 4. تخصيم الأدراج (إضافة عرض وعمق الدرج)
        if dr_n and dr_n > 0:
            alum.append(["درج عرض", dr_w - 2.5, dr_n * 2, "2x8"])
            alum.append(["درج عمق", dr_d, dr_n * 2, "2x8"])
            fiber.append(["لوح درج", dr_w, dr_d, dr_n])

        # 5. تخصيم الفيبر للهيكل
        fiber += [
            ["ضهرية", w_final, h_final, 1],
            ["أرضية", w_final, d_final, 1],
            ["أجناب", h_final, d_final, 2]
        ]

        # حفظ البيانات
        st.session_state.project_list.append({
            "client": client,
            "unit_type": unit_type,
            "alum": alum,
            "fiber": fiber
        })
        
        # تصفير الفاتورة المؤقتة لتحديثها بالبيانات الجديدة
        if "df_invoice" in st.session_state:
            del st.session_state.df_invoice
            
        st.success(f"✅ تم إضافة {unit_type} بنجاح")

    # --- عرض الجرد الحالي ---
    if st.session_state.project_list:
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("📄 الانتقال لحساب الأسعار", use_container_width=True, type="primary"):
                st.session_state.page = "invoice"
                st.rerun()
        with col_btn2:
            if st.button("🗑️ مسح الكل والبدء من جديد", use_container_width=True):
                st.session_state.project_list = []
                if "df_invoice" in st.session_state: del st.session_state.df_invoice
                st.rerun()

        st.markdown("### 📋 تفاصيل الوحدات الحالية")
        for i, unit in enumerate(st.session_state.project_list):
            with st.expander(f"📦 {unit['unit_type']} - العميل: {unit['client']}"):
                st.write("**تخصيم الألمنيوم:**")
                st.table(clean_num(pd.DataFrame(unit["alum"], columns=["بيان", "مقاس", "عدد", "نوع"])))
                st.write("**تخصيم الفيبر:**")
                st.table(clean_num(pd.DataFrame(unit["fiber"], columns=["بيان", "عرض", "ارتفاع", "عدد"])))
