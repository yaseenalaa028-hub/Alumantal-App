import streamlit as st
import pandas as pd

# =========================
# إعداد التطبيق
# =========================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

# =========================
# Session State
# =========================
if "project_list" not in st.session_state:
    st.session_state.project_list = []
import streamlit as st
import pandas as pd

# =========================
# إعداد التطبيق
# =========================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

# =========================
# Session State
# =========================
if "project_list" not in st.session_state:
    st.session_state.project_list = []

if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================
# الصفحة الرئيسية
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
# صفحة الفاتورة (جدول إكسيل تفاعلي)
# =========================
elif st.session_state.page == "invoice":
    st.title("📄 فاتورة الخامات")

    if st.button("⬅️ رجوع للتخصيم"):
        st.session_state.page = "calc"
        st.rerun()

    # حساب الجرد التلقائي
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

    # تجهيز بيانات الجدول
    if "df_invoice" not in st.session_state or not st.session_state.project_list:
        initial_data = [
            {"البيان": "أعواد ألمنيوم (مفرد)", "العدد": qty_m, "سعر الوحدة": 0.0},
            {"البيان": "أعواد ألمنيوم (متقارب)", "العدد": qty_t, "سعر الوحدة": 0.0},
            {"البيان": "ألواح فيبر", "العدد": qty_f, "سعر الوحدة": 0.0},
        ]
        st.session_state.df_invoice = pd.DataFrame(initial_data)

    st.markdown("### 📝 جدول الفاتورة (أضف خامات أو عدل الأسعار)")
    
    # الجدول التفاعلي
    edited_df = st.data_editor(
        st.session_state.df_invoice,
        column_config={
            "البيان": st.column_config.TextColumn("البيان", width="large"),
            "العدد": st.column_config.NumberColumn("العدد/الكمية", format="%.2f"),
            "سعر الوحدة": st.column_config.NumberColumn("سعر الوحدة", format="%.2f"),
        },
        num_rows="dynamic",
        use_container_width=True,
        key="invoice_editor"
    )

    # حساب الإجماليات لكل سطر
    edited_df["الإجمالي"] = edited_df["العدد"] * edited_df["سعر الوحدة"]
    
    st.markdown("---")
    st.dataframe(edited_df, use_container_width=True)

    total_sum = edited_df["الإجمالي"].sum()
    st.success(f"### 💰 الإجمالي الكلي: {total_sum:,.2f} جنية")

