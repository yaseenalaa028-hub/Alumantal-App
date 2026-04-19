import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="DOGGA SMART KITCHEN - الإدارة الهندسية", layout="wide")

# 2. تهيئة مخزن البيانات
if 'project_data' not in st.session_state:
    st.session_state.project_data = [] 
if 'page' not in st.session_state:
    st.session_state.page = 'main_menu'

# --- كود التصميم الجمالي المحدث (Gold & Black Stars) ---
st.markdown("""
    <style>
    /* القائمة الرئيسية: نصف ذهبي ونصف أسود بنجوم ذهبية */
    .stApp {
        background: linear-gradient(to right, 
            #D4AF37 50%, 
            #121212 50%);
        background-image: 
            linear-gradient(to right, #D4AF37 50%, transparent 50%),
            radial-gradient(circle at 75% 20%, #D4AF37 1.5px, transparent 1.5px),
            radial-gradient(circle at 85% 50%, #D4AF37 2px, transparent 2px),
            radial-gradient(circle at 70% 80%, #D4AF37 1.5px, transparent 1.5px),
            radial-gradient(circle at 92% 30%, #D4AF37 1.2px, transparent 1.2px);
        background-size: 100% 100%, 120px 120px, 180px 180px, 250px 250px, 150px 150px;
    }
    
    /* تنسيق اسم البرنامج بالإنجليزية */
    .main-title-text {
        text-align: center;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 45px;
        font-weight: 900;
        margin-top: 60px;
        letter-spacing: 2px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.6);
    }
    
    /* اسم المهندس بالأسود على الخلفية الذهبية */
    .dev-tag {
        color: #000000;
        text-align: center;
        font-weight: bold;
        font-size: 22px;
        margin-bottom: 60px;
        font-family: 'Arial';
    }

    /* أزرار القائمة */
    div.stButton > button {
        width: 100%;
        border-radius: 50px !important;
        height: 70px;
        font-weight: bold;
        font-size: 20px;
        border: 3px solid #D4AF37;
        background-color: #1e1e1e;
        color: #D4AF37;
        transition: 0.4s ease;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.4);
    }
    
    div.stButton > button:hover {
        border-color: #ffffff;
        color: #ffffff;
        background-color: #D4AF37;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

def add_to_project(unit_name, category, item_name, length, qty, unit_type="-"):
    st.session_state.project_data.append({
        "اسم الوحدة": unit_name,
        "الخامة": category,
        "اسم القطعة": item_name,
        "المقاس (سم)": length,
        "العدد": qty,
        "نوع التخصيم": unit_type
    })

# ==========================================
# الصفحة (0): القائمة الرئيسية (Main Menu)
# ==========================================
if st.session_state.page == 'main_menu':
    st.markdown('<div class="main-title-text">DOGGA SMART KITCHEN</div>', unsafe_allow_html=True)
    st.markdown('<div class="dev-tag">برمجة المهندس ياسين علاء</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🚀 ابدأ التخصيم"):
            st.session_state.page = 'deduction'
            st.rerun()
            
        if st.button("🖼️ تخصيم الدرف"):
            st.session_state.page = 'doors_empty'
            st.rerun()
            
        if st.button("📁 المشاريع"):
            st.session_state.page = 'inventory'
            st.rerun()

# ==========================================
# صفحة تخصيم الدرف (فارغة)
# ==========================================
elif st.session_state.page == 'doors_empty':
    st.markdown("<style>.stApp { background: white !important; }</style>", unsafe_allow_html=True)
    st.title("🖼️ تخصيم الدرف")
    st.info("هذه القائمة فارغة حالياً.")
    if st.button("⬅️ عودة للقائمة الرئيسية"):
        st.session_state.page = 'main_menu'
        st.rerun()

# ==========================================
# الصفحة الأولى: التخصيم التفصيلي (كودك الأصلي)
# ==========================================
elif st.session_state.page == 'deduction':
    st.markdown("<style>.stApp { background: white !important; color: black !important; }</style>", unsafe_allow_html=True)
    st.title("🏗️ تخصيم مشروع متكامل - ورشة DED EL KASR")
    
    if st.button("⬅️ العودة للقائمة الرئيسية"):
        st.session_state.page = 'main_menu'
        st.rerun()

    with st.form("main_form", clear_on_submit=True):
        st.subheader("📏 إدخال بيانات الوحدة")
        c_name, c_kind = st.columns(2)
        u_label = c_name.text_input("اسم الوحدة (مثلاً: سفلي 80 سم)", placeholder="وحدة 1")
        u_kind = c_kind.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])

        c1, c2, c3 = st.columns(3)
        W = c1.number_input("العرض الكلي (W)", min_value=0.0)
        H = c2.number_input("الارتفاع الكلي (H)", min_value=0.0)
        D = c3.number_input("العمق الكلي (D)", min_value=0.0)

        st.divider()
        st.subheader("📦 الأرفف والفواصل والأدراج")
        
        cs1, cs2, cs3 = st.columns(3)
        s_w = cs1.number_input("عرض الرف", value=0.0)
        s_d = cs2.number_input("عمق الرف", value=0.0)
        s_q = cs3.number_input("عدد الأرفف", min_value=0)

        cv1, cv2, cv3 = st.columns(3)
        v_h = cv1.number_input("ارتفاع الفاصل", value=0.0)
        v_d = cv2.number_input("عمق الفاصل", value=0.0)
        v_q = cv3.number_input("عدد الفواصل", min_value=0)

        cd1, cd2, cd3 = st.columns(3)
        dr_w = cd1.number_input("عرض الدرج", value=0.0)
        dr_d = cd2.number_input("عمق الدرج", value=0.0)
        dr_q = cd3.number_input("عدد الأدراج", min_value=0)

        submit = st.form_submit_button("✅ إضافة الوحدة للمشروع")

    if submit:
        if W > 0 and H > 0:
            name = u_label if u_label else f"وحدة {u_kind}"
            h_ded = 13 if u_kind in ["سفلي", "دولاب خزين"] else 5
            f_h, f_w, f_d = H - h_ded, W - 5, D - 5

            if u_kind == "سفلي":
                add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
                add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
                add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 3, "مفرد")
                add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 1, "متقارب")
                add_to_project(name, "ألومنيوم", "رباط عمق", f_d, 2, "مفرد")
                add_to_project(name, "ألومنيوم", "رباط عمق", f_d, 2, "متقارب")
            else:
                add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
                add_to_project(name, "ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
                add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 2, "مفرد")
                add_to_project(name, "ألومنيوم", "عارضة عرض", f_w, 2, "متقارب")
                add_to_project(name, "ألومنيوم", "رباط عمق", f_d, 4, "متقارب")

            add_to_project(name, "فيبر", "ضهرية", f"{f_w}×{f_h}", 1, "لوح")
            add_to_project(name, "فيبر", "أرضية", f"{f_w}×{f_d}", 1, "لوح")
            add_to_project(name, "فيبر", "أجناب", f"{f_h}×{f_d}", 2, "لوح")

            if s_q > 0:
                add_to_project(name, "ألومنيوم", "عرض رف", s_w, s_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "عمق رف", s_d, s_q*2, "مفرد")
                add_to_project(name, "فيبر", "حشو رف", f"{s_w-5}×{s_d-5}", s_q, "لوح")

            if v_q > 0:
                add_to_project(name, "ألومنيوم", "ارتفاع فاصل", v_h, v_q*2, "مفرد")
                add_to_project(name, "ألومنيوم", "عمق فاصل", v_d, v_q*2, "مفرد")
                add_to_project(name, "فيبر", "حشو فاصل", f"{v_h-5}×{v_d-5}", v_q, "لوح")

            if dr_q > 0:
                add_to_project(name, "ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q*2, "علبه درج")
                add_to_project(name, "ألومنيوم", "جنب درج", dr_d, dr_q*2, "علبه درج")
                add_to_project(name, "فيبر", "أرضية درج", f"{dr_w-7.5}×{dr_d-5}", dr_q, "لوح")

            st.success(f"تمت إضافة {name} للمشروع")

    if st.session_state.project_data:
        st.divider()
        df = pd.DataFrame(st.session_state.project_data)
        for n, g in df.groupby("اسم الوحدة"):
            st.subheader(f"📍 {n}")
            st.table(g.drop(columns=["اسم الوحدة"]))
        
        if st.button("💰 حساب استهلاك الخامات والتسعير ⬅️", use_container_width=True):
            st.session_state.page = 'inventory'
            st.rerun()

# ==========================================
# الصفحة الثانية: الاستهلاك (كودك الأصلي)
# ==========================================
elif st.session_state.page == 'inventory':
    st.markdown("<style>.stApp { background: white !important; }</style>", unsafe_allow_html=True)
    st.title("📊 استهلاك خامات المشروع - DOGGA SMART KITCHEN")
    
    if st.session_state.project_data:
        df = pd.DataFrame(st.session_state.project_data)
        alum = df[df["الخامة"] == "ألومنيوم"].copy()
        alum["المقاس (سم)"] = pd.to_numeric(alum["المقاس (سم)"], errors='coerce')

        st.subheader("🥢 تقدير أعواد الألومنيوم (6 متر)")
        summary = alum.groupby("نوع التخصيم").apply(
            lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()
        ).reset_index(name="إجمالي سم")
        summary["الأعواد"] = summary["إجمالي سم"].apply(lambda x: math.ceil(x / 600))
        st.table(summary)

        total_area = 0
        for _, row in df[df["الخامة"] == "فيبر"].iterrows():
            dims = str(row["المقاس (سم)"]).split('×')
            if len(dims) == 2:
                total_area += float(dims[0]) * float(dims[1]) * row["العدد"]
        sheets = math.ceil(total_area / (280 * 130))
        st.metric("عدد ألواح الفيبر المطلوبة", f"{sheets} لوح")

        st.divider()
        st.subheader("💵 فاتورة المشتريات المفتوحة")
        
        base_bill = []
        for _, r in summary.iterrows():
            base_bill.append({"الصنف": f"ألومنيوم {r['نوع التخصيم']}", "الكمية": r["الأعواد"], "السعر": 0.0})
        base_bill.append({"الصنف": "لوح فيبر كامل", "الكمية": sheets, "السعر": 0.0})

        final_bill = st.data_editor(pd.DataFrame(base_bill), num_rows="dynamic", use_container_width=True)
        total = (final_bill["الكمية"] * final_bill["السعر"]).sum()
        st.header(f"💰 التكلفة الإجمالية: {total:,.2f} ج.م")

        st.divider()
        with st.expander("🔍 مراجعة الأطوال الكلية"):
            st.dataframe(summary, use_container_width=True)

        st.write("### ⚙️ خيارات المشروع")
        c_inv1, c_inv2, c_inv3 = st.columns(3)
        
        with c_inv1:
            if st.button("⬅️ إضافة وحدات أخرى", use_container_width=True):
                st.session_state.page = 'deduction'; st.rerun()
                
        with c_inv2:
            csv_final = final_bill.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 تحميل الفاتورة", data=csv_final, file_name="DOGGA_Invoice.csv", mime="text/csv", use_container_width=True)
            
        with c_inv3:
            if st.button("🗑️ تفريغ المشروع", use_container_width=True, type="secondary"):
                st.session_state.project_data = []; st.session_state.page = 'main_menu'; st.rerun()
    else:
        st.error("⚠️ لا توجد بيانات.")
        if st.button("العودة للرئيسية"):
            st.session_state.page = 'main_menu'; st.rerun()
            # 4. تفاصيل إضافية للمراجعة (من كودك الأصلي)
        with st.expander("🔍 مراجعة الأطوال الكلية قبل التقطيع"):
            st.write("الأطوال التالية هي ناتج جمع كل القطع المضافة للمشروع:")
            st.dataframe(summary, use_container_width=True)

        # 5. منطقة أزرار الإجراءات النهائية (تكملة الـ inventory)
        st.write("### ⚙️ خيارات المشروع")
        c_inv1, c_inv2, c_inv3 = st.columns(3)
        
        with c_inv1:
            if st.button("⬅️ إضافة وحدات أخرى", key="add_more_final", use_container_width=True):
                st.session_state.page = 'deduction'
                st.rerun()
                
        with c_inv2:
            # تصدير الفاتورة النهائية
            csv_final = final_bill.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 تحميل الفاتورة (Excel)",
                data=csv_final,
                file_name=f"DOGGA_Smart_Invoice.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with c_inv3:
            # زر المسح النهائي مع العودة للقائمة الرئيسية (Gold/Black)
            if st.button("🗑️ تفريغ المشروع بالكامل", key="clear_all_final", use_container_width=True, type="secondary"):
                st.session_state.project_data = []
                st.session_state.page = 'main_menu'
                st.rerun()

    else:
        # حماية في حالة الدخول للصفحة مباشرة بدون بيانات
        st.error("⚠️ لا توجد بيانات مسجلة في المشروع حالياً.")
        if st.button("العودة للقائمة الرئيسية لإضافة وحدات", key="back_to_main_err"):
            st.session_state.page = 'main_menu'
            st.rerun()

# --- نهاية كود تطبيق DOGGA SMART KITCHEN المتكامل ---
# فخر الصناعة المصرية بلمسة هندسية
# المبرمج: المهندس ياسين علاء
