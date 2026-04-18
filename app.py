import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الهوية البصرية الصارمة - م/ ياسين علاء
st.set_page_config(page_title="Kitchen Pro ERP | Yassin Alaa", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .hero-section {
        background: linear-gradient(135deg, #0f141a 0%, #2c3e50 100%);
        color: white; padding: 80px 20px; border-radius: 25px;
        text-align: center; border-bottom: 10px solid #f1c40f;
    }
    .engineer-tag {
        color: #f1c40f; font-size: 30px; font-weight: 900; margin-top: 15px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .unit-card {
        background: white; border-radius: 15px; padding: 25px;
        border-right: 12px solid #f39c12; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px; border: 1px solid #eee;
    }
    .total-box {
        background:#1e272e; color:#f1c40f; padding:30px; border-radius:15px; 
        text-align:center; border:3px solid #f1c40f; margin-top:30px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'db' not in st.session_state: st.session_state.db = []

# --- الواجهة الخارجية ---
if not st.session_state.auth:
    st.markdown(f"""
        <div class="hero-section">
            <h1 style="font-size: 60px;">💎 KITCHEN PRO ERP</h1>
            <div class="engineer-tag">برمجة المهندس ياسين علاء</div>
            <p style="font-size: 20px; color: #bdc3c7; margin-top: 20px;">الإصدار المعتمد 2026 - نظام تخصيم الألومنيوم والفيبر</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    _, col_btn, _ = st.columns([1, 0.8, 1])
    with col_btn:
        if st.button("🔓 الدخول إلى لوحة التحكم الفنية", use_container_width=True):
            st.session_state.auth = True
            st.rerun()
            # --- واجهة العمل الداخلية ---
else:
    st.markdown(f"<div style='text-align:left; color:#f39c12; font-weight:bold;'>المطور: م/ ياسين علاء</div>", unsafe_allow_html=True)
    col_h1, col_h2 = st.columns([8, 2])
    with col_h1: st.title("🛠️ تخصيم المشاريع والجرد الدقيق")
    with col_h2: 
        if st.button("🚪 تسجيل الخروج"): 
            st.session_state.auth = False
            st.rerun()

    with st.expander("📝 إضافة وحدة جديدة للمشروع", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        u_name = c1.text_input("اسم أو كود الوحدة (يجب أن يكون فريداً)")
        u_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "أخرى"])
        qty = c3.number_input("الكمية المطلوبة", min_value=1, value=1)
        
        m1, m2, m3 = st.columns(3)
        W = m1.number_input("العرض الكلي (سم)", min_value=0.0)
        H = m2.number_input("الارتفاع الكلي (سم)", min_value=0.0)
        D = m3.number_input("العمق الكلي (سم)", min_value=0.0)

        st.markdown("---")
        ex1, ex2, ex3, ex4 = st.columns(4)
        sh_n = ex1.number_input("عدد الرفوف", 0)
        dv_n = ex2.number_input("عدد الفواصل", 0)
        dr_n = ex3.number_input("عدد الأدراج", 0)
        dr_w = ex4.number_input("عرض الدرج اليدوي", 0.0)

        # منطق منع التكرار
        existing_names = [u['name'] for u in st.session_state.db]

        if st.button("💾 حفظ الوحدة وتثبيت التخصيم", use_container_width=True):
            if not u_name:
                st.error("⚠️ يرجى تسمية الوحدة أولاً")
            elif u_name in existing_names:
                st.error(f"⚠️ خطأ: الاسم '{u_name}' موجود بالفعل. م/ ياسين يمنع تكرار الأكواد.")
            elif W <= 0 or H <= 0:
                st.error("⚠️ يرجى مراجعة المقاسات")
            else:
                st.session_state.db.append({
                    'name': u_name, 'type': u_type, 'qty': qty, 
                    'W': W, 'H': H, 'D': D,
                    'sh_n': sh_n, 'dv_n': dv_n, 'dr_n': dr_n, 'dr_w': dr_w
                })
                st.success(f"تمت إضافة {u_name} بنجاح ✅")
                st.rerun()
                # محرك الحسابات الفنية (تأكد من المحاذاة مع الـ else)
    if st.session_state.db:
        st.divider()
        total_m, total_t, total_f = 0, 0, 0
        total_joints, total_handles, total_hinges = 0, 0, 0

        for u in st.session_state.db:
            # معادلات تخصيم م/ ياسين علاء الصارمة
            h_ded = 13 if (u['type'] == "وحدة سفلية" or u['type'] == "دولاب خزين") else 5
            h_b, w_b, d_b = u['H'] - h_ded, u['W'] - 5, u['D'] - 5
            
            # حساب الألومنيوم للهيكل
            if u['type'] == "وحدة سفلية":
                u_m = (h_b*2 + w_b*3 + d_b*2); u_t = (h_b*2 + w_b*1 + d_b*2)
            else:
                u_m = (h_b*2 + w_b*2); u_t = (h_b*2 + w_b*2 + d_b*4)
            
            # إضافة تخصيمات الرفوف والفواصل (مفرد)
            u_m += (u['sh_n'] * 4 * (u['W']-5)) + (u['dv_n'] * 4 * (u['H']-h_ded))
            if u['dr_n'] > 0:
                u_m += ((u['dr_w']-2.5)*2 + d_b*2) * u['dr_n']

            # حساب الفيبر
            f_u = (w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)
            if u['sh_n'] > 0: f_u += (u['W']-10) * (u['D']-10) * u['sh_n']
            
            # تراكم الجرد الإجمالي
            total_m += u_m * u['qty']; total_t += u_t * u['qty']; total_f += f_u * u['qty']
            total_joints += 8 * u['qty']
            total_handles += (u['dr_n'] if u['dr_n'] > 0 else 1) * u['qty']
            total_hinges += 4 * u['qty']

            # عرض كارت الوحدة
            st.markdown(f'<div class="unit-card"><h3>📦 الوحدة: {u["name"]} | إشراف م/ ياسين علاء</h3>', unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**📐 تفصيل الألومنيوم (سم):**")
                st.table(pd.DataFrame({"القطعة": ["الارتفاع", "العرض", "العمق"], "مفرد": [h_b, w_b, d_b], "متقارب": [h_b, w_b, d_b]}))
            with col_b:
                st.write("**🪵 تفصيل الفيبر (سم):**")
                st.table(pd.DataFrame({"الجزء": ["الضهرية", "الأرضية", "الأجناب"], "المقاس": [f"{w_b}×{h_b}", f"{w_b}×{d_b}", f"{h_b}×{d_b}"]}))
            st.markdown('</div>', unsafe_allow_html=True)
            # الفاتورة الإجمالية للجرد
        st.markdown(f'<div class="total-box"><h2>📊 فاتورة خامات المشروع - م/ ياسين علاء</h2>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        r1.metric("إجمالي المفرد (عود 6م)", f"{total_m/600:.2f}")
        r2.metric("إجمالي المتقارب (عود 6م)", f"{total_t/600:.2f}")
        r3.metric("إجمالي الفيبر (لوح)", f"{total_f/36400:.2f}")
        
        st.divider()
        st.write("**⚙️ جرد الإكسسوارات:**")
        ix1, ix2, ix3 = st.columns(3)
        ix1.write(f"✅ زوايا تجميع: {total_joints} قطعة")
        ix2.write(f"✅ مقابض: {total_handles} قطعة")
        ix3.write(f"✅ مفصلات: {total_hinges} قطعة")
        
        if st.button("🗑️ مسح كافة البيانات لبدء مشروع جديد"): 
            st.session_state.db = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# تذييل الصفحة الثابت
st.markdown("<br><br><p style='text-align:center; color:#bdc3c7;'>جميع الحقوق محفوظة - برمجة المهندس ياسين علاء © 2026</p>", unsafe_allow_html=True)
