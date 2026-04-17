import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام التخصيم الذكي", layout="wide")

# =========================
# STATE
# =========================
if "projects" not in st.session_state:
    st.session_state.projects = []

if "price_mode" not in st.session_state:
    st.session_state.price_mode = False


# =========================
# HEADER
# =========================
st.markdown("""
<h1 style='text-align:center;color:#f1c40f;'>نظام التخصيم الذكي</h1>
<p style='text-align:center;color:gray;'>برمجة المهندس / ياسين علاء</p>
<hr>
""", unsafe_allow_html=True)


# =========================
# INPUTS
# =========================
st.markdown("## 🛠️ إدخال البيانات")

c1, c2 = st.columns(2)
client = c1.text_input("اسم العميل")
unit_type = c2.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين"])

c1, c2, c3 = st.columns(3)
W = c1.number_input("العرض", 0.0)
H = c2.number_input("الارتفاع", 0.0)
D = c3.number_input("العمق", 0.0)

st.markdown("### 🧱 الأرفف")
c1, c2, c3 = st.columns(3)
sh_n = c1.number_input("عدد الأرفف", 0)
sh_w = c2.number_input("عرض الرف", 0.0)
sh_d = c3.number_input("عمق الرف", 0.0)

st.markdown("### 📐 الفواصل")
c1, c2, c3 = st.columns(3)
v_n = c1.number_input("عدد الفواصل", 0)
v_h = c2.number_input("ارتفاع الفاصل", 0.0)
v_d = c3.number_input("عمق الفاصل", 0.0)

st.markdown("### 🗄️ الأدراج")
c1, c2, c3 = st.columns(3)
dr_n = c1.number_input("عدد الأدراج", 0)
dr_w = c2.number_input("عرض الدرج", 0.0)
dr_d = c3.number_input("عمق الدرج", 0.0)


# =========================
# BUILD UNIT FUNCTION
# =========================
def build_unit():

    h_final = H - (13 if unit_type in ["سفلية", "دولاب خزين"] else 5)
    w_final = W - 5
    d_final = D - 5

    alum = []
    fiber = []

    # ================= المونتال =================
    if unit_type == "سفلية":
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

    # ================= الأرفف =================
    if sh_n > 0:
        alum.append(["رف عرض", sh_w, sh_n * 2, "مفرد"])
        alum.append(["رف عمق", sh_d, sh_n * 2, "مفرد"])
        fiber.append(["رف", sh_w - 5, sh_d - 5, sh_n])

    # ================= الفواصل =================
    if v_n > 0:
        alum.append(["فاصل ارتفاع", v_h, v_n * 2, "مفرد"])
        alum.append(["فاصل عمق", v_d, v_n * 2, "مفرد"])
        fiber.append(["فاصل", v_h - 5, v_d - 5, v_n])

    # ================= الأدراج =================
    if dr_n > 0:
        dw = dr_w - 2.5
        alum.append(["درج عرض", dw, dr_n * 2, "متقارب"])
        alum.append(["درج عمق", dr_d, dr_n * 2, "متقارب"])
        fiber.append(["قاعدة درج", dw, dr_d, dr_n])

    # ================= الفيبر =================
    fiber += [
        ["ضهرية", w_final, h_final, 1],
        ["أرضية", w_final, d_final, 1],
        ["أجناب", h_final, d_final, 2],
    ]

    return {
        "client": client,
        "type": unit_type,
        "alum": alum,
        "fiber": fiber
    }


# =========================
# ADD UNIT
# =========================
if st.button("➕ إضافة وحدة"):

    if W > 0 and H > 0 and D > 0:
        st.session_state.projects.append(build_unit())
        st.success("تمت الإضافة بنجاح")


# =========================
# INVENTORY
# =========================
if st.session_state.projects:

    total_m = 0
    total_t = 0
    fiber_sum = 0

    for u in st.session_state.projects:

        for a in u["alum"]:
            if a[3] == "مفرد":
                total_m += a[1] * a[2]
            else:
                total_t += a[1] * a[2]

        for f in u["fiber"]:
            fiber_sum += f[1] * f[2] * f[3]

    st.markdown("## 📊 الجرد")

    st.write(f"🔹 ألومنيوم مفرد: {total_m/600:.2f} عود")
    st.write(f"🔹 ألومنيوم متقارب: {total_t/600:.2f} عود")
    st.write(f"🔹 فيبر: {fiber_sum/(280*130):.2f} لوح")


# =========================
# DETAILS
# =========================
if st.session_state.projects:

    st.markdown("## 📋 التفاصيل")

    for u in st.session_state.projects:

        st.write(f"### 🏷️ {u['type']} - {u['client']}")

        st.table(pd.DataFrame(u["alum"], columns=["البيان","المقاس","العدد","النوع"]))
        st.table(pd.DataFrame(u["fiber"], columns=["البيان","العرض","الطول","العدد"]))


# =========================
# PRICING SYSTEM
# =========================
st.divider()

if st.session_state.projects:

    st.markdown("## 💰 الفاتورة والتسعير")

    if st.button("💰 فتح الفاتورة"):
        st.session_state.price_mode = True

    if st.session_state.price_mode:

        rows = []

        for u in st.session_state.projects:

            for a in u["alum"]:
                rows.append({
                    "الصنف": f"مونتال - {a[0]}",
                    "المقاس": a[1],
                    "العدد": a[2],
                    "النوع": a[3],
                    "سعر الوحدة": 0
                })

            for f in u["fiber"]:
                rows.append({
                    "الصنف": f"فيبر - {f[0]}",
                    "المقاس": f"{f[1]}x{f[2]}",
                    "العدد": f[3],
                    "النوع": "فيبر",
                    "سعر الوحدة": 0
                })

        df = pd.DataFrame(rows)

        st.markdown("### 🧾 إدخال الأسعار")

        for i in range(len(df)):

            price = st.number_input(
                f"سعر {df.iloc[i]['الصنف']} ({i})",
                min_value=0.0,
                key=f"p_{i}"
            )

            df.at[i, "سعر الوحدة"] = price
            df.at[i, "الإجمالي"] = price * df.at[i, "العدد"]

        st.markdown("### 📋 الفاتورة")

        st.dataframe(df, use_container_width=True)

        st.markdown(f"## 💰 الإجمالي النهائي: {df['الإجمالي'].sum():.2f}")

        if st.button("🧹 إغلاق الفاتورة"):
            st.session_state.price_mode = False
