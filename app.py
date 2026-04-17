import streamlit as st
import pandas as pd

# =========================
# إعداد التطبيق
# =========================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

# =========================
# Session
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
# صفحة الفاتورة (الجدول التفاعلي المطلوب)
# =========================
elif st.session_state.page == "invoice":

    st.title("📄 فاتورة الخامات")

    if st.button("⬅️ رجوع"):
        st.session_state.page = "calc"
        st.rerun()

    if not st.session_state.project_list:
        st.warning("لا توجد بيانات")
    else:
        # حساب الجرد الإجمالي للأعواد والفيبر
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

        # تجهيز جدول الفاتورة (إكسيل)
        if "df_invoice" not in st.session_state:
            initial_data = [
                {"البيان": "أعواد ألمنيوم (مفرد)", "العدد": qty_m, "سعر الوحدة": 0.0},
                {"البيان": "أعواد ألمنيوم (متقارب)", "العدد": qty_t, "سعر الوحدة": 0.0},
                {"البيان": "ألواح فيبر", "العدد": qty_f, "سعر الوحدة": 0.0},
            ]
            st.session_state.df_invoice = pd.DataFrame(initial_data)

        st.markdown("### ✏️ إدخال الأسعار (إكسيل)")
        
        edited_df = st.data_editor(
            st.session_state.df_invoice,
            column_config={
                "البيان": st.column_config.TextColumn("البيان", width="large"),
                "العدد": st.column_config.NumberColumn("العدد", format="%.2f"),
                "سعر الوحدة": st.column_config.NumberColumn("سعر الوحدة", format="%.2f"),
            },
            num_rows="dynamic",
            use_container_width=True,
            key="invoice_editor"
        )

        edited_df["الإجمالي"] = edited_df["العدد"] * edited_df["سعر الوحدة"]
        
        st.markdown("### 📊 الفاتورة")
        st.dataframe(edited_df, use_container_width=True)

        st.markdown(f"""
        <h2 style='color:green;'>💰 الإجمالي النهائي: {edited_df['الإجمالي'].sum():.2f}</h2>
        """, unsafe_allow_html=True)

# =========================
# صفحة التخصيم (رجوع الكود الأصلي بالكامل)
# =========================
else:

    st.title("🛠️ التخصيم")

    if st.button("🏠 رجوع"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # الإدخال (مع تعديل value=None لإخفاء 0.00)
    # =========================
    with st.form("form"):

        c1, c2 = st.columns(2)
        client = c1.text_input("اسم العميل", key="client")
        unit_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"], key="type")

        d1, d2, d3 = st.columns(3)
        W = d1.number_input("العرض", key="W", value=None)
        H = d2.number_input("الارتفاع", key="H", value=None)
        D = d3.number_input("العمق", key="D", value=None)

        st.markdown("### الأرفف")
        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.number_input("عدد الأرفف", key="sh_n", value=None)
        sh_w = sh2.number_input("عرض الرف", key="sh_w", value=None)
        sh_d = sh3.number_input("عمق الرف", key="sh_d", value=None)

        st.markdown("### الفواصل")
        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", key="v_n", value=None)
        v_h = v2.number_input("ارتفاع الفاصل", key="v_h", value=None)
        v_d = v3.number_input("عمق الفاصل", key="v_d", value=None)

        st.markdown("### الأدراج")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", key="dr_n", value=None)
        dr_w = dr2.number_input("عرض الدرج", key="dr_w", value=None)
        dr_d = dr3.number_input("عمق الدرج", key="dr_d", value=None)

        submit = st.form_submit_button("حساب")

    # =========================
    # الحساب (كودك الأصلي بنسبة 100%)
    # =========================
    if submit and W and H and D:

        h_final = H - (13 if unit_type in ["وحدة سفلية", "دولاب خزين"] else 5)
        w_final = W - 5
        d_final = D - 5

        alum = []
        fiber = []

        if unit_type == "وحدة سفلية":
            alum += [
                ["ارتفاع", h_final, 2, "مفرد"],
                ["ارتفاع", h_final, 2, "متقارب"],
                ["عرض", w_final, 3, "مفرد"],
                ["عرض", w_final, 1, "متقارب"],
                ["عمق", d_final, 2, "مفرد"],
                ["عمق", d_final, 2, "متقارب"],
            ]
        else:
            alum += [
                ["ارتفاع", h_final, 2, "مفرد"],
                ["ارتفاع", h_final, 2, "متقارب"],
                ["عرض", w_final, 2, "مفرد"],
                ["عرض", w_final, 2, "متقارب"],
                ["عمق", d_final, 0, "مفرد"],
                ["عمق", d_final, 4, "متقارب"],
            ]

        if sh_n and sh_n > 0:
            alum.append(["رف عرض", sh_w, sh_n * 2, "مفرد"])
            alum.append(["رف عمق", sh_d, sh_n * 2, "مفرد"])
            fiber.append(["رف", sh_w - 5, sh_d - 5, sh_n])

        if v_n and v_n > 0:
            alum.append(["فواصل ارتفاع", v_h, v_n * 2, "مفرد"])
            alum.append(["فواصل عمق", v_d, v_n * 2, "مفرد"]) # تعديل: إضافة عمق الفاصل
            fiber.append(["فاصل", v_h - 5, v_d - 5, v_n])

        if dr_n and dr_n > 0:
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
        # مسح الفاتورة لتحديثها بالبيانات الجديدة
        if "df_invoice" in st.session_state:
            del st.session_state.df_invoice

    # =========================
    # عرض الجرد والتفاصيل (كودك الأصلي)
    # =========================
    if st.session_state.project_list:

        total_m = total_t = total_f = 0
        for u in st.session_state.project_list:
            for a in u["alum"]:
                if a[3] == "مفرد": total_m += a[1] * a[2]
                else: total_t += a[1] * a[2]
            for f in u["fiber"]:
                total_f += f[1] * f[2] * f[3]

        st.markdown("## 📊 جرد الخامات")
        st.write(f"🔹 مفرد: {total_m / 600:.2f} عود")
        st.write(f"🔹 متقارب: {total_t / 600:.2f} عود")
        st.write(f"🔹 فيبر: {total_f / (280*130):.2f} لوح")

        if st.button("📄 فتح فاتورة الخامات", use_container_width=True):
            st.session_state.page = "invoice"
            st.rerun()

        for unit in st.session_state.project_list:
            st.markdown(f"### 🏷️ {unit['unit_type']} - {unit['client']}")
            st.table(pd.DataFrame(unit["alum"], columns=["بيان", "مقاس", "عدد", "نوع"]))
            st.table(pd.DataFrame(unit["fiber"], columns=["بيان", "عرض", "ارتفاع", "عدد"]))
