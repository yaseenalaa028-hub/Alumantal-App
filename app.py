import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة - عرض كامل لتسهيل القراءة
st.set_page_config(page_title="نظام تخصيمات ورشة الألومنيوم PRO", layout="wide")

# 2. تنسيق الواجهة (CSS) لتناسب ذوق الورش الاحترافية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }
    .main-header {
        background-color: #2c3e50;
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    .unit-card {
        background-color: #ffffff;
        border-right: 12px solid #e67e22;
        padding: 25px;
        margin-bottom: 35px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        border: 1px solid #ddd;
    }
    .unit-title {
        font-size: 24px;
        color: #2c3e50;
        border-bottom: 2px solid #e67e22;
        padding-bottom: 10px;
        margin-bottom: 20px;
        font-weight: bold;
    }
    th { background-color: #34495e !important; color: white !important; text-align: center !important; font-size: 16px; }
    td { text-align: center !important; font-weight: bold !important; font-size: 17px !important; border: 1px solid #eee !important; }
    .total-box {
        background-color: #1e272e;
        color: #f1c40f;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        border: 3px solid #f1c40f;
        margin-top: 40px;
    }
    .stNumberInput label { font-size: 16px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. إدارة البيانات
if 'project' not in st.session_state:
    st.session_state.project = []

# رأس الصفحة
st.markdown('<div class="main-header"><h1>🏗️ نظام تخصيم الألومنيوم والفيبر (المعادلات الدقيقة)</h1></div>', unsafe_allow_html=True)

# 4. نموذج الإدخال الشامل (كل الخانات)
with st.expander("➕ إضافة وحدة جديدة للمشروع (اضغط هنا)", expanded=True):
    c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
    u_name = c1.text_input("اسم الوحدة (مثال: سفلي حوض)")
    u_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "وحدة أخرى"])
    u_W = c3.number_input("العرض الكلي (W)", min_value=0.0, format="%.1f")
    u_H = c4.number_input("الارتفاع الكلي (H)", min_value=0.0, format="%.1f")
    u_D = c5.number_input("العمق الكلي (D)", min_value=0.0, format="%.1f")

    st.markdown("---")
    st.write("🧱 **إضافات الأرفف والفواصل والأدراج:**")
    
    col_sh1, col_sh2, col_sh3 = st.columns(3)
    sh_n = col_sh1.number_input("عدد الأرفف", min_value=0, step=1)
    sh_w = col_sh2.number_input("عرض الرف اليدوي", min_value=0.0)
    sh_d = col_sh3.number_input("عمق الرف اليدوي", min_value=0.0)

    col_dv1, col_dv2, col_dv3 = st.columns(3)
    dv_n = col_dv1.number_input("عدد الفواصل", min_value=0, step=1)
    dv_h = col_dv2.number_input("ارتفاع الفاصل اليدوي", min_value=0.0)
    dv_d = col_dv3.number_input("عمق الفاصل اليدوي", min_value=0.0)

    col_dr1, col_dr2, col_dr3 = st.columns(3)
    dr_n = col_dr1.number_input("عدد الأدراج", min_value=0, step=1)
    dr_w = col_dr2.number_input("عرض الدرج اليدوي", min_value=0.0)
    dr_d = col_dr3.number_input("عمق الدرج اليدوي", min_value=0.0)

    if st.button("💾 حفظ الوحدة وحساب التخصيم فوراً", type="primary", use_container_width=True):
        if u_W > 0 and u_H > 0:
            st.session_state.project.append({
                'name': u_name or f"وحدة {len(st.session_state.project)+1}",
                'type': u_type, 'W': u_W, 'H': u_H, 'D': u_D,
                'sh_n': sh_n, 'sh_w': sh_w, 'sh_d': sh_d,
                'dv_n': dv_n, 'dv_h': dv_h, 'dv_d': dv_d,
                'dr_n': dr_n, 'dr_w': dr_w, 'dr_d': dr_d
            })
            st.rerun()

# 5. عرض النتائج (كل وحدة في جدول مستقل تحت بعضها)
if st.session_state.project:
    st.subheader("📋 شيت تفصيل الوحدات المضافة")
    
    total_mufard = 0
    total_mutaqarib = 0
    total_fiber_area = 0

    for idx, u in enumerate(st.session_state.project):
        # --- تطبيق المعادلات الخاصة بك ---
        # خصم الارتفاع: 13 سم للسفلي والخزين، 5 سم للباقي
        h_deduct = 13 if (u['type'] == "وحدة سفلية" or u['type'] == "دولاب خزين") else 5
        h_baky = u['H'] - h_deduct
        w_baky = u['W'] - 5
        d_baky = u['D'] - 5

        # حساب الألومنيوم (سم طولي)
        if u['type'] == "وحدة سفلية":
            m_u = (h_baky * 2) + (w_baky * 3) + (d_baky * 2)
            t_u = (h_baky * 2) + (w_baky * 1) + (d_baky * 2)
        else:
            m_u = (h_baky * 2) + (w_baky * 2)
            t_u = (h_baky * 2) + (w_baky * 2) + (d_baky * 4)
        
        # إضافة الأرفف والفواصل (كل واحد يضرب في 4 ألومنيوم مفرد حسب ملاحظتك)
        m_u += (u['sh_w'] * 4 if u['sh_n'] > 0 else 0) + (u['sh_d'] * 4 if u['sh_n'] > 0 else 0)
        m_u += (u['dv_h'] * 4 if u['dv_n'] > 0 else 0) + (u['dv_d'] * 4 if u['dv_n'] > 0 else 0)
        # تخصيم الدرج: عرض يخصم 2.5 والعمق كما هو
        m_u += (((u['dr_w']-2.5)*2) + (u['dr_d']*2)) * u['dr_n']

        # حساب الفيبر (سم مربع)
        f_dhara = w_baky * h_baky
        f_ardya = w_baky * d_baky
        f_ajnab = h_baky * d_baky * 2
        f_total_unit = f_dhara + f_ardya + f_ajnab
        
        # أرفف وفواصل فيبر (خصم 5 سم من العرض والعمق)
        f_raf_total = 0
        if u['sh_n'] > 0:
            f_raf_total = (u['sh_w'] - 5) * (u['sh_d'] - 5) * u['sh_n']
        
        f_fawasil_total = 0
        if u['dv_n'] > 0:
            f_fawasil_total = (u['dv_h'] - 5) * (u['dv_d'] - 5) * u['dv_n']
            
        f_total_unit += f_raf_total + f_fawasil_total

        total_mufard += m_u
        total_mutaqarib += t_u
        total_fiber_area += f_total_unit

        # --- رسم جدول الوحدة ---
        st.markdown(f'<div class="unit-card"><div class="unit-title">📦 {u["name"]} ({u["type"]})</div>', unsafe_allow_html=True)
        
        # جدول الألومنيوم
        st.write("**📐 مقاسات تقطيع الألومنيوم:**")
        alum_data = {
            "البيان": ["الارتفاع", "العرض", "العمق", "الفواصل/الأرفف"],
            "مفرد (العدد * المقاس)": [f"2 * {h_baky}", f"{'3' if u['type']=='وحدة سفلية' else '2'} * {w_baky}", f"2 * {d_baky}", f"{(u['sh_n']+u['dv_n'])*4} قطعة"],
            "متقارب (العدد * المقاس)": [f"2 * {h_baky}", f"{'1' if u['type']=='وحدة سفلية' else '2'} * {w_baky}", f"{'2' if u['type']=='وحدة سفلية' else '4'} * {d_baky}", "-"]
        }
        st.table(pd.DataFrame(alum_data))

        # جدول الفيبر
        st.write("**🪵 مقاسات تقطيع الفيبر:**")
        fiber_data = {
            "الجزء": ["الضهرية", "الأرضية", "الأجناب (قطعتين)", "الرفوف", "الفواصل"],
            "المقاس النهائي": [f"{w_baky} × {h_baky}", f"{w_baky} × {d_baky}", f"{h_baky} × {d_baky}", 
                              f"{u['sh_w']-5} × {u['sh_d']-5}" if u['sh_n']>0 else "-",
                              f"{u['dv_h']-5} × {u['dv_d']-5}" if u['dv_n']>0 else "-"]
        }
        st.table(pd.DataFrame(fiber_data))
        
        if u['dr_n'] > 0:
            st.warning(f"📥 ملحوظة للأدراج: تم تخصيم 2.5 سم من العرض (مقاس الدرج: {u['dr_w']-2.5} سم)")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # 6. الفاتورة الإجمالية للجرد
    st.markdown('<div class="total-box">', unsafe_allow_html=True)
    st.header("📊 إجمالي خامات المشروع (فاتورة الجرد)")
    res_c1, res_c2, res_c3 = st.columns(3)
    res_c1.metric("ألومنيوم مفرد (عـود 6م)", f"{total_mufard/600:.2f}")
    res_c2.metric("ألومنيوم متقارب (عـود 6م)", f"{total_mutaqarib/600:.2f}")
    res_c3.metric("فيبر لوح (2.8x1.3)", f"{total_fiber_area/36400:.2f}")
    
    if st.button("🗑️ مسح المشروع وإفراغ البيانات", use_container_width=True):
        st.session_state.project = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("💡 المشروع فارغ حالياً.. ابدأ بإضافة أول وحدة من القائمة بالأعلى.")
