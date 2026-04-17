import streamlit as st
import pandas as pd

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(page_title="SMART ALUM SYSTEM", layout="wide")

# =========================
# Session State
# =========================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "project_list" not in st.session_state:
    st.session_state.project_list = []

if "show_price" not in st.session_state:
    st.session_state.show_price = False


# =========================
# LOGIN PAGE
# =========================
if st.session_state.page == "login":

    st.markdown("""
        <style>
        .center {
            text-align: center;
            margin-top: 15%;
        }
        .title {
            font-size: 50px;
            color: #f1c40f;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='center'><div class='title'>ضجة سمارت</div></div>", unsafe_allow_html=True)

    user = st.text_input("اسم المستخدم", key="login_user")
    password = st.text_input("كلمة المرور", type="password", key="login_pass")

    if st.button("دخول", use_container_width=True):
        if user and password:
            st.session_state.page = "home"
            st.rerun()
        else:
            st.warning("اكتب البيانات")

# =========================
# HOME PAGE
# =========================
elif st.session_state.page == "home":

    st.title("🏠 الصفحة الرئيسية")

    if st.button("🚀 ابدأ التخصيم", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()

    if st.button("🚪 تسجيل خروج"):
        st.session_state.page = "login"
        st.rerun()


# =========================
# CALC PAGE
# =========================
else:

    st.title("🛠️ نظام التخصيم")

    if st.button("⬅️ رجوع"):
        st.session_state.page = "home"
        st.rerun()

    # =====================
    # FORM
    # =====================
    with st.form("main_form"):

        c1, c2 = st.columns(2)

        client = c1.text_input("اسم العميل", key="client_name")
        unit_type = c2.selectbox(
            "نوع الوحدة",
            ["وحدة سفلية", "وحدة علوية", "دولاب خزين"],
            key="unit_type"
        )

        d1, d2, d3 = st.columns(3)

        W = d1.number_input("العرض", min_value=0.0, step=1.0, key="W")
        H = d2.number_input("الارتفاع", min_value=0.0, step=1.0, key="H")
        D = d3.number_input("العمق", min_value=0.0, step=1.0, key="D")

        st.markdown("### الأرفف")

        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.number_input("عدد الأرفف", min_value=0, key="sh_n")
        sh_w = sh2.number_input("عرض الرف", min_value=0.0, key="sh_w")
        sh_d = sh3.number_input("عمق الرف", min_value=0.0, key="sh_d")

        st.markdown("### الفواصل")

        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", min_value=0, key="v_n")
        v_h = v2.number_input("ارتفاع الفاصل", min_value=0.0, key="v_h")
        v_d = v3.number_input("عمق الفاصل", min_value=0.0, key="v_d")

        st.markdown("### الأدراج")

        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", min_value=0, key="dr_n")
        dr_w = dr2.number_input("عرض الدرج", min_value=0.0, key="dr_w")
        dr_d = dr3.number_input("عمق الدرج", min_value=0.0, key="dr_d")

        submit = st.form_submit_button("حساب")

    # =====================
    # CALCULATION
    # =====================
    if submit and W > 0 and H > 0 and D > 0:

        h_final = H - (13 if unit_type in ["وحدة سفلية", "دولاب خزين"] else 5)
        w_final = W - 5
        d_final = D - 5

        alum = []
        fiber = []

        # Montal
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

        # shelves
        if sh_n > 0:
            alum.append(["رف عرض", sh_w, sh_n * 2, "مفرد"])
            alum.append(["رف عمق", sh_d, sh_n * 2, "مفرد"])
            fiber.append(["رف", sh_w - 5, sh_d - 5, sh_n])

        # dividers
        if v_n > 0:
            alum.append(["فواصل", v_h, v_n * 2, "مفرد"])
            alum.append(["فواصل", v_d, v_n * 2, "مفرد"])
            fiber.append(["فاصل", v_h - 5, v_d - 5, v_n])

        # drawers
        if dr_n > 0:
            alum.append(["درج", dr_w - 2.5, dr_n * 2, "2x8"])
            alum.append(["درج", dr_d, dr_n * 2, "2x8"])
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

    # =====================
    # REPORT
    # =====================
    if st.session_state.project_list:

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

        st.markdown("## 📊 الجرد")

        st.write(f"المفرد: {total_m / 600:.2f}")
        st.write(f"المتقارب: {total_t / 600:.2f}")
        st.write(f"الفيبر: {total_f / (280*130):.2f}")

        # =====================
        # PRICE SYSTEM
        # =====================
        if st.button("💰 فتح التسعير", key="price_btn"):
            st.session_state.show_price = True

        if st.session_state.show_price:

            rows = []
            for i, unit in enumerate(st.session_state.project_list):

                for a in unit["alum"]:
                    rows.append({
                        "item": f"مونتال - {a[0]}",
                        "qty": a[2],
                        "price": 0
                    })

                for f in unit["fiber"]:
                    rows.append({
                        "item": f"فيبر - {f[0]}",
                        "qty": f[3],
                        "price": 0
                    })

            df = pd.DataFrame(rows)

            for i in range(len(df)):
                df.at[i, "price"] = st.number_input(
                    f"سعر {df.iloc[i]['item']} {i}",
                    key=f"price_{i}"
                )

            df["total"] = df["qty"] * df["price"]

            st.table(df)
            st.write("## الإجمالي:", df["total"].sum())

    # =====================
    # DETAILS
    # =====================
    for unit in st.session_state.project_list:

        st.markdown(f"### {unit['client']} - {unit['unit_type']}")

        st.table(pd.DataFrame(unit["alum"], columns=["بيان", "مقاس", "عدد", "نوع"]))
        st.table(pd.DataFrame(unit["fiber"], columns=["بيان", "عرض", "ارتفاع", "عدد"]))
