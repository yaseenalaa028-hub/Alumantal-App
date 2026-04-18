import streamlit as st
import pandas as pd

# 1. إعدادات الهوية البصرية (Kitchen Pro ERP)
st.set_page_config(page_title="Kitchen Pro ERP", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .hero-section {
        background: linear-gradient(135deg, #1e272e 0%, #2c3e50 100%);
        color: white; padding: 100px 20px; border-radius: 20px;
        text-align: center; margin-top: 50px; border-bottom: 8px solid #f1c40f;
    }
    .enter-btn button {
        background-color: #f1c40f !important; color: #1e272e !important;
        font-weight: bold !important; font-size: 24px !important;
        padding: 20px 50px !important; border-radius: 15px !important;
    }
    .unit-card {
        background: white; border-radius: 15px; padding: 25px;
        border-right: 12px solid #27ae60; box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 25px; border: 1px solid #e0e0e0;
    }
    .total-box {
        background:#1e272e; color:#f1c40f; padding:30px; border-radius:15px; 
        text-align:center; border:3px solid #f1c40f; margin-top:30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة التنقل بين الصفحات
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'db' not in st.session_state:
    st.session_state.db = []

# --- [ الواجهة الرئيسية المنفصلة ] ---
if not st.session_state.auth:
    st.markdown("""
        <div class="hero-section">
            <h1 style="font-size: 60px; margin-bottom: 20px;">💎 KITCHEN PRO ERP</h1>
            <p style="font-size: 24px; color: #dcdde1;">النظام السحابي المتطور لتخصيم المطابخ وإدارة الإنتاج</p>
            <br>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 دخول للنظام الفني", use_container_width=True, type="primary"):
            st.session_state.auth = True
            st.rerun()
    
    st.markdown("<p style='text-align:center; color:#7f8c8d; margin-top:50px;'>إصدار 2026 المعتمد للشركات الكبرى</p>", unsafe_allow_html=True)

# --- [ واجهة الشغل والتخصيم ] ---
else:
    col_head1, col_head2 = st.columns([8, 2])
    with col_head1:
        st.title("🛠️ لوحة التحكم في التشغيل")
    with col_head2:
        if st.button("🏠 تسجيل خروج"):
            st.session_state.auth = False
            st.rerun()

    st.divider()

    # نموذج الإدخال الثابت
    with st.expander("📝 إضافة وحدة تشغيل جديدة", expanded=True):
        c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
        u_name = c1.text_input("اسم الوحدة")
        u_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "أخرى"])
        qty = c3.number_input("العدد", min_value=1, value=1)
        
        m1, m2, m3 = st.columns(3)
        W = m1.number_input("العرض الكلي", min_value=0.0)
        H = m2.number_input("الارتفاع الكلي", min_value=0.0)
        D = m3.number_input("العمق الكلي", min_value=0.0)
        
        st.markdown("---")
        st.write("🧱 **الإضافات الفنية:**")
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

        if st.button("💾 حفظ الوحدة وتثبيت التخصيم", use_container_width=True):
            if W > 0 and H > 0:
                st.session_state.db.append({
                    'name': u_name, 'type': u_type, 'qty': qty, 'W': W, 'H': H, 'D': D,
                    'sh_n': sh_n, 'sh_w': sh_w, 'sh_d': sh_d,
                    'dv_n': dv_n, 'dv_h': dv_h, 'dv_d': dv_d,
                    'dr_n': dr_n, 'dr_w': dr_w, 'dr_d': dr_d
                })
                st.rerun()

    # محرك الحسابات (نفس المعادلات الصارمة)
    if st.session_state.db:
        st.divider()
        t_m, t_t, t_f = 0, 0, 0

        for idx, u in enumerate(st.session_state.db):
            h_ded = 13 if (u['type'] == "وحدة سفلية" or u['type'] == "دولاب خزين") else 5
            h_b, w_b, d_b = u['H'] - h_ded, u['W'] - 5, u['D'] - 5
            
            if u['type'] == "وحدة سفلية":
                u_m = (h_b * 2) + (w_b * 3) + (d_b * 2)
                u_t = (h_b * 2) + (w_b * 1) + (d_b * 2)
            else:
                u_m = (h_b * 2) + (w_b * 2)
                u_t = (h_b * 2) + (w_b * 2) + (d_b * 4)
            
            u_m += (u['sh_w'] * 4 + u['sh_d'] * 4) * u['sh_n']
            u_m += (u['dv_h'] * 4 + u['dv_d'] * 4) * u['dv_n']
            u_m += ((u['dr_w'] - 2.5) * 2 + u['dr_d'] * 2) * u['dr_n']

            f_u = (w_b * h_b) + (w_b * d_b) + (h_b * d_b * 2)
            f_u += (u['sh_w'] - 5) * (u['sh_d'] - 5) * u['sh_n'] if u['sh_n'] > 0 else 0
            f_u += (u['dv_h'] - 5) * (u['dv_d'] - 5) * u['dv_n'] if u['dv_n'] > 0 else 0
            
            t_m += u_m * u['qty']; t_t += u_t * u['qty']; t_f += f_u * u['qty']

            # عرض الجداول
            st.markdown(f'<div class="unit-card"><h3>📦 {u["name"]} | العدد: {u["qty"]}</h3>', unsafe_allow_html=True)
            ca, cb = st.columns(2)
            with ca:
                st.write("**📐 تخصيم الألومنيوم:**")
                st.table(pd.DataFrame({
                    "البند": ["ارتفاع", "عرض", "عمق"],
                    "مفرد": [f"2 * {h_b}", f"{'3' if u['type']=='وحدة سفلية' else '2'} * {w_b}", f"2 * {d_b}"],
                    "متقارب": [f"2 * {h_b}", f"{'1' if u['type']=='سفلية' else '2'} * {w_b}", f"{'2' if u['type']=='سفلية' else '4'} * {d_b}"]
                }))
            with cb:
                st.write("**🪵 تخصيم الفيبر:**")
                st.table(pd.DataFrame({
                    "الجزء": ["ضهرية", "أرضية", "أجناب"],
                    "المقاس": [f"{w_b} × {h_b}", f"{w_b} × {d_b}", f"{h_b} × {d_b} (×2)"]
                }))
            st.markdown('</div>', unsafe_allow_html=True)

        # الفاتورة الإجمالية
        st.markdown(f'<div class="total-box"><h2>📊 فاتورة خامات المشروع بالكامل</h2>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        r1.metric("مفرد (عود)", f"{t_m/600:.2f}")
        r2.metric("متقارب (عود)", f"{t_t/600:.2f}")
        r3.metric("فيبر (لوح)", f"{t_f/36400:.2f}")
        if st.button("🗑️ إفراغ المشروع"): st.session_state.db = []; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True) 
# --- [ تابع: واجهة الشغل والتخصيم ] ---
    # محرك الحسابات (المعادلات الصارمة المثبتة)
    if st.session_state.db:
        st.divider()
        st.subheader("📋 كشوف التخصيم وأوامر التشغيل")
        
        t_m, t_t, t_f = 0, 0, 0

        for idx, u in enumerate(st.session_state.db):
            # 1. معادلات تخصيم الهيكل (قانون الورشة)
            # السفلي والخزين يخصم 13 سم من الارتفاع، الباقي يخصم 5 سم
            h_ded = 13 if (u['type'] == "وحدة سفلية" or u['type'] == "دولاب خزين") else 5
            h_b, w_b, d_b = u['H'] - h_ded, u['W'] - 5, u['D'] - 5
            
            # 2. جرد الألومنيوم (سم طولي)
            if u['type'] == "وحدة سفلية":
                u_m = (h_b * 2) + (w_b * 3) + (d_b * 2)  # مفرد
                u_t = (h_b * 2) + (w_b * 1) + (d_b * 2)  # متقارب
            else:
                u_m = (h_b * 2) + (w_b * 2)              # مفرد
                u_t = (h_b * 2) + (w_b * 2) + (d_b * 4)  # متقارب
            
            # إضافة ألومنيوم الرفوف والفواصل (4 قطع مفرد لكل وحدة إضافية)
            u_m += (u['sh_w'] * 4 + u['sh_d'] * 4) * u['sh_n']
            u_m += (u['dv_h'] * 4 + u['dv_d'] * 4) * u['dv_n']
            # إضافة ألومنيوم الدرج (تخصيم 2.5 سم من العرض)
            u_m += ((u['dr_w'] - 2.5) * 2 + u['dr_d'] * 2) * u['dr_n']

            # 3. جرد الفيبر (سم مربع)
            f_u = (w_b * h_b) + (w_b * d_b) + (h_b * d_b * 2) # الهيكل الأساسي
            if u['sh_n'] > 0: 
                f_u += (u['sh_w'] - 5) * (u['sh_d'] - 5) * u['sh_n'] # الرفوف
            if u['dv_n'] > 0: 
                f_u += (u['dv_h'] - 5) * (u['dv_d'] - 5) * u['dv_n'] # الفواصل
            
            # تجميع الإجمالي الكلي مضروباً في كمية الوحدات
            t_m += u_m * u['qty']
            t_t += u_t * u['qty']
            t_f += f_u * u['qty']

            # --- عرض الجداول (كل وحدة في كارت مستقل) ---
            st.markdown(f"""
            <div class="unit-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:24px; font-weight:800; color:#1e272e;">📦 {u['name']}</span>
                    <span style="background:#27ae60; color:white; padding:8px 25px; border-radius:12px; font-weight:bold;">العدد: {u['qty']}</span>
                </div>
                <p style="color:#7f8c8d; font-weight:bold;">التصنيف: {u['type']} | المقاس الكلي: {u['W']} × {u['H']} × {u['D']}</p>
                <hr>
            """, unsafe_allow_html=True)
            
            col_alum, col_fiber = st.columns(2)
            
            with col_alum:
                st.markdown("**📐 تقطيع الألومنيوم (سم):**")
                alum_df = pd.DataFrame({
                    "البند": ["الارتفاع", "العرض", "العمق", "الإضافات"],
                    "مفرد (العدد * المقاس)": [
                        f"2 * {h_b}", 
                        f"{'3' if u['type']=='وحدة سفلية' else '2'} * {w_b}", 
                        f"2 * {d_b}", 
                        f"{(u['sh_n'] + u['dv_n']) * 4} قطع" if (u['sh_n'] + u['dv_n']) > 0 else "-"
                    ],
                    "متقارب (العدد * المقاس)": [
                        f"2 * {h_b}", 
                        f"{'1' if u['type']=='وحدة سفلية' else '2'} * {w_b}", 
                        f"{'2' if u['type']=='وحدة سفلية' else '4'} * {d_b}", 
                        "-"
                    ]
                })
                st.table(alum_df)

            with col_fiber:
                st.markdown("**🪵 تقطيع الفيبر (سم):**")
                fiber_df = pd.DataFrame({
                    "الجزء": ["الضهرية", "الأرضية", "الأجناب (×2)", "الرفوف/الفواصل"],
                    "المقاس التخصيمي": [
                        f"{w_b} × {h_b}", 
                        f"{w_b} × {d_b}", 
                        f"{h_b} × {d_b}", 
                        f"خصم 5 سم من المقاس اليدوي" if (u['sh_n'] + u['dv_n']) > 0 else "-"
                    ]
                })
                st.table(fiber_df)

            if u['dr_n'] > 0:
                st.info(f"📥 تخصيم الأدراج: تم اعتماد عرض الدرج {u['dr_w']-2.5} سم (تخصيم 2.5 سم ثابت).")
            
            st.markdown('</div>', unsafe_allow_html=True)

        # --- فاتورة الخامات النهائية ---
        st.markdown('<div class="total-box">', unsafe_allow_html=True)
        st.header("📊 فاتورة جرد الخامات (المشروع بالكامل)")
        res1, res2, res3 = st.columns(3)
        res1.metric("ألومنيوم مفرد (عـود 6م)", f"{t_m/600:.2f}")
        res2.metric("ألومنيوم متقارب (عـود 6م)", f"{t_t/600:.2f}")
        res3.metric("فيبر لوح (2.8 × 1.3)", f"{t_f/36400:.2f}")
        st.write("---")
        if st.button("🗑️ إفراغ قاعدة بيانات المشروع وبدء جديد", use_container_width=True):
            st.session_state.db = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("💡 النظام في انتظار إدخال مقاسات الوحدات للبدء في التخصيم.")
