import streamlit as st
import pandas as pd

# ==========================================
# 1. إعدادات النظام والتنسيق
# ==========================================
st.set_page_config(page_title="DOGGA SMART SYSTEM", layout="wide")

# تهيئة مخزن البيانات (Session State)
if "project_list" not in st.session_state:
    st.session_state.project_list = []
if "page" not in st.session_state:
    st.session_state.page = "home"
if "last_processed_id" not in st.session_state:
    st.session_state.last_processed_id = None

# وظيفة تنظيف الأرقام (لتحويل 2.0000 إلى 2 لسهولة القراءة)
def clean_num(df):
    return df.map(lambda x: f"{x:g}" if isinstance(x, (int, float)) else x)

# ==========================================
# 2. الصفحة الرئيسية
# ==========================================
if st.session_state.page == "home":
    st.markdown("""
        <div style='text-align:center;margin-top:10%;'>
            <h1 style='color:#f1c40f; font-size: 3.5em;'>ضجة سمارت</h1>
            <h2 style='color:#ffffff;'>نظام التخصيم الفني المتكامل</h2>
            <p style='color:#bdc3c7; font-size: 1.2em;'>دقة متناهية في حسابات الألمنيوم والفيبر</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 دخول لنظام التخصيم", use_container_width=True):
        st.session_state.page = "calc"
        st.rerun()

# ==========================================
# 3. صفحة الفاتورة
# ==========================================
elif st.session_state.page == "invoice":
    st.title("📄 فاتورة الخامات النهائية")
    
    if st.button("⬅️ العودة للتخصيم"):
        st.session_state.page = "calc"
        st.rerun()

    # حساب الجرد الإجمالي (مع صمام أمان لمنع القفلة TypeError)
    t_m = 0; t_t = 0; t_f = 0
    for u in st.session_state.project_list:
        for a in u["alum"]:
            val = a[1] if (a[1] is not None) else 0
            count = a[2] if (a[2] is not None) else 0
            if a[3] == "مفرد": t_m += val * count
            else: t_t += val * count
        for f in u["fiber"]:
            w = f[1] if (f[1] is not None) else 0
            h = f[2] if (f[2] is not None) else 0
            qty = f[3] if (f[3] is not None) else 0
            t_f += w * h * qty

    qty_m = round(t_m / 600, 2)
    qty_t = round(t_t / 600, 2)
    qty_f = round(t_f / (280*130), 2)

    if "df_invoice" not in st.session_state:
        st.session_state.df_invoice = pd.DataFrame([
            {"البيان": "أعواد ألمنيوم (مفرد)", "العدد": qty_m, "سعر الوحدة": 0.0},
            {"البيان": "أعواد ألمنيوم (متقارب)", "العدد": qty_t, "سعر الوحدة": 0.0},
            {"البيان": "ألواح فيبر", "العدد": qty_f, "سعر الوحدة": 0.0},
        ])

    st.markdown("### ✏️ تحرير بنود الأسعار")
    edited_df = st.data_editor(st.session_state.df_invoice, num_rows="dynamic", use_container_width=True, key="inv_editor")
    edited_df["الإجمالي"] = edited_df["العدد"] * edited_df["سعر الوحدة"]
    
    st.table(clean_num(edited_df))
    st.success(f"### 💰 إجمالي الفاتورة: {edited_df['الإجمالي'].sum():,.2f} جنيه")

# ==========================================
# 4. صفحة التخصيم (الكود الكامل مع زر المسح)
# ==========================================
else:
    st.title("🛠️ لوحة تخصيم الوحدات")
    
    if st.button("🏠 الرئيسية"):
        st.session_state.page = "home"
        st.rerun()

    # Form يضمن بقاء الأرقام بعد التخصيم للمراجعة
    with st.form(key="full_calc_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        client = c1.text_input("👤 اسم العميل", key="c_name")
        unit_type = c2.selectbox("📦 نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين"])

        st.markdown("#### 📏 المقاسات الكلية")
        d1, d2, d3 = st.columns(3)
        W = d1.number_input("العرض (W)", value=None)
        H = d2.number_input("الارتفاع (H)", value=None)
        D = d3.number_input("العمق (D)", value=None)

        st.markdown("#### 📏 الأرفف")
        sh1, sh2, sh3 = st.columns(3)
        sh_n = sh1.number_input("عدد الأرفف", value=None)
        sh_w = sh2.number_input("عرض الرف", value=None)
        sh_d = sh3.number_input("عمق الرف", value=None)

        st.markdown("#### 📏 الفواصل")
        v1, v2, v3 = st.columns(3)
        v_n = v1.number_input("عدد الفواصل", value=None)
        v_h = v2.number_input("ارتفاع الفاصل", value=None)
        v_d = v3.number_input("عمق الفاصل", value=None)

        st.markdown("#### 📏 الأدراج")
        dr1, dr2, dr3 = st.columns(3)
        dr_n = dr1.number_input("عدد الأدراج", value=None)
        dr_w = dr2.number_input("عرض الدرج", value=None)
        dr_d = dr3.number_input("عمق الدرج", value=None)

        submit_btn = st.form_submit_button("🔨 تنفيذ التخصيم وإضافة للجرد")

    # معالجة البيانات ومنع التكرار التلقائي
    if submit_btn:
        if W and H and D:
            op_id = f"{client}-{W}-{H}-{D}-{sh_n}-{v_n}-{dr_n}"
            if st.session_state.last_processed_id != op_id:
                # معادلات التخصيم
                h_f = H - (13 if unit_type in ["وحدة سفلية", "دولاب خزين"] else 5)
                w_f = W - 5
                d_f = D - 5
                alum = []; fiber = []

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

                if sh_n and sh_n > 0:
                    alum += [["رف عرض", sh_w, sh_n * 2, "مفرد"], ["رف عمق", sh_d, sh_n * 2, "مفرد"]]
                    fiber.append(["لوح رف", sh_w - 5, sh_d - 5, sh_n])

                if v_n and v_n > 0:
                    alum += [["فاصل ارتفاع", v_h, v_n * 2, "مفرد"], ["فاصل عمق", v_d, v_n * 2, "مفرد"]]
                    fiber.append(["لوح فاصل", v_h - 5, v_d - 5, v_n])

                if dr_n and dr_n > 0:
                    alum += [["درج عرض", dr_w - 2.5, dr_n * 2, "2x8"], ["درج عمق", dr_d, dr_n * 2, "2x8"]]
                    fiber.append(["لوح درج", dr_w, dr_d, dr_n])

                fiber += [["ضهرية", w_f, h_f, 1], ["أرضية", w_f, d_f, 1], ["أجناب", h_f, d_f, 2]]

                st.session_state.project_list.append({"client": client, "unit_type": unit_type, "alum": alum, "fiber": fiber})
                st.session_state.last_processed_id = op_id
                if "df_invoice" in st.session_state: del st.session_state.df_invoice
                st.success("✅ تم الحساب بنجاح.")
            else:
                st.info("ℹ️ هذه الوحدة مضافة بالفعل.")
        else:
            st.error("⚠️ يرجى إدخال المقاسات الأساسية.")

    # عرض الجرد وأزرار التحكم
    if st.session_state.project_list:
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        
        if col_btn1.button("📄 فتح الفاتورة النهائية", use_container_width=True, type="primary"):
            st.session_state.page = "invoice"
            st.rerun()
            
        # زر مسح المشروع (الذي تم إعادته بناءً على طلبك)
        if col_btn2.button("🗑️ مسح كافة الوحدات (مشروع جديد)", use_container_width=True):
            st.session_state.project_list = []
            st.session_state.last_processed_id = None
            if "df_invoice" in st.session_state: del st.session_state.df_invoice
            st.rerun()
        
        for unit in st.session_state.project_list:
            with st.expander(f"📦 جرد: {unit['unit_type']} - العميل: {unit['client']}"):
                c_a, c_f = st.columns(2)
                with c_a:
                    st.write("**الألمنيوم:**")
                    st.table(clean_num(pd.DataFrame(unit["alum"], columns=["بيان", "مقاس", "عدد", "نوع"])))
                with c_f:
                    st.write("**الفيبر:**")
                    st.table(clean_num(pd.DataFrame(unit["fiber"], columns=["بيان", "عرض", "ارتفاع", "عدد"])))
