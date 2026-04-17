import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات النظام الأساسية
# ==========================================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

# وظيفة تنظيف عرض الأرقام في الجداول
def clean_num(df):
    return df.map(lambda x: f"{x:g}" if isinstance(x, (int, float)) else x)

# تهيئة Session State
if "project_list" not in st.session_state:
    st.session_state.project_list = []
if "page" not in st.session_state:
    st.session_state.page = "home"
if "last_id" not in st.session_state:
    st.session_state.last_id = None

# ==========================================
# 2. الصفحة الرئيسية
# ==========================================
if st.session_state.page == "home":
    st.markdown("""
        <div style='text-align:center;margin-top:10%;'>
            <h1 style='color:#f1c40f; font-size: 3.5em;'>ضجة سمارت</h1>
            <h2 style='color:#ffffff;'>نظام التخصيم الفني الشامل</h2>
            <p style='color:#bdc3c7; font-size: 1.2em;'>برمجة خاصة لدقة متناهية في جرد الألمنيوم والفيبر</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🚀 دخول لنظام التخصيم", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()

# ==========================================
# 3. صفحة الفاتورة (الجرد والتسعير)
# ==========================================
elif st.session_state.page == "invoice":
    st.title("📄 فاتورة الخامات النهائية")
    
    if st.button("⬅️ العودة للتخصيم"):
        st.session_state.page = "calc"
        st.rerun()

    # الحسابات الإجمالية للجرد
    t_m = 0; t_t = 0; t_f = 0
    for u in st.session_state.project_list:
        for a in u["alum"]:
            if a[3] == "مفرد": t_m += a[1] * a[2]
            else: t_t += a[1] * a[2]
        for f in u["fiber"]:
            t_f += f[1] * f[2] * f[3]

    qty_m = round(t_m / 600, 2)
    qty_t = round(t_t / 600, 2)
    qty_f = round(t_f / (280*130), 2)

    if "df_invoice" not in st.session_state:
        st.session_state.df_invoice = pd.DataFrame([
            {"البيان": "أعواد ألمنيوم (مفرد)", "العدد": qty_m, "سعر الوحدة": 0.0},
            {"البيان": "أعواد ألمنيوم (متقارب)", "العدد": qty_t, "سعر الوحدة": 0.0},
            {"البيان": "ألواح فيبر", "العدد": qty_f, "سعر الوحدة": 0.0},
        ])

    st.markdown("### ✏️ محرر الأسعار (إكسيل)")
    edited_df = st.data_editor(st.session_state.df_invoice, num_rows="dynamic", use_container_width=True, key="inv_edit")
    edited_df["الإجمالي"] = edited_df["العدد"] * edited_df["سعر الوحدة"]
    
    st.markdown("---")
    st.table(clean_num(edited_df))
    st.success(f"### 💰 إجمالي الفاتورة: {edited_df['الإجمالي'].sum():,.2f} جنيه")

# ==========================================
# 4. صفحة التخصيم (الكود الكامل 250+ سطر)
# ==========================================
else:
    st.title("🛠️ لوحة تخصيم الوحدات")
    
    if st.button("🏠 الرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    # استخدام Form مع تثبيت البيانات (clear_on_submit=False)
    with st.form(key="calculation_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        client = c1.text_input("👤 اسم العميل", key="cli_name")
        unit_type = c2.selectbox("📦 نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"], key="u_type")

        st.markdown("#### 📏 المقاسات الأساسية")
        d1, d2, d3 = st.columns(3)
        # value=None لإخفاء الـ 0.00
        W = d1.number_input("العرض (W)", value=None, key="w_val")
        H = d2.number_input("الارتفاع (H)", value=None, key="h_val")
        D = d3.number_input("العمق (D)", value=None, key="d_val")

        st.markdown("#### 📏 تفاصيل الأرفف")
        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.number_input("عدد الأرفف", value=None, key="sh_n")
        sh_w = sh2.number_input("عرض الرف", value=None, key="sh_w")
        sh_d = sh3.number_input("عمق الرف", value=None, key="sh_d")

        st.markdown("#### 📏 تفاصيل الفواصل")
        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", value=None, key="v_n")
        v_h = v2.number_input("ارتفاع الفاصل", value=None, key="v_h")
        v_d = v3.number_input("عمق الفاصل", value=None, key="v_d")

        st.markdown("#### 📏 تفاصيل الأدراج")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", value=None, key="dr_n")
        dr_w = dr2.number_input("عرض الدرج", value=None, key="dr_w")
        dr_d = dr3.number_input("عمق الدرج", value=None, key="dr_d")

        # زر التخصيم
        submit_btn = st.form_submit_button("🔨 تنفيذ التخصيم وإضافة للجرد")

    # منطق المعالجة (منع التكرار + الحساب الكامل)
    if submit_btn:
        if W and H and D:
            # منع التكرار باستخدام معرف فريد للمدخلات
            current_id = f"{client}-{W}-{H}-{D}-{sh_n}-{v_n}-{dr_n}"
            
            if st.session_state.last_id != current_id:
                # معادلات التخصيم الأصلية
                h_f = H - (13 if unit_type in ["وحدة سفلية", "دولاب خزين"] else 5)
                w_f = W - 5
                d_f = D - 5

                alum = []
                fiber = []

                # حسابات الهيكل (ألمنيوم)
                if unit_type == "وحدة سفلية":
                    alum = [
                        ["ارتفاع", h_f, 2, "مفرد"], ["ارتفاع", h_f, 2, "متقارب"],
                        ["عرض", w_f, 3, "مفرد"], ["عرض", w_f, 1, "متقارب"],
                        ["عمق", d_f, 2, "مفرد"], ["عمق", d_f, 2, "متقارب"]
                    ]
                else:
                    alum = [
                        ["ارتفاع", h_f, 2, "مفرد"], ["ارتفاع", h_f, 2, "متقارب"],
                        ["عرض", w_f, 2, "مفرد"], ["عرض", w_f, 2, "متقارب"],
                        ["عمق", d_f, 0, "مفرد"], ["عمق", d_f, 4, "متقارب"]
                    ]

                # حسابات الأرفف
                if sh_n and sh_n > 0:
                    alum += [["رف عرض", sh_w, sh_n * 2, "مفرد"], ["رف عمق", sh_d, sh_n * 2, "مفرد"]]
                    fiber.append(["لوح رف", sh_w - 5, sh_d - 5, sh_n])

                # حسابات الفواصل (إضافة عمق الفاصل)
                if v_n and v_n > 0:
                    alum += [["فاصل ارتفاع", v_h, v_n * 2, "مفرد"], ["فاصل عمق", v_d, v_n * 2, "مفرد"]]
                    fiber.append(["لوح فاصل", v_h - 5, v_d - 5, v_n])

                # حسابات الأدراج (إضافة عرض وعمق الدرج)
                if dr_n and dr_n > 0:
                    alum += [["درج عرض", dr_w - 2.5, dr_n * 2, "2x8"], ["درج عمق", dr_d, dr_n * 2, "2x8"]]
                    fiber.append(["لوح درج", dr_w, dr_d, dr_n])

                # حسابات الفيبر للهيكل
                fiber += [
                    ["ضهرية", w_f, h_f, 1],
                    ["أرضية", w_f, d_f, 1],
                    ["أجناب", h_f, d_f, 2]
                ]

                # الحفظ في القائمة
                st.session_state.project_list.append({
                    "client": client, "unit_type": unit_type, "alum": alum, "fiber": fiber
                })
                st.session_state.last_id = current_id # تحديث المعرف لمنع التكرار
                
                if "df_invoice" in st.session_state: del st.session_state.df_invoice
                st.success(f"✅ تم إضافة {unit_type} بنجاح.")
            else:
                st.info("ℹ️ هذه الوحدة مضافة بالفعل. عدل المقاسات لإضافة وحدة جديدة.")
        else:
            st.error("⚠️ يرجى إدخال المقاسات الأساسية (W, H, D)")

    # عرض الجرد والوحدات المضافة
    if st.session_state.project_list:
        st.markdown("---")
        if st.button("📄 الانتقال للفاتورة النهائية", use_container_width=True, type="primary"):
            st.session_state.page = "invoice"
            st.rerun()
        
        for unit in st.session_state.project_list:
            with st.expander(f"📦 جرد: {unit['unit_type']} - العميل: {unit['client']}"):
                col_a, col_f = st.columns(2)
                with col_a:
                    st.write("**الألمنيوم:**")
                    st.table(clean_num(pd.DataFrame(unit["alum"], columns=["بيان", "مقاس", "عدد", "نوع"])))
                with col_f:
                    st.write("**الفيبر:**")
                    st.table(clean_num(pd.DataFrame(unit["fiber"], columns=["بيان", "عرض", "ارتفاع", "عدد"])))
