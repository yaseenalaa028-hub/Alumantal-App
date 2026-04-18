import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الهوية البصرية للشركة (تليق بشركة كبيرة)
st.set_page_config(page_title="Kitchen Pro ERP", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .main { background-color: #f4f7f6; }
    .header-style { 
        background: linear-gradient(90deg, #1e272e, #2c3e50);
        color: #f1c40f; padding: 30px; border-radius: 15px; 
        text-align: center; margin-bottom: 30px; border-bottom: 5px solid #f1c40f;
    }
    .unit-card {
        background: white; border-radius: 15px; padding: 25px;
        border-right: 12px solid #27ae60; box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 25px; border: 1px solid #e0e0e0;
    }
    .stNumberInput label { font-weight: bold !important; color: #2c3e50 !important; }
    th { background-color: #2c3e50 !important; color: white !important; font-size: 16px !important; }
    td { font-size: 16px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

if 'db' not in st.session_state: st.session_state.db = []

st.markdown('<div class="header-style"><h1>💎 KITCHEN PRO ERP</h1><p>نظام إدارة الإنتاج والتقطيع الفني المتطور</p></div>', unsafe_allow_html=True)

# 2. نموذج الإدخال (البيانات الأساسية + الإضافات)
with st.expander("📝 إضافة وحدة تشغيل جديدة", expanded=True):
    col1, col2, col3 = st.columns([2, 1, 1])
    u_name = col1.text_input("اسم الوحدة (كود الوحدة)")
    u_type = col2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "أخرى"])
    qty = col3.number_input("العدد (الكمية)", min_value=1, value=1)
    
    m1, m2, m3 = st.columns(3)
    W = m1.number_input("العرض الكلي (W)", min_value=0.0)
    H = m2.number_input("الارتفاع الكلي (H)", min_value=0.0)
    D = m3.number_input("العمق الكلي (D)", min_value=0.0)
    
    st.markdown("---")
    st.write("🧱 **الإضافات الفنية (الرفوف - الفواصل - الأدراج):**")
    
    sh_c1, sh_c2, sh_c3 = st.columns(3)
    sh_n = sh_c1.number_input("عدد الرفوف", 0)
    sh_w = sh_c2.number_input("عرض الرف", 0.0)
    sh_d = sh_c3.number_input("عمق الرف", 0.0)

    dv_c1, dv_c2, dv_c3 = st.columns(3)
    dv_n = dv_c1.number_input("عدد الفواصل", 0)
    dv_h = dv_c2.number_input("ارتفاع الفاصل", 0.0)
    dv_d = dv_c3.number_input("عمق الفاصل", 0.0)

    dr_c1, dr_c2, dr_c3 = st.columns(3)
    dr_n = dr_c1.number_input("عدد الأدراج", 0)
    dr_w = dr_c2.number_input("عرض الدرج", 0.0)
    dr_d = dr_c3.number_input("عمق الدرج", 0.0)

    if st.button("إرسال لأمر التشغيل 🛠️", use_container_width=True):
        if W > 0 and H > 0:
            st.session_state.db.append({
                'name': u_name or f"UNIT-{len(st.session_state.db)+1}",
                'type': u_type, 'qty': qty, 'W': W, 'H': H, 'D': D,
                'sh_n': sh_n, 'sh_w': sh_w, 'sh_d': sh_d,
                'dv_n': dv_n, 'dv_h': dv_h, 'dv_d': dv_d,
                'dr_n': dr_n, 'dr_w': dr_w, 'dr_d': dr_d
            })
            st.rerun()# 3. محرك الحسابات وعرض أوامر التشغيل
if st.session_state.db:
    st.divider()
    st.subheader("📋 كشوف التخصيم وأوامر الإنتاج")
    
    total_m, total_t, total_f = 0, 0, 0

    for idx, u in enumerate(st.session_state.db):
        # تطبيق معادلات التخصيم الصارمة
        h_deduct = 13 if (u['type'] == "وحدة سفلية" or u['type'] == "دولاب خزين") else 5
        h_b, w_b, d_b = u['H'] - h_deduct, u['W'] - 5, u['D'] - 5
        
        # حساب جرد الألومنيوم للوحدة الواحدة
        if u['type'] == "وحدة سفلية":
            u_m = (h_b * 2) + (w_b * 3) + (d_b * 2)
            u_t = (h_b * 2) + (w_b * 1) + (d_b * 2)
        else:
            u_m = (h_b * 2) + (w_b * 2)
            u_t = (h_b * 2) + (w_b * 2) + (d_b * 4)
        
        # حساب ألومنيوم الإضافات (مفرد × 4 لكل قطعة)
        u_m += (u['sh_w'] * 4 + u['sh_d'] * 4) * u['sh_n']
        u_m += (u['dv_h'] * 4 + u['dv_d'] * 4) * u['dv_n']
        u_m += ((u['dr_w'] - 2.5) * 2 + u['dr_d'] * 2) * u['dr_n']

        # حساب جرد الفيبر للوحدة الواحدة
        f_u = (w_b * h_b) + (w_b * d_b) + (h_b * d_b * 2)
        if u['sh_n'] > 0: f_u += (u['sh_w'] - 5) * (u['sh_d'] - 5) * u['sh_n']
        if u['dv_n'] > 0: f_u += (u['dv_h'] - 5) * (u['dv_d'] - 5) * u['dv_n']
        
        # الإجمالي الكلي للمشروع (مضروب في الكمية)
        total_m += u_m * u['qty']
        total_t += u_t * u['qty']
        total_f += f_u * u['qty']

        # عرض الكارت الفني للوحدة
        st.markdown(f"""
        <div class="unit-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:22px; font-weight:800; color:#2c3e50;">📦 {u['name']} | {u['type']}</span>
                <span style="background:#27ae60; color:white; padding:5px 20px; border-radius:10px;">العدد المطلوب: {u['qty']}</span>
            </div>
            <hr>
        """, unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**📐 تقطيع الألومنيوم للوحدة (سم):**")
            df_alum = pd.DataFrame({
                "البند": ["الارتفاع", "العرض", "العمق", "الإضافات"],
                "مفرد (العدد * المقاس)": [f"2 * {h_b}", f"{'3' if u['type']=='وحدة سفلية' else '2'} * {w_b}", f"2 * {d_b}", f"{(u['sh_n']+u['dv_n'])*4} قطع"],
                "متقارب (العدد * المقاس)": [f"2 * {h_b}", f"{'1' if u['type']=='وحدة سفلية' else '2'} * {w_b}", f"{'2' if u['type']=='وحدة سفلية' else '4'} * {d_b}", "-"]
            })
            st.table(df_alum)
            
        with col_b:
            st.markdown("**🪵 تقطيع الفيبر للوحدة (سم):**")
            df_fiber = pd.DataFrame({
                "الجزء": ["الضهرية", "الأرضية", "الأجناب (×2)", "الرفوف/الفواصل"],
                "المقاس النهائي": [f"{w_b} × {h_b}", f"{w_b} × {d_b}", f"{h_b} × {d_b}", 
                                  f"خصم 5 سم من المقاس اليدوي" if (u['sh_n']+u['dv_n'])>0 else "-"]
            })
            st.table(df_fiber)
        
        if u['dr_n'] > 0:
            st.warning(f"⚠️ تنبيه فني: يتم تخصيم 2.5 سم من عرض درج الألومنيوم والفيبر (المقاس: {u['dr_w']-2.5} سم)")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. التقرير الختامي للمخازن
    st.markdown('<div style="background:#1e272e; color:#f1c40f; padding:30px; border-radius:15px; text-align:center; border:3px solid #f1c40f; margin-top:30px;">', unsafe_allow_html=True)
    st.header("📊 فاتورة إجمالي خامات المشروع")
    res1, res2, res3 = st.columns(3)
    res1.metric("ألومنيوم مفرد (عـود 6م)", f"{total_m/600:.2f}")
    res2.metric("ألومنيوم متقارب (عـود 6م)", f"{total_t/600:.2f}")
    res3.metric("فيبر لوح (2.8×1.3)", f"{total_f/36400:.2f}")
    
    st.write("---")
    if st.button("🗑️ مسح المشروع الحالي وبدء مشروع جديد", use_container_width=True):
        st.session_state.db = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("💡 النظام جاهز.. يرجى إضافة مقاسات الوحدات من القائمة بالأعلى لبدء التخصيم.")
