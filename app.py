import streamlit as st
import pandas as pd

# =========================
# 1. إعداد التطبيق
# =========================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

# تهيئة مخزن البيانات (Session State)
if "project_list" not in st.session_state:
    st.session_state.project_list = []

if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================
# 2. الصفحة الرئيسية
# =========================
if st.session_state.page == "home":
    st.markdown("""
        <div style='text-align:center;margin-top:10%;'>
            <h1 style='color:#f1c40f;'>ضجة سمارت</h1>
            <h4>نحو دقة أعلى في شغل المطابخ 👌</h4>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 ابدأ التخصيم", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()

# =========================
# 3. صفحة الفاتورة (الجدول التفاعلي)
# =========================
elif st.session_state.page == "invoice":
    st.title("📄 فاتورة الخامات النهائية")

    if st.button("⬅️ رجوع للتخصيم"):
        st.session_state.page = "calc"
        st.rerun()

    # حساب إجمالي الجرد تلقائياً من الوحدات المضافة
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

    # إنشاء بيانات الجدول الأولية (لو مش موجودة)
    if "df_invoice" not in st.session_state or not st.session_state.project_list:
        initial_data = [
            {"البيان": "أعواد ألمنيوم (مفرد)", "العدد": qty_m, "سعر الوحدة": 0.0},
            {"البيان": "أعواد ألمنيوم (متقارب)", "العدد": qty_t, "سعر الوحدة": 0.0},
            {"البيان": "ألواح فيبر", "العدد": qty_f, "سعر الوحدة": 0.0},
        ]
        st.session_state.df_invoice = pd.DataFrame(initial_data)

    st.markdown("### ✏️ جدول الفاتورة (إكسيل)")
    st.info("يمكنك تعديل الأسعار، أو إضافة صفوف جديدة لأي خامات إضافية في نهاية الجدول.")

    # عرض الجدول كإكسيل تفاعلي (يسمح بإضافة صفوف num_rows="dynamic")
    edited_df = st.data_editor(
        st.session_state.df_invoice,
        column_config={
            "البيان": st.column_config.TextColumn("البيان", width="large"),
            "العدد": st.column_config.NumberColumn("العدد / الكمية", format="%.2f"),
            "سعر الوحدة": st.column_config.NumberColumn("سعر الوحدة", format="%.2f"),
        },
        num_rows="dynamic",
        use_container_width=True,
        key="invoice_editor"
    )

    # حساب الإجمالي لكل سطر تلقائياً
    edited_df["الإجمالي"] = edited_df["العدد"] * edited_df["سعر الوحدة"]
    
    st.markdown("---")
    # عرض الجدول النهائي مع خانة الإجمالي المحسوبة
    st.table(edited_df)

    # حساب الإجمالي الكلي للفاتورة
    grand_total = edited_df["الإجمالي"].sum()
    st.markdown(f"""
        <div style='text-align:right; background-color:#1e272e; padding:20px; border-radius:10px; border: 2px solid #2ecc71;'>
            <h2 style='color:#2ecc71; margin:0;'>💰 إجمالي الفاتورة النهائي: {grand_total:,.2f} جنية</h2>
        </div>
    """, unsafe_allow_html=True)

# =========================
# 4. صفحة التخصيم (الخانات كاملة)
# =========================
else:
    st.title("🛠️ تخصيم الوحدات")

    if st.button("🏠 الرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    with st.form("main_form"):
        # البيانات الأساسية
        c1, c2 = st.columns(2)
        client = c1.text_input("اسم العميل")
        unit_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

        d1, d2, d3 = st.columns(3)
        W = d1.number_input("عرض الوحدة الكلي (W)", min_value=0.0)
        H = d2.number_input("ارتفاع الوحدة الكلي (H)", min_value=0.0)
        D = d3.number_input("عمق الوحدة الكلي (D)", min_value=0.0)

        st.markdown("---")
        # خانات الأرفف
        st.markdown("### 🔹 الأرفف")
        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.number_input("عدد الأرفف", min_value=0, step=1)
        sh_w = sh2.number_input("عرض الرف", min_value=0.0)
        sh_d = sh3.number_input("عمق الرف", min_value=0.0)

        # خانات الفواصل
        st.markdown("### 🔹 الفواصل")
        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", min_value=0, step=1)
        v_h = v2.number_input("ارتفاع الفاصل", min_value=0.0)
        v_d = v3.number_input("عمق الفاصل", min_value=0.0)

        # خانات الأدراج
        st.markdown("### 🔹 الأدراج")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", min_value=0, step=1)
        dr_w = dr2.number_input("عرض الدرج", min_value=0.0)
        dr_d = dr3.number_input("عمق الدرج", min_value=0.0)

        submit = st.form_submit_button("إضافة الوحدة للجرد")

    if submit and W > 0:
        # معادلات الخصم الأساسية
        h_final = H - (13 if unit_type in ["وحدة سفلية", "دولاب خزين"] else 5)
        w_final = W - 5
        d_final = D - 5

        alum = []
        fiber = []

        # تخصيم الهيكل الأساسي
        if unit_type == "وحدة سفلية":
            alum += [["ارتفاع", h_final, 2, "مفرد"], ["ارتفاع", h_final, 2, "متقارب"],
                     ["عرض", w_final, 3, "مفرد"], ["عرض", w_final, 1, "متقارب"],
                     ["عمق", d_final, 2, "مفرد"], ["عمق", d_final, 2, "متقارب"]]
        else:
            alum += [["ارتفاع", h_final, 2, "مفرد"], ["ارتفاع", h_final, 2, "متقارب"],
                     ["عرض", w_final, 2, "مفرد"], ["عرض", w_final, 2, "متقارب"],
                     ["عمق", d_final, 0, "مفرد"], ["عمق", d_final, 4, "متقارب"]]

        # تخصيم الأرفف
        if sh_n > 0:
            alum.append(["رف عرض", sh_w, sh_n * 2, "مفرد"])
            alum.append(["رف عمق", sh_d, sh_n * 2, "مفرد"])
            fiber.append(["رف", sh_w - 5, sh_d - 5, sh_n])

        # تخصيم الفواصل
        if v_n > 0:
            alum.append(["فواصل", v_h, v_n * 2, "مفرد"])
            fiber.append(["فاصل", v_h - 5, v_d - 5, v_n])

        # تخصيم الأدراج
        if dr_n > 0:
            alum.append(["درج", dr_w - 2.5, dr_n * 2, "2x8"])
            fiber.append(["درج", dr_w, dr_d, dr_n])

        # إضافة الضهرية والأرضية والأجناب
        fiber += [["ضهرية", w_final, h_final, 1], ["أرضية", w_final, d_final, 1], ["أجناب", h_final, d_final, 2]]

        # حفظ الوحدة في القائمة
        st.session_state.project_list.append({
            "client": client, "unit_type": unit_type, "alum": alum, "fiber": fiber
        })
        
        # مسح الفاتورة القديمة لتحديثها بالبيانات الجديدة
        if "df_invoice" in st.session_state:
            del st.session_state.df_invoice
            
        st.success(f"✅ تم إضافة {unit_type} للعميل {client}")

    # أزرار الانتقال
    if st.session_state.project_list:
        st.markdown("---")
        if st.button("📄 فتح فاتورة الخامات النهائية", use_container_width=True, type="primary"):
            st.session_state.page = "invoice"
            st.rerun()
        
        if st.button("🗑️ مسح جميع البيانات"):
            st.session_state.project_list = []
            if "df_invoice" in st.session_state: del st.session_state.df_invoice
            st.rerun()

        # عرض تفاصيل كل وحدة بشكل منظم
        for i, unit in enumerate(st.session_state.project_list):
            with st.expander(f"📦 تفاصيل {unit['unit_type']} - {unit['client']}"):
                st.write("**الألمنيوم:**")
                st.table(pd.DataFrame(unit["alum"], columns=["بيان", "مقاس", "عدد", "نوع"]))
                st.write("**الفيبر:**")
                st.table(pd.DataFrame(unit["fiber"], columns=["بيان", "عرض", "ارتفاع", "عدد"]))