# =========================
# صفحة التخصيم (رجوع الخانات بالكامل)
# =========================
else:
    st.title("🛠️ التخصيم وإضافة الوحدات")

    if st.button("🏠 الرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    with st.form("main_form"):
        c1, c2 = st.columns(2)
        client = c1.text_input("اسم العميل")
        unit_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

        d1, d2, d3 = st.columns(3)
        W = d1.number_input("العرض", min_value=0.0)
        H = d2.number_input("الارتفاع", min_value=0.0)
        D = d3.number_input("العمق", min_value=0.0)

        st.markdown("---")
        # رجوع خانات الأرفف
        st.markdown("### 🔹 الأرفف")
        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.number_input("عدد الأرفف", min_value=0, step=1)
        sh_w = sh2.number_input("عرض الرف", min_value=0.0)
        sh_d = sh3.number_input("عمق الرف", min_value=0.0)

        # رجوع خانات الفواصل
        st.markdown("### 🔹 الفواصل")
        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", min_value=0, step=1)
        v_h = v2.number_input("ارتفاع الفاصل", min_value=0.0)
        v_d = v3.number_input("عمق الفاصل", min_value=0.0)

        # رجوع خانات الأدراج
        st.markdown("### 🔹 الأدراج")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", min_value=0, step=1)
        dr_w = dr2.number_input("عرض الدرج", min_value=0.0)
        dr_d = dr3.number_input("عمق الدرج", min_value=0.0)

        submit = st.form_submit_button("حساب وإضافة للجرد")

    if submit and W > 0:
        h_final = H - (13 if unit_type in ["وحدة سفلية", "دولاب خزين"] else 5)
        w_final = W - 5
        d_final = D - 5

        alum = []
        fiber = []

        # الحسابات الأساسية للوحدة
        if unit_type == "وحدة سفلية":
            alum += [["ارتفاع", h_final, 2, "مفرد"], ["ارتفاع", h_final, 2, "متقارب"],
                     ["عرض", w_final, 3, "مفرد"], ["عرض", w_final, 1, "متقارب"],
                     ["عمق", d_final, 2, "مفرد"], ["عمق", d_final, 2, "متقارب"]]
        else:
            alum += [["ارتفاع", h_final, 2, "مفرد"], ["ارتفاع", h_final, 2, "متقارب"],
                     ["عرض", w_final, 2, "مفرد"], ["عرض", w_final, 2, "متقارب"],
                     ["عمق", d_final, 0, "مفرد"], ["عمق", d_final, 4, "متقارب"]]

        # حساب الأرفف
        if sh_n > 0:
            alum.append(["رف عرض", sh_w, sh_n * 2, "مفرد"])
            alum.append(["رف عمق", sh_d, sh_n * 2, "مفرد"])
            fiber.append(["رف", sh_w - 5, sh_d - 5, sh_n])

        # حساب الفواصل
        if v_n > 0:
            alum.append(["فواصل", v_h, v_n * 2, "مفرد"])
            fiber.append(["فاصل", v_h - 5, v_d - 5, v_n])

        # حساب الأدراج
        if dr_n > 0:
            alum.append(["درج", dr_w - 2.5, dr_n * 2, "2x8"])
            fiber.append(["درج", dr_w, dr_d, dr_n])

        # حساب الهيكل
        fiber += [["ضهرية", w_final, h_final, 1], ["أرضية", w_final, d_final, 1], ["أجناب", h_final, d_final, 2]]

        st.session_state.project_list.append({
            "client": client, "unit_type": unit_type, "alum": alum, "fiber": fiber
        })
        if "df_invoice" in st.session_state: del st.session_state.df_invoice
        st.success(f"تم إضافة {unit_type} بنجاح!")

    # أزرار العرض
    if st.session_state.project_list:
        st.markdown("---")
        if st.button("📄 فتح الفاتورة النهائية", use_container_width=True, type="primary"):
            st.session_state.page = "invoice"
            st.rerun()
        
        for unit in st.session_state.project_list:
            with st.expander(f"📦 {unit['unit_type']} - {unit['client']}"):
                st.table(pd.DataFrame(unit["alum"], columns=["بيان", "مقاس", "عدد", "نوع"]))
                st.table(pd.DataFrame(unit["fiber"], columns=["بيان", "عرض", "ارتفاع", "عدد"]))
if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================
# الصفحة الرئيسية
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
# صفحة الفاتورة (المعدلة)
# =========================
elif st.session_state.page == "invoice":
    st.title("📄 فاتورة الخامات الإجمالية")

    if st.button("⬅️ رجوع"):
        st.session_state.page = "calc"
        st.rerun()

    if not st.session_state.project_list:
        st.warning("لا توجد بيانات جرد لإصدار فاتورة")
    else:
        # حساب إجمالي الجرد من البيانات الحالية
        total_m = 0
        total_t = 0
        total_f = 0

        for u in st.session_state.project_list:
            for a in u["alum"]:
                if a[3] == "مفرد":
                    total_m += a[1] * a[2]
                else:
                    total_t += a[1] * a[2]
            for f in u["fiber"]:
                total_f += f[1] * f[2] * f[3]

        # تحويل الجرد لوحدات (أعواد وألواح)
        qty_m = round(total_m / 600, 2)
        qty_t = round(total_t / 600, 2)
        qty_f = round(total_f / (280*130), 2)

        # تجهيز بيانات الجدول (الفاتورة)
        invoice_data = [
            {"النوع": "أعواد ألمنيوم (مفرد)", "الكمية": qty_m, "سعر الوحدة": 0.0},
            {"النوع": "أعواد ألمنيوم (متقارب)", "الكمية": qty_t, "سعر الوحدة": 0.0},
            {"النوع": "ألواح فيبر", "الكمية": qty_f, "سعر الوحدة": 0.0},
        ]

        df_invoice = pd.DataFrame(invoice_data)

        st.markdown("### ✏️ جدول الفاتورة (يمكنك تعديل الأسعار مباشرة)")
        st.info("اضغط مرتين على خانة 'سعر الوحدة' لتعديل السعر")

        # عرض الجدول بصيغة قابلة للتعديل (مثل الإكسيل)
        edited_df = st.data_editor(
            df_invoice,
            column_config={
                "النوع": st.column_config.TextColumn("الصنف", disabled=True),
                "الكمية": st.column_config.NumberColumn("الكمية المطلوبة", disabled=True),
                "سعر الوحدة": st.column_config.NumberColumn("سعر الوحدة (جنية)", min_value=0, format="%.2f"),
            },
            hide_index=True,
            use_container_width=True,
            key="invoice_editor"
        )

        # حساب الإجمالي
        edited_df["الإجمالي"] = edited_df["الكمية"] * edited_df["سعر الوحدة"]
        grand_total = edited_df["الإجمالي"].sum()

        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"### 💰 إجمالي الفاتورة: `{grand_total:,.2f}` جنية")
        
        # زر إضافي لمسح البيانات والبدء من جديد
        if st.button("🗑️ مسح جميع البيانات والبدء من جديد", color="red"):
            st.session_state.project_list = []
            st.session_state.page = "home"
            st.rerun()

