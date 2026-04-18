import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وتنسيق الواجهة لدعم العربية
st.set_page_config(page_title="نظام تخصيم الألومنيوم", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }
    .report-box {
        background-color: #f8f9fa;
        border-right: 5px solid #27ae60;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .total-card {
        background-color: #1e272e;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ نظام تخصيم الألومنيوم - نسخة الورشة النهائية")

# 2. تهيئة مخزن البيانات في الجلسة
if 'project_storage' not in st.session_state:
    st.session_state.project_storage = []

# 3. قسم المدخلات
st.header("📝 إدخال بيانات الوحدة")
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        unit_title = st.text_input("اسم الوحدة (مثال: علوية حوض)")
        unit_type = st.selectbox("نوع الوحدة", ["سفلية", "علوية", "دولاب خزين", "وحدة أخرى"])
    with col2:
        w = st.number_input("العرض الكلي (سم)", min_value=0.0, step=0.1, key='w')
        h = st.number_input("الارتفاع الكلي (سم)", min_value=0.0, step=0.1, key='h')
    with col3:
        d = st.number_input("العمق الكلي (سم)", min_value=0.0, step=0.1, key='d')

    with st.expander("➕ تخصيص (رفوف / فواصل / أدراج)"):
        c1, c2, c3 = st.columns(3)
        with c1:
            sh_w = st.number_input("عرض الرف", min_value=0.0)
            sh_d = st.number_input("عمق الرف", min_value=0.0)
            sh_n = st.number_input("عدد الرفوف", min_value=0)
        with c2:
            dv_h = st.number_input("ارتفاع الفاصل", min_value=0.0)
            dv_d = st.number_input("عمق الفاصل", min_value=0.0)
            dv_n = st.number_input("عدد الفواصل", min_value=0)
        with c3:
            dr_w = st.number_input("عرض الدرج", min_value=0.0)
            dr_d = st.number_input("عمق الدرج", min_value=0.0)
            dr_n = st.number_input("عدد الأدراج", min_value=0)

    if st.button("💾 إضافة الوحدة الحالية للجدول"):
        if w > 0 and h > 0:
            unit_data = {
                'الوحدة': unit_title or f"وحدة رقم {len(st.session_state.project_storage)+1}",
                'النوع': unit_type,
                'عرض': w, 'ارتفاع': h, 'عمق': d,
                'sh_w': sh_w, 'sh_d': sh_d, 'sh_n': sh_n,
                'dv_h': dv_h, 'dv_d': dv_d, 'dv_n': dv_n,
                'dr_w': dr_w, 'dr_d': dr_d, 'dr_n': dr_n
            }
            st.session_state.project_storage.append(unit_data)
            st.success("✅ تمت الإضافة")
        else:
            st.error("⚠️ يرجى إدخال الطول والعرض")

# 4. عرض البيانات والجرد التفصيلي
if st.session_state.project_storage:
    st.divider()
    st.header("📋 الوحدات المضافة للمشروع")
    df = pd.DataFrame(st.session_state.project_storage)
    st.dataframe(df[['الوحدة', 'النوع', 'عرض', 'ارتفاع', 'عمق']], use_container_width=True)

    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn2:
        if st.button("🗑️ مسح جميع البيانات", type="primary"):
            st.session_state.project_storage = []
            st.rerun()

    with col_btn1:
        if st.button("📊 جرد الخامات وبيان التقطيع التفصيلي"):
            st.header("📄 تقرير تقطيع الخامات")
            
            m_sum, t_sum, f_area = 0, 0, 0
            
            for u in st.session_state.project_storage:
                # منطق التخصيم الأصلي
                h_b = u['ارتفاع'] - 13 if u['النوع'] in ["سفلية", "دولاب خزين"] else u['ارتفاع'] - 5
                w_b, d_b = u['عرض'] - 5, u['عمق'] - 5
                
                with st.container():
                    st.markdown(f"""
                    <div class="report-box">
                        <strong>📦 الوحدة: {u['الوحدة']} ({u['النوع']})</strong><br>
                        📐 المقاس الكلي: {u['عرض']} × {u['ارتفاع']} × {u['عمق']}<br>
                        ---<br>
                        🪚 <b>ألومنيوم الهيكل:</b><br>
                        - الارتفاع: {h_b} سم (عدد 4 قطع)<br>
                        - العرض: {w_b} سم (عدد 4 قطع)<br>
                        - العمق: {d_b} سم (عدد 4 قطع)<br>
                        🪵 <b>الفيبر (التقطيع):</b><br>
                        - ضهرية: {w_b} × {h_b} (قطعة 1)<br>
                        - أرضية/سقف: {w_b} × {d_b} ({"قطعة 1" if u['النوع']=='سفلية' else "قطعتين"})<br>
                        - أجناب: {h_b} × {d_b} (قطعتين)
                    </div>
                    """, unsafe_allow_html=True)

                # الحسابات الإجمالية للوحدة
                if u['النوع'] == "سفلية":
                    m_sum += (h_b*2)+(w_b*3)+(d_b*2)
                    t_sum += (h_b*2)+(w_b*1)+(d_b*2)
                    f_u = (w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)
                else:
                    m_sum += (h_b*2)+(w_b*2)
                    t_sum += (h_b*2)+(w_b*2)+(d_b*4)
                    f_u = (w_b*h_b) + (w_b*d_b*2) + (h_b*d_b*2)
                
                f_area += f_u

                # حساب الإضافات (رفوف / فواصل / أدراج)
                if u['sh_n'] > 0:
                    m_sum += (u['sh_w']*2 + u['sh_d']*2) * u['sh_n']
                    f_area += (u['sh_w']-5)*(u['sh_d']-5)*u['sh_n']
                    st.write(f"🔹 رفوف ({u['sh_n']}): ألومنيوم {u['sh_w']} سم و {u['sh_d']} سم")

                if u['dv_n'] > 0:
                    m_sum += (u['dv_h']*2 + u['dv_d']*2) * u['dv_n']
                    f_area += (u['dv_h']-5)*(u['dv_d']-5)*u['dv_n']
                    st.write(f"🔹 فواصل ({u['dv_n']}): ألومنيوم {u['dv_h']} سم و {u['dv_d']} سم")

                if u['dr_n'] > 0:
                    m_sum += ((u['dr_w']-2.5)*2 + u['dr_d']*2) * u['dr_n']
                    st.write(f"🔹 أدراج ({u['dr_n']}): ألومنيوم عرض {u['dr_w']-2.5} سم وعمق {u['dr_d']} سم")

            # عرض الخلاصة النهائية للمشروع
            st.divider()
            st.header("💰 إجمالي خامات المشروع بالكامل")
            r1, r2, r3 = st.columns(3)
            with r1:
                st.metric("ألومنيوم مفرد (عود)", f"{m_sum/600:.2f}")
            with r2:
                st.metric("ألومنيوم متقارب (عود)", f"{t_sum/600:.2f}")
            with r3:
                st.metric("فيبر لوح (2.8*1.3)", f"{f_area/36400:.2f}")
