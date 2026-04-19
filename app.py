import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="DOGGA SYSTEM - الإصدار الشامل", layout="wide")

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
        font-weight: 900; margin-top: 40px; text-shadow: 3px 3px 6px rgba(0,0,0,0.6);
    }
    .dev-tag { color: #000000; text-align: center; font-weight: bold; font-size: 22px; margin-bottom: 40px; }
    
    /* تنسيق الجداول لتناسب الواجهة البيضاء في النتائج */
    .report-box { background-color: white; padding: 20px; border-radius: 15px; color: black; direction: rtl; }
    
    label { font-weight: bold; color: #ffffff !important; }
    .stNumberInput label, .stSelectbox label { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة حالة البيانات
if 'data_list' not in st.session_state:
    st.session_state.data_list = []

def add_to_bill(category, item_name, length, qty, unit_type="-"):
    st.session_state.data_list.append({
        "الخامة": category,
        "اسم القطعة": item_name,
        "المقاس (سم)": round(length, 1) if isinstance(length, (int, float)) else length,
        "العدد": qty,
        "نوع التخصيم": unit_type
    })

# --- الواجهة الرئيسية ---
st.markdown('<div class="main-title-text">DOGGA SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="dev-tag">برمجة المهندس ياسين علاء</div>', unsafe_allow_html=True)

# --- واجهة إدخال البيانات (مدعومة بـ Expander لتقليل الزحام) ---
with st.expander("📏 إدخال أبعاد الوحدة والأجزاء المنفصلة", expanded=True):
    st.subheader("1. أبعاد الوحدة الأساسية")
    c1, c2, c3, c4 = st.columns(4)
    unit_kind = c1.selectbox("نوع الوحدة", ["سفلي", "علوي", "دولاب خزين", "مطبقيه"])
    W = c2.number_input("عرض القطعة الكلي (W)", min_value=0.0)
    H = c3.number_input("ارتفاع القطعة الكلي (H)", min_value=0.0)
    D = c4.number_input("عمق القطعة الكلي (D)", min_value=0.0)

    st.divider()
    c_s1, c_v1, c_d1 = st.columns(3)
    with c_s1:
        st.subheader("الأرفف")
        s_w = st.number_input("عرض الرف", value=0.0); s_d = st.number_input("عمق الرف", value=0.0); s_q = st.number_input("عدد الأرفف", 0)
    with c_v1:
        st.subheader("الفواصل")
        v_h = st.number_input("ارتفاع الفاصل", value=0.0); v_d = st.number_input("عمق الفاصل", value=0.0); v_q = st.number_input("عدد الفواصل", 0)
    with c_d1:
        st.subheader("الأدراج")
        dr_w = st.number_input("عرض الدرج", value=0.0); dr_d = st.number_input("عمق الدرج", value=0.0); dr_q = st.number_input("عدد الأدراج", 0)

# --- محرك الحسابات الهندسي ---
if st.button("🚀 إصدار بيان التقطيع وحساب الخامات", use_container_width=True):
    st.session_state.data_list = []
    
    if W > 0 and H > 0:
        # [ أ ] تخصيم الألومنيوم للوحدة
        h_ded = 13 if unit_kind in ["سفلي", "دولاب خزين"] else 5
        f_h, f_w, f_d = H - h_ded, W - 5, D - 5

        # توزيع المفرد والمتقارب حسب طلبك
        if unit_kind == "سفلي":
            add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
            add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
            add_to_bill("ألومنيوم", "عارضة عرض", f_w, 3, "مفرد")
            add_to_bill("ألومنيوم", "عارضة عرض", f_w, 1, "متقارب")
            add_to_bill("ألومنيوم", "رباط عمق", f_d, 2, "مفرد")
            add_to_bill("ألومنيوم", "رباط عمق", f_d, 2, "متقارب")
            add_to_bill("فيبر", "أرضية فقط", f"{f_w} × {f_d}", 1, "حشو")
        else:
            add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "مفرد")
            add_to_bill("ألومنيوم", "قائم ارتفاع", f_h, 2, "متقارب")
            add_to_bill("ألومنيوم", "عارضة عرض", f_w, 2, "مفرد")
            add_to_bill("ألومنيوم", "عارضة عرض", f_w, 2, "متقارب")
            add_to_bill("ألومنيوم", "رباط عمق", f_d, 4, "متقارب")
            add_to_bill("فيبر", "أرضية + سقفية", f"{f_w} × {f_d}", 2, "حشو")

        add_to_bill("فيبر", "ضهرية الوحدة", f"{f_w} × {f_h}", 1, "حشو")
        add_to_bill("فيبر", "أجناب الوحدة", f"{f_h} × {f_d}", 2, "حشو")

        # [ ج ] الأرفف والفواصل والأدراج (بمعادلاتها الدقيقة)
        if s_q > 0:
            add_to_bill("ألومنيوم", "عرض الرف", s_w, s_q * 2, "مفرد")
            add_to_bill("ألومنيوم", "عمق الرف", s_d, s_q * 2, "مفرد")
            add_to_bill("فيبر", "حشو رف", f"{s_w-5} × {s_d-5}", s_q, "خصم 5 سم")
        if v_q > 0:
            add_to_bill("ألومنيوم", "ارتفاع فاصل", v_h, v_q * 2, "مفرد")
            add_to_bill("ألومنيوم", "عمق فاصل", v_d, v_q * 2, "مفرد")
            add_to_bill("فيبر", "حشو فاصل", f"{v_h-5} × {v_d-5}", v_q, "خصم 5 سم")
        if dr_q > 0:
            add_to_bill("ألومنيوم", "وش/ضهر درج", dr_w - 2.5, dr_q * 2, "مفرد")
            add_to_bill("ألومنيوم", "جنب درج عمق", dr_d, dr_q * 2, "مفرد")

# --- عرض النتائج في جداول منفصلة ---
if st.session_state.data_list:
    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    df_full = pd.DataFrame(st.session_state.data_list)

    # 1. جدول الألومنيوم
    st.subheader("🟦 أولاً: جدول تقطيع الألومنيوم")
    df_alum = df_full[df_full["الخامة"] == "ألومنيوم"].drop(columns=["الخامة"])
    st.table(df_alum)

    # 2. جدول حسابات الخامات (عدد الأعواد) - الميزة المتفق عليها
    st.subheader("🥢 ثانياً: ملخص حساب الأعواد (طول 6 متر)")
    df_alum["المقاس (سم)"] = pd.to_numeric(df_alum["المقاس (سم)"], errors='coerce')
    summary = df_alum.groupby("اسم القطعة").apply(lambda x: (x["المقاس (سم)"] * x["العدد"]).sum()).reset_index(name="الإجمالي سم")
    summary["عدد الأعواد"] = summary["الإجمالي سم"].apply(lambda x: math.ceil(x/600))
    st.dataframe(summary, use_container_width=True)

    # 3. جدول الفيبر
    st.subheader("⬜ ثالثاً: جدول تقطيع الفيبر")
    df_fiber = df_full[df_full["الخامة"] == "فيبر"].drop(columns=["الخامة", "نوع التخصيم"])
    st.table(df_fiber)

    # تحميل البيانات
    csv = df_full.to_csv(index=False).encode('utf-8-sig')
    st.download_button(label="📥 تحميل شيت التخصيم الكامل (Excel)", data=csv, file_name="DOGGA_Deduction_Report.csv", mime="text/csv", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