# =========================
# صفحة التخصيم
# =========================
else:
    st.title("🛠️ التخصيم")

    if st.button("🏠 الصفحة الرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    with st.form("form"):
        c1, c2 = st.columns(2)
        client = c1.text_input("اسم العميل", key="client")
        unit_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"], key="type")

        d1, d2, d3 = st.columns(3)
        W = d1.number_input("العرض", key="W")
        H = d2.number_input("الارتفاع", key="H")
        D = d3.number_input("العمق", key="D")

        st.markdown("### الأرفف والأدراج")
        sh1, sh2 = st.columns(2)
        sh_n = sh1.number_input("عدد الأرفف", min_value=0, step=1)
        dr_n = sh2.number_input("عدد الأدراج", min_value=0, step=1)

        # قيم افتراضية للأرفف والأدراج لتسهيل الكود
        sh_w = W - 5; sh_d = D - 5
        dr_w = W - 5; dr_d = D - 5
        v_n = 0; v_h = 0; v_d = 0

        submit = st.form_submit_button("حساب وإضافة للجرد")

    if submit and W > 0 and H > 0 and D > 0:
        h_final = H - (13 if unit_type in ["وحدة سفلية", "دولاب خزين"] else 5)
        w_final = W - 5
        d_final = D - 5

        alum = []
        fiber = []

        if unit_type == "وحدة سفلية":
            alum += [
                ["ارتفاع", h_final, 2, "مفرد"], ["ارتفاع", h_final, 2, "متقارب"],
                ["عرض", w_final, 3, "مفرد"], ["عرض", w_final, 1, "متقارب"],
                ["عمق", d_final, 2, "مفرد"], ["عمق", d_final, 2, "متقارب"],
            ]
        else:
            alum += [
                ["ارتفاع", h_final, 2, "مفرد"], ["ارتفاع", h_final, 2, "متقارب"],
                ["عرض", w_final, 2, "مفرد"], ["عرض", w_final, 2, "متقارب"],
                ["عمق", d_final, 0, "مفرد"], ["عمق", d_final, 4, "متقارب"],
            ]

        if sh_n > 0:
            alum.append(["رف عرض", sh_w, sh_n * 2, "مفرد"])
            alum.append(["رف عمق", sh_d, sh_n * 2, "مفرد"])
            fiber.append(["رف", sh_w - 5, sh_d - 5, sh_n])

        if dr_n > 0:
            alum.append(["درج", dr_w - 2.5, dr_n * 2, "2x8"])
            fiber.append(["درج", dr_w, dr_d, dr_n])

        fiber += [
            ["ضهرية", w_final, h_final, 1],
            ["أرضية", w_final, d_final, 1],
            ["أجناب", h_final, d_final, 2],
        ]

        st.session_state.project_list.append({
            "client": client,
            "unit_type": unit_type,
            "alum": alum,
            "fiber": fiber
        })
        st.success(f"تم إضافة {unit_type} للعميل {client} بنجاح!")

    # =========================
    # عرض الجرد والأزرار
    # =========================
    if st.session_state.project_list:
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📄 فتح فاتورة الخامات النهائية", use_container_width=True, type="primary"):
                st.session_state.page = "invoice"
                st.rerun()
        
        with col_btn2:
            if st.button("🗑️ مسح الكل", use_container_width=True):
                st.session_state.project_list = []
                st.rerun()

        # عرض تفاصيل الوحدات المضافة
        for i, unit in enumerate(st.session_state.project_list):
            with st.expander(f"تفاصيل: {unit['unit_type']} - {unit['client']}"):
                st.table(pd.DataFrame(unit["alum"], columns=["بيان", "مقاس", "عدد", "نوع"]))
                st.table(pd.DataFrame(unit["fiber"], columns=["بيان", "عرض", "ارتفاع", "عدد"]))
