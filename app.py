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
# صفحة الفاتورة
# =========================
elif st.session_state.page == "invoice":

    st.title("📄 فاتورة الخامات")

    if st.button("⬅️ رجوع"):
        st.session_state.page = "calc"
        st.rerun()

    if not st.session_state.project_list:
        st.warning("لا توجد بيانات")
    else:

        rows = []

        for unit in st.session_state.project_list:

            for a in unit["alum"]:
                rows.append({
                    "القسم": "مونتال",
                    "البيان": a[0],
                    "المقاس": int(a[1]),
                    "العدد": a[2],
                    "النوع": a[3],
                    "سعر الوحدة": 0,
                    "الإجمالي": 0
                })

            for f in unit["fiber"]:
                rows.append({
                    "القسم": "فيبر",
                    "البيان": f[0],
                    "المقاس": f"{int(f[1])}×{int(f[2])}",
                    "العدد": f[3],
                    "النوع": "فيبر",
                    "سعر الوحدة": 0,
                    "الإجمالي": 0
                })

        df = pd.DataFrame(rows)

        st.markdown("### ✏️ إدخال الأسعار")

        for i in range(len(df)):
            price = st.number_input(
                f"سعر {df.iloc[i]['القسم']} - {df.iloc[i]['البيان']} ({i})",
                key=f"price_{i}"
            )
            df.at[i, "سعر الوحدة"] = price
            df.at[i, "الإجمالي"] = price * df.at[i, "العدد"]

        st.markdown("### 📊 الفاتورة")

        st.dataframe(df, use_container_width=True)

        st.markdown(f"""
        <h2 style='color:green;'>💰 الإجمالي: {df['الإجمالي'].sum():.2f}</h2>
        """, unsafe_allow_html=True)

# =========================
# صفحة التخصيم
# =========================
else:

    st.title("🛠️ التخصيم")

    if st.button("🏠 رجوع"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # الإدخال
    # =========================
    with st.form("form"):

        c1, c2 = st.columns(2)
        client = c1.text_input("اسم العميل", key="client")
        unit_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"], key="type")

        d1, d2, d3 = st.columns(3)
        W = d1.number_input("العرض", key="W")
        H = d2.number_input("الارتفاع", key="H")
        D = d3.number_input("العمق", key="D")

        st.markdown("### الأرفف")
        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.number_input("عدد الأرفف", key="sh_n")
        sh_w = sh2.number_input("عرض الرف", key="sh_w")
        sh_d = sh3.number_input("عمق الرف", key="sh_d")

        st.markdown("### الفواصل")
        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", key="v_n")
        v_h = v2.number_input("ارتفاع الفاصل", key="v_h")
        v_d = v3.number_input("عمق الفاصل", key="v_d")

        st.markdown("### الأدراج")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", key="dr_n")
        dr_w = dr2.number_input("عرض الدرج", key="dr_w")
        dr_d = dr3.number_input("عمق الدرج", key="dr_d")

        submit = st.form_submit_button("حساب")

    # =========================
    # الحساب
    # =========================
    if submit and W > 0 and H > 0 and D > 0:

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

        if sh_n > 0:
            alum.append(["رف عرض", sh_w, sh_n * 2, "مفرد"])
            alum.append(["رف عمق", sh_d, sh_n * 2, "مفرد"])
            fiber.append(["رف", sh_w - 5, sh_d - 5, sh_n])

        if v_n > 0:
            alum.append(["فواصل", v_h, v_n * 2, "مفرد"])
            fiber.append(["فاصل", v_h - 5, v_d - 5, v_n])

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

    # =========================
    # الجرد
    # =========================
    if st.session_state.project_list:

        total_m = total_t = total_f = 0

        for u in st.session_state.project_list:

            for a in u["alum"]:
                if a[3] == "مفرد":
                    total_m += a[1] * a[2]
                else:
                    total_t += a[1] * a[2]

            for f in u["fiber"]:
                total_f += f[1] * f[2] * f[3]

        st.markdown("## 📊 جرد الخامات")

        st.write(f"🔹 مفرد: {total_m / 600:.2f} عود")
        st.write(f"🔹 متقارب: {total_t / 600:.2f} عود")
        st.write(f"🔹 فيبر: {total_f / (280*130):.2f} لوح")

        # زر الفاتورة
        if st.button("📄 فتح فاتورة الخامات", use_container_width=True):
            st.session_state.page = "invoice"
            st.rerun()

    # =========================
    # التفاصيل
    # =========================
    for unit in st.session_state.project_list:

        st.markdown(f"### 🏷️ {unit['unit_type']} - {unit['client']}")

        st.table(pd.DataFrame(unit["alum"], columns=["بيان", "مقاس", "عدد", "نوع"]))
        st.table(pd.DataFrame(unit["fiber"], columns=["بيان", "عرض", "ارتفاع", "عدد"]))
