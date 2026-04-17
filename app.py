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
