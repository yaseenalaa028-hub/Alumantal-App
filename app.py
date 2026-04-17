import streamlit as st
import math

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="DOGGA SMART ERP", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

if "projects" not in st.session_state:
    st.session_state.projects = []


# =========================
# تحويل آمن للأرقام
# =========================
def num(x):
    try:
        return float(x) if x != "" else 0
    except:
        return 0


# =========================
# HOME
# =========================
if st.session_state.page == "home":

    st.markdown("""
    <style>
    .logo{
        text-align:center;
        font-size:70px;
        font-weight:bold;
        color:#f1c40f;
        margin-top:8%;
    }
    .sub{
        text-align:center;
        font-size:22px;
    }
    .by{
        text-align:center;
        color:gray;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="logo">ضجة سمارت ERP</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">نظام تخصيم المطابخ الاحترافي</div>', unsafe_allow_html=True)
    st.markdown('<div class="by">برمجة المهندس / ياسين علاء</div>', unsafe_allow_html=True)

    if st.button("🚀 بدء النظام", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()


# =========================
# CALC
# =========================
elif st.session_state.page == "calc":

    st.title("🛠️ شاشة التخصيم")

    if st.button("🏠 الرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    # =========================
    # إدخال فاضي بالكامل (بدون 0.00)
    # =========================
    client = st.text_input("اسم العميل")

    unit = st.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

    W = st.text_input("العرض")
    H = st.text_input("الارتفاع")
    D = st.text_input("العمق")

    sh = st.text_input("عدد الأرفف")
    sh_w = st.text_input("عرض الرف")
    sh_d = st.text_input("عمق الرف")

    vf = st.text_input("عدد الفواصل")
    vf_h = st.text_input("ارتفاع الفاصل")
    vf_d = st.text_input("عمق الفاصل")

    dr = st.text_input("عدد الأدراج")
    dr_w = st.text_input("عرض الدرج")
    dr_d = st.text_input("عمق الدرج")

    # =========================
    # حساب
    # =========================
    if st.button("💾 حساب التخصيم"):

        W = num(W)
        H = num(H)
        D = num(D)

        sh = int(num(sh))
        sh_w = num(sh_w)
        sh_d = num(sh_d)

        vf = int(num(vf))
        vf_h = num(vf_h)
        vf_d = num(vf_d)

        dr = int(num(dr))
        dr_w = num(dr_w)
        dr_d = num(dr_d)

        if W and H and D:

            Hf = H - (13 if unit == "وحدة سفلية" else 5)
            Wf = W - 5
            Df = D - 5

            alum = []
            fiber = []

            # =========================
            # مونتال
            # =========================
            alum += [
                ["قائم", Hf, 2, "مفرد"],
                ["قائم", Hf, 2, "متقارب"],
                ["عرض", Wf, 3, "مفرد"],
                ["عرض", Wf, 2, "متقارب"],
                ["عمق", Df, 2, "مفرد"],
                ["عمق", Df, 2, "متقارب"],
            ]

            # =========================
            # أرفف
            # =========================
            if sh > 0:
                alum.append(["رف", Wf, sh * 2, "مفرد"])
                fiber.append(["رف", Wf - 5, Df - 5, sh])

            # =========================
            # فواصل
            # =========================
            if vf > 0:
                alum.append(["فاصل", Hf, vf * 4, "مفرد"])
                fiber.append(["فاصل", Hf - 5, Df - 5, vf])

            # =========================
            # أدراج
            # =========================
            if dr > 0:
                dw = dr_w - 2.5
                fiber.append(["درج", dw, dr_d, dr])

            # =========================
            # فيبر أساسي
            # =========================
            fiber += [
                ["ضهرية", Wf, Hf, 1],
                ["أرضية", Wf, Df, 1],
                ["أجناب", Hf, Df, 2],
            ]

            st.session_state.projects.append({
                "client": client,
                "unit": unit,
                "alum": alum,
                "fiber": fiber
            })

            st.success("تم الحساب بنجاح")

    # =========================
    # الجرد
    # =========================
    if st.session_state.projects:

        muf = mut = fib = 0

        for p in st.session_state.projects:
            for a in p["alum"]:
                if a[3] == "مفرد":
                    muf += a[1] * a[2]
                else:
                    mut += a[1] * a[2]

            for f in p["fiber"]:
                fib += f[1] * f[2] * f[3]

        st.markdown("## 📊 جرد الخامات")

        st.success(f"المفرد: {math.ceil(muf / 600)} عود")
        st.success(f"المتقارب: {math.ceil(mut / 600)} عود")
        st.success(f"الفيبر: {math.ceil(fib / (280*130))} لوح")

        if st.button("💰 الفاتورة"):
            st.session_state.page = "invoice"
            st.rerun()


# =========================
# INVOICE
# =========================
elif st.session_state.page == "invoice":

    st.title("📋 الفاتورة النهائية")

    if st.button("⬅️ رجوع"):
        st.session_state.page = "calc"
        st.rerun()

    for p in st.session_state.projects:

        st.markdown("---")

        st.markdown(f"## 👤 العميل: {p['client']}")
        st.markdown(f"### 🏷️ نوع الوحدة: {p['unit']}")

        st.markdown("## 🛠️ مونتال")

        for a in p["alum"]:
            st.markdown(f"""
            ▪ **{a[0]}**  
            المقاس: {a[1]}  
            العدد: {a[2]}  
            النوع: مونتال  
            ---
            """)

        st.markdown("## 🪵 فيبر")

        for f in p["fiber"]:
            st.markdown(f"""
            ▪ **{f[0]}**  
            المقاس: {f[1]} × {f[2]}  
            العدد: {f[3]}  
            النوع: فيبر  
            ---
            """)

        st.success("تم حساب الوحدة بالكامل")

    st.markdown("---")
    st.success("📦 نهاية الفاتورة")
