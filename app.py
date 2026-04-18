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
# --- [ تابع: قسم التخصيمات والجرد التفصيلي ] ---

if st.session_state.project_db:
    st.markdown("---")
    st.header("📏 بند التخصيمات والماتريال (Deductions)")

    # إعداد قوائم لتجميع البيانات النهائية للجرد
    all_cuts = []
    total_fiber_area = 0
    total_alum_length = 0

    for idx, u in enumerate(st.session_state.project_db):
        # 1. معادلات م/ ياسين علاء الأساسية
        h_deduct = 13 if u['type'] != "علوية" else 5
        h_final = u['h'] - h_deduct
        w_final = u['w'] - 5
        d_final = u['d'] - 5
        
        # 2. حسابات الألومنيوم (قوائم + عوارض + أعماق)
        # القوائم والعوارض والأعماق (4 قطع من كل نوع لكل وحدة)
        u_alum = (h_final * 4 + w_final * 4 + d_final * 4)
        
        # 3. حسابات الإضافات (الرفوف والفواصل تضرب في 2 حسب طلبك)
        sh_alum = (u['sh'] * w_final * 2) + (u['sh'] * d_final * 2)
        dv_alum = (u['dv'] * h_final * 2) + (u['dv'] * d_final * 2)
        
        # 4. حسابات الفيبر
        # ضهرية (1) + أرضية (1) + أجناب (2)
        u_fiber = (w_final * h_final) + (w_final * d_final) + (h_final * d_final * 2)
        # أضف فيبر الرفوف والفواصل
        u_fiber += (u['sh'] * w_final * d_final) + (u['dv'] * h_final * d_final)

        # تجميع البيانات لعرضها في كارت الوحدة
        with st.expander(f"🔍 تفاصيل تقطيع: {u['title']} ({u['type']})", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                st.write("**✂️ تقطيع الألومنيوم (صافي):**")
                st.write(f"- ارتفاع (قوائم): {h_final} سم")
                st.write(f"- عرض (عوارض): {w_final} سم")
                st.write(f"- عمق (أعماق): {d_final} سم")
                if u['sh'] > 0: st.write(f"- ألومنيوم رفوف: {u['sh'] * 2} قطعة")
                if u['dr'] > 0: st.write(f"- أدراج: {u['dr']} درج")
            
            with c2:
                st.write("**🪵 تقطيع الفيبر:**")
                st.write(f"- ضهرية: {w_final} × {h_final}")
                st.write(f"- أرضية: {w_final} × {d_final}")
                st.write(f"- أجناب: {h_final} × {d_final} (عدد 2)")

        # إرسال البيانات للجرد العام
        total_alum_length += (u_alum + sh_alum + dv_alum) * u['qty']
        total_fiber_area += u_fiber * u['qty']

    # --- [ القسم الأخير: ملخص الخامات المطلوب شراؤها ] ---
    st.markdown("### 🛒 إجمالي الطلبية (خامات المشروع)")
    
    col_fin1, col_fin2, col_fin3 = st.columns(3)
    
    with col_fin1:
        st.info(f"**إجمالي الألومنيوم:**\n\n {total_alum_length/100:.2f} متر طولي")
        st.write(f"≈ {total_alum_length/600:.2f} عود (6 متر)")
        
    with col_fin2:
        st.success(f"**إجمالي الفيبر:**\n\n {total_fiber_area/10000:.2f} متر مربع")
        st.write(f"≈ {total_fiber_area/36400:.2f} لوح (2.8*1.3)")

    with col_fin3:
        st.warning(f"**إجمالي الوحدات:**\n\n {len(st.session_state.project_db)} وحدات")
        st.write(f"إجمالي قطع المشروع: {sum([x['qty'] for x in st.session_state.project_db])}")

    # زر مسح الجدول لبدء مشروع جديد
    if st.button("❌ مسح كافة البيانات وبدء مشروع جديد"):
        st.session_state.project_db = []
        st.rerun()

# التوقيع النهائي للمنظومة
st.markdown("<br><br><p style='text-align:center; color:#7f8c8d; font-size:12px;'>DOGGA SYSTEM V2.0 | Developed by Eng. Yassin Alaa</p>", unsafe_allow_html=True)
