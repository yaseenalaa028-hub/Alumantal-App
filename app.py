import streamlit as st
import pandas as pd

# إعداد واجهة الصفحة
st.set_page_config(page_title="برنامج تخصيم الألومنيوم", layout="wide")

# تهيئة مخزن البيانات
if 'data' not in st.session_state:
    st.session_state.data = []

st.title("⚒️ نظام إدارة ورشة الألومنيوم")
st.markdown("---")

# --- الخانة الأولى: مدخلات المقاسات (ترتيب أفقي) ---
st.subheader("1️⃣ إدخال مقاسات الوحدة")
with st.container():
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1:
        title = st.text_input("اسم الوحدة", "مطبخ - وحدة 1")
    with c2:
        u_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب"])
    with c3:
        w = st.number_input("العرض (W)", min_value=0.0, format="%.1f")
    with c4:
        h = st.number_input("الارتفاع (H)", min_value=0.0, format="%.1f")

    c5, c6, c7, c8 = st.columns([1, 1, 1, 2])
    with c5:
        d = st.number_input("العمق (D)", min_value=0.0, format="%.1f")
    with c6:
        shelves = st.number_input("الرفوف", min_value=0, step=1)
    with c7:
        drawers = st.number_input("الأدراج", min_value=0, step=1)
    with c8:
        st.write(" ") # موازنة شكل الزر
        if st.button("➕ إضافة الوحدة للمشروع", use_container_width=True):
            entry = {"الوحدة": title, "النوع": u_type, "عرض": w, "ارتفاع": h, "عمق": d, "رفوف": shelves, "أدراج": drawers}
            st.session_state.data.append(entry)

st.markdown("---")

# --- الخانة الثانية: جدول مراجعة المقاسات ---
st.subheader("2️⃣ جدول الوحدات المضافة")
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.table(df) # عرض كجدول ثابت ومنظم
    if st.button("🗑️ مسح الجدول بالكامل"):
        st.session_state.data = []
        st.rerun()
else:
    st.info("لا توجد بيانات حالياً. ابدأ بإضافة وحدة.")

st.markdown("---")

# --- الخانة الثالثة: نتائج التخصيم النهائي (القص) ---
if st.session_state.data:
    st.subheader("3️⃣ نتائج تخصيم القص (النتائج النهائية)")
    
    for i, u in enumerate(st.session_state.data):
        # معادلة التخصيم (حسب نوع الوحدة)
        h_cut = u['ارتفاع'] - 13 if u['النوع'] in ["سفلية", "دولاب"] else u['ارتفاع'] - 5
        w_cut = u['عرض'] - 5
        d_cut = u['عمق'] - 5
        
        # تنسيق عرض النتيجة في كارت منفصل لكل وحدة
        with st.expander(f"📋 تفاصيل قص: {u['الوحدة']}", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("**📏 مقاسات الألومنيوم:**")
                st.write(f"- الارتفاع (صافي): `{h_cut}` سم")
                st.write(f"- العرض (صافي): `{w_cut}` سم")
                st.write(f"- العمق (صافي): `{d_cut}` سم")
            with col_b:
                st.markdown("**🪵 مقاسات الفيبر:**")
                st.write(f"- الظهر: `{w_cut} × {h_cut}`")
                st.write(f"- الأرضية: `{w_cut} × {d_cut}`")
                if u['رفوف'] > 0:
                    st.write(f"- الرفوف (عدد {u['رفوف']}): `{w_cut-0.5} × {d_cut-0.5}`")

# --- زر الجرد النهائي ---
if st.session_state.data:
    st.markdown("---")
    if st.sidebar.button("📊 إظهار فاتورة الجرد النهائي"):
        st.sidebar.success("تم حساب الإجماليات بنجاح في الخلفية!")
        # هنا يمكنك إضافة حسابات الأمتار الإجمالية إذا أردت
        # --- 4. نظام الجرد النهائي والتقارير (Final Totals Report) ---
st.markdown("---")
st.subheader("4️⃣ التقرير الإجمالي للمشروع (الجرد النهائي)")

if st.session_state.data:
    col_report, col_summary = st.columns([2, 1])
    
    with col_report:
        # حسابات الجرد (منطق الحساب)
        total_m_linear = 0  # إجمالي أمتار الألومنيوم
        total_fiber_sq = 0   # إجمالي مساحة الفيبر
        
        for u in st.session_state.data:
            h_b = u['ارتفاع'] - 13 if u['النوع'] in ["سفلية", "دولاب"] else u['ارتفاع'] - 5
            w_b, d_b = u['عرض'] - 5, u['عمق'] - 5
            
            # حساب الأمتار الطولية للألومنيوم (تقريبي للورشة)
            total_m_linear += (h_b * 4) + (w_b * 4) + (d_b * 4)
            # حساب مساحة الفيبر بالمتر المربع
            total_fiber_sq += (w_b * h_b) + (w_b * d_b * 2) + (h_b * d_b * 2)

        # تحويل السنتيمتر إلى أمتار وأعواد
        total_m = total_m_linear / 100
        total_sticks = total_m / 6  # العود 6 متر
        total_sheets = (total_fiber_sq / 10000) / 3.6  # اللوح تقريباً 3.6 متر مربع
        
        st.info("💡 **ملخص الكميات المطلوبة للشراء:**")
        st.success(f"✅ ستحتاج إلى حوالي **{total_sticks:.1f}** عود ألومنيوم (طول 6م).")
        st.success(f"✅ ستحتاج إلى حوالي **{total_sheets:.1f}** لوح فيبر (مقاس قياسي).")

    with col_summary:
        st.write("📊 **إحصائيات سريعة:**")
        st.metric("عدد الوحدات", f"{len(st.session_state.data)} وحدة")
        st.metric("إجمالي الأمتار", f"{total_m:.1f} متر")

    # --- زر الطباعة أو الحفظ ---
    st.markdown("---")
    if st.button("🖨️ تجهيز التقرير للطباعة"):
        st.write("تم تجهيز البيانات، يمكنك الآن تصوير الشاشة أو حفظ الصفحة كـ PDF.")
else:
    st.warning("برجاء إضافة وحدات أولاً ليتمكن النظام من حساب الجرد.")

# --- تذييل الصفحة ---
st.markdown("<br><hr><center>نظام تخصيم الألومنيوم الذكي | 2026</center>", unsafe_allow_html=True)
