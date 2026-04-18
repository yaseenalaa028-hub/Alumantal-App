import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات النظام المتقدمة - م/ ياسين علاء
st.set_page_config(page_title="Kitchen Pro ERP | Yassin Alaa", layout="wide")

# تصميم واجهة احترافية جداً CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .main { background-color: #f8f9fa; }
    .hero-section {
        background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%);
        color: white; padding: 50px 20px; border-radius: 20px;
        text-align: center; border-bottom: 8px solid #f1c40f; box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .engineer-tag {
        color: #f1c40f; font-size: 32px; font-weight: 900; margin-top: 10px;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.6);
    }
    .unit-card {
        background: white; border-radius: 15px; padding: 25px;
        border-right: 15px solid #f39c12; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 30px; border: 1px solid #eef0f2;
    }
    .total-box {
        background: #1e272e; color: #f1c40f; padding: 30px; border-radius: 15px;
        text-align: center; border: 2px solid #f1c40f; margin-top: 30px;
    }
    .stats-card {
        background: #2c3e50; color: white; padding: 15px; border-radius: 10px; text-align: center;
    }
    th { background-color: #2c3e50 !important; color: white !important; }
    td { font-weight: bold !important; text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة (State Management)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'db' not in st.session_state: st.session_state.db = []

# --- [ واجهة الدخول ] ---
if not st.session_state.auth:
    st.markdown(f"""
        <div class="hero-section">
            <h1 style="font-size: 60px; margin-bottom: 0;">💎 KITCHEN PRO ERP</h1>
            <div class="engineer-tag">برمجة المهندس ياسين علاء</div>
            <p style="font-size: 22px; color: #bdc3c7; margin-top: 15px;">نظام الإدارة الصناعية المتكامل للتخصيم والجرد - 2026</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    _, col_btn, _ = st.columns([1, 0.6, 1])
    with col_btn:
        if st.button("🔓 الدخول إلى لوحة التشغيل", use_container_width=True):
            st.session_state.auth = True
            st.rerun()

# --- [ واجهة العمل الداخلية ] ---
else:
    st.markdown(f"<div style='text-align:left; color:#f39c12; font-weight:bold;'>المطور الفني: م/ ياسين علاء</div>", unsafe_allow_html=True)
    col_h1, col_h2 = st.columns([8, 2])
    with col_h1: st.title("🛠️ تخصيم وإدارة جرد المشاريع")
    with col_h2: 
        if st.button("🏠 تسجيل الخروج"): 
            st.session_state.auth = False
            st.rerun()

    # نموذج الإدخال
    with st.expander("📝 إضافة وحدة جديدة - تفاصيل فنية", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        u_name = c1.text_input("اسم/كود الوحدة")
        u_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "أدراج"])
        qty = c3.number_input("الكمية", min_value=1, value=1)
        
        m1, m2, m3 = st.columns(3)
        W = m1.number_input("العرض (سم)", min_value=0.0)
        H = m2.number_input("الارتفاع (سم)", min_value=0.0)
        D = m3.number_input("العمق (سم)", min_value=0.0)

        st.markdown("---")
        ex1, ex2, ex3 = st.columns(3)
        sh_n = ex1.number_input("الرفوف", 0)
        dv_n = ex2.number_input("الفواصل", 0)
        dr_n = ex3.number_input("الأدراج", 0)

        if st.button("📥 اعتماد الوحدة", use_container_width=True):
            if not u_name or W <= 0 or H <= 0:
                st.error("⚠️ يرجى إدخال كافة البيانات الصحيحة")
            else:
                st.session_state.db.append({
                    'name': u_name, 'type': u_type, 'qty': qty, 'W': W, 'H': H, 'D': D,
                    'sh_n': sh_n, 'dv_n': dv_n, 'dr_n': dr_n
                })
                st.rerun()

    # الحسابات والجرد
    if st.session_state.db:
        t_m, t_t, t_f = 0, 0, 0
        t_hinges, t_handles = 0, 0

        for u in st.session_state.db:
            # قانون التخصيم (13 سم للسفلي و 5 سم للعلوي)
            h_ded = 13 if ("سفلية" in u['type'] or "خزين" in u['type']) else 5
            h_f, w_f, d_f = u['H'] - h_ded, u['W'] - 5, u['D'] - 5
            
            # حساب الألومنيوم والفيبر
            u_m = (h_f*2 + w_f*3 + d_f*2) if "سفلية" in u['type'] else (h_f*2 + w_f*2 + d_f*2)
            f_unit = (w_f*h_f) + (w_f*d_f) + (h_f*d_f*2)
            
            t_m += u_m * u['qty']; t_f += f_unit * u['qty']
            t_hinges += 4 * u['qty']; t_handles += (u['dr_n'] + 1) * u['qty']

            # عرض كارت الوحدة
            st.markdown(f"""
            <div class="unit-card">
                <h3>📦 {u['name']} ({u['type']}) - العدد: {u['qty']}</h3>
                <p><b>مقاسات التقطيع:</b> ارتفاع: {h_f} سم | عرض: {w_f} سم | عمق: {d_f} سم</p>
            </div>
            """, unsafe_allow_html=True)

        # الفاتورة النهائية
        st.markdown(f"""
        <div class="total-box">
            <h2>📊 إجمالي خامات المشروع - م/ ياسين علاء</h2>
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                <div class="stats-card"><h3>{t_m/600:.2f}</h3><p>ألومنيوم (عود)</p></div>
                <div class="stats-card"><h3>{t_f/36400:.2f}</h3><p>فيبر (لوح)</p></div>
                <div class="stats-card"><h3>{t_handles}</h3><p>مقابض</p></div>
            </div>
            <br><button onclick="window.print()">🖨️ طباعة التقرير</button>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ مسح الكل"):
            st.session_state.db = []
            st.rerun()

st.markdown("<br><p style='text-align:center; color:#bdc3c7;'>برمجة المهندس ياسين علاء © 2026</p>", unsafe_allow_html=True)
