import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="DOGGA SYSTEM", layout="wide")

# 2. تهيئة مخزن البيانات والصفحات
if 'data_list' not in st.session_state:
    st.session_state.data_list = [] 
if 'page' not in st.session_state:
    st.session_state.page = 'deduction' # الصفحة الافتراضية

# --- الواجهة المتفق عليها (الذهب والأسود والنجوم) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #D4AF37 50%, #121212 50%);
        background-image: 
            linear-gradient(to right, #D4AF37 50%, transparent 50%),
            radial-gradient(circle at 75% 20%, #D4AF37 1.5px, transparent 1.5px),
            radial-gradient(circle at 85% 50%, #D4AF37 2px, transparent 2px),
            radial-gradient(circle at 70% 80%, #D4AF37 1.5px, transparent 1.5px),
            radial-gradient(circle at 92% 30%, #D4AF37 1.2px, transparent 1.2px);
        background-size: 100% 100%, 120px 120px, 180px 180px, 250px 250px, 150px 150px;
    }
    .main-title-text {
        text-align: center; color: #ffffff; font-family: 'Segoe UI'; font-size: 45px;
        font-weight: 900; margin-top: 20px; text-shadow: 3px 3px 6px rgba(0,0,0,0.6);
    }
    .dev-tag { color: #000000; text-align: center; font-weight: bold; font-size: 22px; margin-bottom: 20px; }
    .report-box { background-color: white; padding: 20px; border-radius: 15px; color: black; }
    div.stButton > button {
        width: 100%; border-radius: 50px !important; height: 55px; font-weight: bold;
        border: 2px solid #D4AF37; background-color: #1e1e1e; color: #D4AF37;
    }
    div.stButton > button:hover { border-color: #ffffff; color: #ffffff; background-color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

def add_to_bill(category, item_name, length, qty, unit_type="-"):
    st.session_state.data_list.append({
        "الخامة": category, "اسم القطعة": item_name,
        "المقاس (سم)": round(length, 1) if isinstance(length, (int, float)) else length,
        "العدد": qty, "نوع التخصيم": unit_type
    })

# العناوين الثابتة
st.markdown('<div class="main-title-text">DOGGA SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="dev-tag">برمجة المهندس ياسين علاء</div>', unsafe_allow_html=True)

# ==========================================
# الصفحة الأولى: التخصيم وإدخال البيانات
# ==========================================
if st.session_state.page == 'deduction':
    with st.container():
        st.subheader("📏 1. أبعاد الوحدة الأساسية")
        c1, c2, c3, c4 = st.columns(4)
        unit_kind = c1.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])
        W = c2.number_input("عرض القطعة الكلي (W)", min_value=0.0)
        H = c3.number_input("ارتفاع القطعة الكلي (H)", min_value=0.0)
        D = c4.number_input("عمق القطعة الكلي (D)", min_value=0.0)

        st.divider()
        st.subheader("📦 2. الأجزاء الإضافية")
        col1, col2, col3 = st.columns(3)
        with col1:
            s_w = st.number_input("عرض الرف", value=0.0); s_d = st.number_input("عمق الرف", value=0.0); s_q = st.number_input("عدد الأرفف", 0)
        with col2:
            v_h = st.number_input("ارتفاع الفاصل", value=0.0); v_d = st.number_input("عمق الفاصل", value=0.0); v_q = st.number_input("عدد الفواصل", 0)
        with col3:
            dr_w = st.number_input("عرض الدرج", value=0.0); dr_d = st.number_input("عمق الدرج", value=0.0); dr_q = st.number_input("عدد الأدراج", 0)

        if st.button("🚀 إضافة الوحدة وإصدار بيان التقطيع", use_container_width=True):
            if W > 0 and H > 0:
                h_ded = 13 if unit_kind in ["سفلي", "دولاب خزين"] else 5
                f_h, f_w, f_d = H - h_ded, W - 5, D - 5
                
                # ألومنيوم الوحدة
                if unit_kind == "سفلي":
                    add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
                    add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
                    add_to_bill("ألومنيوم", "عارضة عرض", f_w, 3, "مفرد")
                    add_to_bill("ألومنيوم", "عارضة عرض", f_w, 1, "متقارب")
                    add_to_bill("ألومنيوم", "رباط عمق", f_d, 2, "مفرد")
                    add_to_bill("ألومنيوم", "رباط عمق", f_d, 2, "متقارب")
                else:
                    add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
                    add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
                    add_to_bill("ألومنيوم", "عارضة عرض", f_w, 2, "مفرد")
                    add_to_bill("ألومنيوم", "عارضة عرض", f_w, 2, "متقارب")
                    add_to_bill("ألومنيوم", "رباط عمق", f_d, 4, "متقارب")

                # فيبر الوحدة
                add_to_bill("فيبر", "ضهرية الوحدة", f"{f_w} × {f_h}", 1, "حشو")
                add_to_bill("فيبر", "أرضية الوحدة", f"{f_w} × {f_d}", 1, "حشو")
                add_to_bill("فيبر", "أجناب الوحدة", f"{f_h} × {f_d}", 2, "حشو")

                # الأرفف والفواصل والأدراج
                if s_q > 0:
                    add_to_bill("ألومنيوم", "عرض الرف", s_w, s_q * 2, "مفرد")
                    add_to_bill("ألومنيوم", "عمق الرف", s_d, s_q * 2, "مفرد")
                    add_to_bill("فيبر", "حشو رف", f"{s_w-5} × {s_d-5}", s_q, "خصم 5 سم")
                if dr_q > 0:
                    add_to_bill("ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q * 2, "مفرد")
                    add_to_bill("ألومنيوم", "جنب درج عمق", dr_d, dr_q * 2, "مفرد")
                
                st.success("تم إضافة الوحدة بنجاح!")
                st.session_state.page = 'inventory'
                st.rerun()

# ==========================================
# الصفحة الثانية: الجرد والفاتورة (Inventory)
# ==========================================
elif st.session_state.page == 'inventory':
    if st.session_state.data_list:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        df_full = pd.DataFrame(st.session_state.data_list)
        
        # 1. جداول التقطيع
        st.subheader("🟦 جداول تقطيع الألومنيوم والفيبر")
        c_table1, c_table2 = st.columns(2)
        with c_table1:
            st.write("**الألومنيوم**")
            st.dataframe(df_full[df_full["الخامة"] == "ألومنيوم"].drop(columns=["الخامة"]), use_container_width=True)
        with c_table2:
            st.write("**الفيبر**")
            st.dataframe(df_full[df_full["الخامة"] == "فيبر"].drop(columns=["الخامة"]), use_container_width=True)

        # 2. حساب الفاتورة (عدد الأعواد)
        st.divider()
        st.subheader("💵 فاتورة المشتريات (الأعواد)")
        df_alum = df_full[df_full["الخامة"] == "ألومنيوم"].copy()
        df_alum["المقاس (سم)"] = pd.to_numeric(df_alum["المقاس (سم)"], errors='coerce')
        summary = df_alum.groupby("اسم القطعة").apply(lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()).reset_index(name="الإجمالي سم")
        summary["الأعواد"] = summary["الإجمالي سم"].apply(lambda x: math.ceil(x/600))
        
        # جدول الفاتورة القابل للتعديل
        final_bill = st.data_editor(pd.DataFrame([{"الصنف": r["اسم القطعة"], "الكمية": r["الأعواد"], "السعر": 0.0} for _, r in summary.iterrows()]), use_container_width=True)
        st.write(f"### إجمالي الفاتورة: {(final_bill['الكمية'] * final_bill['السعر']).sum():,.2f} ج.م")

        st.divider()
        # 4. تفاصيل إضافية للمراجعة (الـ Expander اللي بعته)
        with st.expander("🔍 مراجعة الأطوال الكلية قبل التقطيع"):
            st.write("الأطوال التالية هي ناتج جمع كل القطع المضافة للمشروع:")
            st.dataframe(summary, use_container_width=True)

        # 5. منطقة أزرار الإجراءات (الأزرار التلاتة)
        st.write("### ⚙️ خيارات المشروع")
        c_inv1, c_inv2, c_inv3 = st.columns(3)
        
        with c_inv1:
            if st.button("⬅️ إضافة وحدات أخرى", use_container_width=True):
                st.session_state.page = 'deduction'; st.rerun()
        
        with c_inv2:
            csv_final = final_bill.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 تحميل الفاتورة (Excel)", data=csv_final, file_name="DOGGA_Project_Invoice.csv", mime="text/csv", use_container_width=True)
            
        with c_inv3:
            if st.button("🗑️ تفريغ المشروع بالكامل", use_container_width=True, type="secondary"):
                st.session_state.data_list = []
                st.session_state.page = 'deduction'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("⚠️ لا توجد بيانات مسجلة في المشروع حالياً.")
        if st.button("الذهاب لصفحة التخصيم لإضافة وحدات"):
            st.session_state.page = 'deduction'; st.rerun()
