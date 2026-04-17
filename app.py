import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات النظام والتنسيق (CSS)
# ==========================================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

# منع تكرار الأرقام العشرية الطويلة في الجداول (تنظيف 0.0000)
def clean_num(df):
    return df.map(lambda x: f"{x:g}" if isinstance(x, (int, float)) else x)

# تهيئة مخزن البيانات في الذاكرة
if "project_list" not in st.session_state:
    st.session_state.project_list = []

if "page" not in st.session_state:
    st.session_state.page = "home"

# ==========================================
# 2. الصفحة الرئيسية
# ==========================================
if st.session_state.page == "home":
    st.markdown("""
        <div style='text-align:center;margin-top:10%;'>
            <h1 style='color:#f1c40f; font-size: 3em;'>ضجة سمارت</h1>
            <h2 style='color:#ffffff;'>نظام التخصيم والجرد الشامل</h2>
            <p style='color:#bdc3c7; font-size: 1.2em;'>دقة، سرعة، احترافية</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🚀 ابدأ العمل على مشروع جديد", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()

# ==========================================
# 3. صفحة الفاتورة (الجرد النهائي والأسعار)
# ==========================================
elif st.session_state.page == "invoice":
    st.title("📄 فاتورة خامات المشروع")
    
    col_nav1, col_nav2 = st.columns([1, 5])
    if col_nav1.button("⬅️ رجوع"):
        st.session_state.page = "calc"
        st.rerun()

    # حساب إجمالي الكميات من قائمة المشاريع
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

    # جدول الفاتورة (إكسيل)
    if "df_invoice" not in st.session_state:
        st.session_state.df_invoice = pd.DataFrame([
            {"البيان": "أعواد ألمنيوم (مفرد)", "العدد": qty_m, "سعر الوحدة": 0.0},
            {"البيان": "أعواد ألمنيوم (متقارب)", "العدد": qty_t, "سعر الوحدة": 0.0},
            {"البيان": "ألواح فيبر", "العدد": qty_f, "سعر الوحدة": 0.0},
        ])

    st.markdown("### ✏️ تحرير بنود الفاتورة والأسعار")
    edited_df = st.data_editor(
        st.session_state.df_invoice,
        column_config={
            "البيان": st.column_config.TextColumn("الصنف", width="large"),
            "العدد": st.column_config.NumberColumn("الكمية", format="%.2f"),
            "سعر الوحدة": st.column_config.NumberColumn("السعر", format="%.2f"),
        },
        num_rows="dynamic",
        use_container_width=True,
        key="main_invoice_editor"
    )
    
    edited_df["الإجمالي"] = edited_df["العدد"] * edited_df["سعر الوحدة"]
    
    st.markdown("---")
    st.markdown("### 📊 معاينة الفاتورة")
    st.table(clean_num(edited_df))

    total_bill = edited_df["الإجمالي"].sum()
    st.markdown(f"""
        <div style='text-align:right; background-color:#1e272e; padding:20px; border-right: 10px solid #2ecc71;'>
            <h1 style='color:#2ecc71; margin:0;'>💰 الإجمالي الكلي: {total_bill:,.2f} جنيه</h1>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 4. صفحة التخصيم (الكود الكامل 250+ سطر)
# ==========================================
else:
    st.title("🛠️ تخصيم الوحدات")
    
    if st.button("🏠 العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    # --- نموذج الإدخال (Form) لمنع التكرار ---
    with st.form(key="master_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        client = c1.text_input("👤 اسم العميل / المشروع")
        unit_type = c2.selectbox("📦 نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

        st.markdown("#### 📏 المقاسات الأساسية")
        d1, d2, d3 = st.columns(3)
        # استخدام value=None لإزالة 0.00
        W = d1.number_input("العرض الكلي (W)", value=None)
        H = d2.number_input("الارتفاع الكلي (H)", value=None)
        D = d3.number_input("العمق الكلي (D)", value=None)

        st.markdown("#### 📏 تخصيم الأرفف")
        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.number_input("عدد الأرفف", value=None)
        sh_w = sh2.number_input("عرض الرف", value=None)
        sh_d = sh3.number_input("عمق الرف", value=None)

        st.markdown("#### 📏 تخصيم الفواصل")
        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", value=None)
        v_h = v2.number_input("ارتفاع الفاصل", value=None)
        v_d = v3.number_input("عمق الفاصل", value=None)

        st.markdown("#### 📏 تخصيم الأدراج")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", value=None)
        dr_w = dr2.number_input("عرض الدرج", value=None)
        dr_d = dr3.number_input("عمق الدرج", value=None)

        # زر التخصيم
        calculate_btn = st.form_submit_button("🔨 تنفيذ التخصيم وإضافة للجرد")

    # --- منطق التخصيم البرمجي ---
    if calculate_btn:
        if W and H and D:
            # 1. معادلات خصم الهيكل
            h_f = H - (13 if unit_type in ["وحدة سفلية", "دولاب خزين"] else 5)
            w_f = W - 5
            d_f = D - 5

            temp_alum = []
            temp_fiber = []

            # 2. ألمنيوم الهيكل
            if unit_type == "وحدة سفلية":
                temp_alum = [
                    ["ارتفاع", h_f, 2, "مفرد"], ["ارتفاع", h_f, 2, "متقارب"],
                    ["عرض", w_f, 3, "مفرد"], ["عرض", w_f, 1, "متقارب"],
                    ["عمق", d_f, 2, "مفرد"], ["عمق", d_f, 2, "متقارب"]
                ]
            else:
                temp_alum = [
                    ["ارتفاع", h_f, 2, "مفرد"], ["ارتفاع", h_f, 2, "متقارب"],
                    ["عرض", w_f, 2, "مفرد"], ["عرض", w_f, 2, "متقارب"],
                    ["عمق", d_f, 0, "مفرد"], ["عمق", d_f, 4, "متقارب"]
                ]

            # 3. حسابات الأرفف
            if sh_n and sh_n > 0:
                temp_alum.append(["رف عرض", sh_w, sh_n * 2, "مفرد"])
                temp_alum.append(["رف عمق", sh_d, sh_n * 2, "مفرد"])
                temp_fiber.append(["لوح رف", sh_w - 5, sh_d - 5, sh_n])

            # 4. حسابات الفواصل (إضافة عمق الفاصل)
            if v_n and v_n > 0:
                temp_alum.append(["فاصل ارتفاع", v_h, v_n * 2, "مفرد"])
                temp_alum.append(["فاصل عمق", v_d, v_n * 2, "مفرد"]) # البند المطلوب
                temp_fiber.append(["لوح فاصل", v_h - 5, v_d - 5, v_n])

            # 5. حسابات الأدراج (إضافة عرض وعمق الدرج)
            if dr_n and dr_n > 0:
                temp_alum.append(["درج عرض", dr_w - 2.5, dr_n * 2, "2x8"])
                temp_alum.append(["درج عمق", dr_d, dr_n * 2, "2x8"]) # البند المطلوب
                temp_fiber.append(["لوح درج", dr_w, dr_d, dr_n])

            # 6. فيبر الهيكل
            temp_fiber += [
                ["ضهرية", w_f, h_f, 1],
                ["أرضية", w_f, d_f, 1],
                ["أجناب", h_f, d_f, 2]
            ]

            # إضافة المشروع للقائمة ومنع التكرار
            st.session_state.project_list.append({
                "client": client,
                "unit_type": unit_type,
                "alum": temp_alum,
                "fiber": temp_fiber
            })
            
            # تحديث الفاتورة
            if "df_invoice" in st.session_state:
                del st.session_state.df_invoice
                
            st.success(f"✅ تم إضافة {unit_type} - {client}")
            st.rerun()
        else:
            st.warning("⚠️ لا يمكن التخصيم بدون إدخال المقاسات الأساسية (W, H, D)")

    # --- عرض النتائج والجرد ---
    if st.session_state.project_list:
        st.markdown("---")
        if st.button("📄 الانتقال للفاتورة النهائية", use_container_width=True, type="primary"):
            st.session_state.page = "invoice"
            st.rerun()
        
        if st.button("🗑️ مسح كافة الوحدات"):
            st.session_state.project_list = []
            if "df_invoice" in st.session_state: del st.session_state.df_invoice
            st.rerun()

        for unit in st.session_state.project_list:
            with st.expander(f"📦 تفاصيل: {unit['unit_type']} - العميل: {unit['client']}"):
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.subheader("🛠️ أعواد الألمنيوم")
                    st.table(clean_num(pd.DataFrame(unit["alum"], columns=["بيان", "مقاس", "عدد", "نوع"])))
                with col_res2:
                    st.subheader("🖼️ ألواح الفيبر")
                    st.table(clean_num(pd.DataFrame(unit["fiber"], columns=["بيان", "عرض", "ارتفاع", "عدد"])))
