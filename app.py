import streamlit as st
import pandas as pd

# --- إعدادات الهوية الفنية (برمجة م/ ياسين علاء) ---
st.set_page_config(page_title="DOGGA SYSTEM | Yassin Alaa", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .main-header {
        background: linear-gradient(135deg, #1e272e 0%, #2c3e50 100%);
        color: #f1c40f; padding: 25px; border-radius: 15px;
        text-align: center; border-bottom: 5px solid #f1c40f;
    }
    .deduction-container {
        background-color: #f8f9fa; border-right: 10px solid #f39c12;
        padding: 20px; border-radius: 10px; margin-top: 10px;
        border: 1px solid #e0e0e0;
    }
    .metric-box {
        background: #1e272e; color: #f1c40f; padding: 15px;
        border-radius: 10px; text-align: center; font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'project_db' not in st.session_state:
    st.session_state.project_db = []

st.markdown('<div class="main-header"><h1>💎 منظومة DOGGA لبرمجة المطابخ</h1><p>إشراف هندسي: ياسين علاء</p></div>', unsafe_allow_html=True)

# --- [1] واجهة الإدخال الرئيسية ---
with st.expander("➕ إضافة وحدة جديدة للمشروع", expanded=True):
    with st.form("main_input", clear_on_submit=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: u_title = st.text_input("كود الوحدة")
        with c2: u_type = st.selectbox("النوع", ["سفلية", "علوية", "خزين"])
        with c3: qty = st.number_input("الكمية", min_value=1, value=1)
        
        m1, m2, m3 = st.columns(3)
        with m1: w = st.number_input("العرض الكلي", min_value=0.0)
        with m2: h = st.number_input("الارتفاع الكلي", min_value=0.0)
        with m3: d = st.number_input("العمق الكلي", min_value=0.0)
        
        st.write("---")
        st.write("⚙️ **إضافات الرفوف والأدراج:**")
        a1, a2, a3 = st.columns(3)
        with a1: sh_n = st.number_input("عدد الرفوف", 0)
        with a2: dv_n = st.number_input("عدد الفواصل", 0)
        with a3: dr_n = st.number_input("عدد الأدراج", 0)
        
        if st.form_submit_button("💾 حفظ الوحدة في النظام"):
            if w > 0 and h > 0:
                st.session_state.project_db.append({
                    "title": u_title, "type": u_type, "qty": qty,
                    "w": w, "h": h, "d": d,
                    "sh": sh_n, "dv": dv_n, "dr": dr_n
                })
                st.rerun()

# --- [2] الخانة الإضافية (بند التخصيمات والجرد) ---
if st.session_state.project_db:
    st.markdown("## 📐 قسم التخصيمات الفنية (Deductions)")
    
    total_fiber = 0
    total_alum = 0
    
    # تبويب لعرض التخصيمات بشكل منظم
    for idx, u in enumerate(st.session_state.project_db):
        # تطبيق معادلات م/ ياسين علاء المعتمدة
        h_ded = 13 if u['type'] != "علوية" else 5
        h_f, w_f, d_f = u['h'] - h_ded, u['w'] - 5, u['d'] - 5
        
        with st.container():
            st.markdown(f"""
            <div class="deduction-container">
                <h4>📦 الوحدة: {u['title']} | النوع: {u['type']} | العدد: {u['qty']}</h4>
                <p><b>📏 مقاسات تقطيع الألومنيوم:</b></p>
                <ul>
                    <li>القوائم (ارتفاع صافي): <b>{h_f} سم</b> (العدد الإجمالي: {u['qty']*4})</li>
                    <li>العوارض (عرض صافي): <b>{w_f} سم</b> (العدد الإجمالي: {u['qty']*4})</li>
                    <li>الأعماق (عمق صافي): <b>{d_f} سم</b> (العدد الإجمالي: {u['qty']*4})</li>
                </ul>
                <p><b>🪵 مقاسات الفيبر:</b> {w_f}×{h_f} (ضهرية) | {w_f}×{d_f} (أرضية)</p>
            </div>
            """, unsafe_allow_html=True)
            
            # حساب الخامات للجرد النهائي (الرفوف والفواصل تضرب في 2 ألومنيوم كما طلبت)
            u_alum = (h_f*4 + w_f*4 + d_f*4 + (u['sh']*w_f*2) + (u['dv']*h_f*2)) * u['qty']
            u_fiber = ((w_f*h_f) + (w_f*d_f) + (u['sh']*w_f*d_f)) * u['qty']
            total_alum += u_alum
            total_fiber += u_fiber

    # --- [3] فاتورة الخامات النهائية ---
    st.divider()
    st.markdown('<div class="metric-box">📊 إجمالي خامات المشروع بالكامل</div>', unsafe_allow_html=True)
    
    res1, res2, res3 = st.columns(3)
    with res1:
        st.metric("ألومنيوم (أعواد)", f"{total_alum/600:.2f}")
    with res2:
        st.metric("فيبر (ألواح)", f"{total_fiber/36400:.2f}")
    with res3:
        if st.button("🗑️ تفريغ كافة البيانات"):
            st.session_state.project_db = []
            st.rerun()

    # زر التحميل للطباعة
    df = pd.DataFrame(st.session_state.project_db)
    st.download_button("📥 تحميل كشف التقطيع", df.to_csv().encode('utf-8-sig'), "Deductions.csv")

st.markdown("<p style='text-align:center; color:#95a5a6; padding-top:50px;'>منظومة DOGGA لبرمجة الألمنيوم - م/ ياسين علاء © 2026</p>", unsafe_allow_html=True)
# --- [ إضافة: منطق حساب الرفوف والفواصل التفصيلي ] ---

if u['sh'] > 0:  # في حالة وجود رفوف
    st.markdown("#### 🧱 بند الرفوف")
    sh_w_final = w_final - 0.5  # خصم خلوص بسيط للرف
    sh_d_final = d_final - 0.5
    
    # حساب الألومنيوم: الرف له 2 عرض و 2 عمق، والعدد يضرب في 2 (حسب قاعدة المهندس ياسين)
    sh_alum_w = sh_w_final * (u['sh'] * 2)
    sh_alum_d = sh_d_final * (u['sh'] * 2)
    
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"• ألومنيوم العرض: {sh_w_final} سم (عدد {u['sh']*2} قطعة)")
        st.write(f"• ألومنيوم العمق: {sh_d_final} سم (عدد {u['sh']*2} قطعة)")
    with c2:
        st.write(f"• فيبر الرفوف: {sh_w_final - 0.5} × {sh_d_final - 0.5} (عدد {u['sh']} قطعة)")
    
    # إضافة للجرد العام
    total_alum_length += (sh_alum_w + sh_alum_d)
    total_fiber_area += (sh_w_final * sh_d_final) * u['sh']

if u['dv'] > 0:  # في حالة وجود فواصل رأسية
    st.markdown("#### 📐 بند الفواصل (Dividers)")
    dv_h_final = h_final - 0.5
    dv_d_final = d_final - 0.5
    
    # حساب الألومنيوم للفواصل
    dv_alum_h = dv_h_final * (u['dv'] * 2)
    dv_alum_d = dv_d_final * (u['dv'] * 2)
    
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"• ألومنيوم الارتفاع: {dv_h_final} سم (عدد {u['dv']*2} قطعة)")
        st.write(f"• ألومنيوم العمق: {dv_d_final} سم (عدد {u['dv']*2} قطعة)")
    with c2:
        st.write(f"• فيبر الفواصل: {dv_h_final - 0.5} × {dv_d_final - 0.5} (عدد {u['dv']} قطعة)")
    
    # إضافة للجرد العام
    total_alum_length += (dv_alum_h + dv_alum_d)
    total_fiber_area += (dv_h_final * dv_d_final) * u['dv']

# --- [ إضافة: بند الأدراج ] ---
if u['dr'] > 0:
    st.markdown("#### 🗄️ بند الأدراج")
    dr_w_final = w_final - 2.5 # تخصيم السكة
    dr_d_final = d_final - 2
    
    st.write(f"• تقطيع درج: عرض {dr_w_final} سم | عمق {dr_d_final} سم (عدد {u['dr']} درج)")
    total_alum_length += (dr_w_final * 2 + dr_d_final * 2) * u['dr']
