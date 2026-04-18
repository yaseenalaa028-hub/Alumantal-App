import streamlit as st
import pandas as pd

# 1. إعدادات الهوية البصرية (تصميم فخم يليق بشركة كبرى)
st.set_page_config(page_title="Kitchen Pro ERP | ياسين علاء", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    .hero-section {
        background: linear-gradient(135deg, #0f141a 0%, #2c3e50 100%);
        color: white; padding: 120px 20px; border-radius: 25px;
        text-align: center; border-bottom: 10px solid #f1c40f; box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .engineer-tag {
        color: #f1c40f; font-size: 28px; font-weight: 900; margin-top: 20px;
        letter-spacing: 2px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .unit-card {
        background: white; border-radius: 15px; padding: 25px;
        border-right: 12px solid #f39c12; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px; border: 1px solid #eee;
    }
    .footer-credit {
        text-align: center; color: #95a5a6; padding: 20px; font-size: 14px;
        border-top: 1px solid #eee; margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'db' not in st.session_state: st.session_state.db = []

# --- [ الواجهة الخارجية: صفحة الدخول ] ---
if not st.session_state.auth:
    st.markdown(f"""
        <div class="hero-section">
            <h1 style="font-size: 70px; margin-bottom: 10px;">💎 KITCHEN PRO ERP</h1>
            <div class="engineer-tag">برمجة المهندس ياسين علاء</div>
            <p style="font-size: 22px; color: #bdc3c7; margin-top: 20px;">النظام المعتمد لإدارة جرد وتخصيم الألومنيوم والفيبر</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    c1, c2, c3 = st.columns([1.2, 1, 1.2])
    with c2:
        if st.button("🔓 الدخول إلى منصة التشغيل", use_container_width=True):
            st.session_state.auth = True
            st.rerun()
    
    st.markdown("<div class='footer-credit'>جميع الحقوق محفوظة © 2026 | تطوير م/ ياسين علاء</div>", unsafe_allow_html=True)

# --- [ واجهة الشغل ] ---
else:
    st.markdown(f"<div style='text-align:left; color:#f39c12; font-weight:bold;'>المطور: م/ ياسين علاء</div>", unsafe_allow_html=True)
    col_h1, col_h2 = st.columns([8, 2])
    with col_h1: st.title("🛠️ لوحة تخصيم المشروع والجرد الدقيق")
    with col_h2: 
        if st.button("🚪 خروج"): 
            st.session_state.auth = False
            st.rerun()

    with st.expander("📝 إضافة وحدة جديدة (دقة متناهية)", expanded=True):
        c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1])
        u_name = c1.text_input("كود أو اسم الوحدة (يمنع التكرار)")
        u_type = c2.selectbox("نوع الوحدة", ["وحدة سفلية", "وحدة علوية", "دولاب خزين", "أخرى"])
        qty = c3.number_input("الكمية", min_value=1, value=1)
        W = c4.number_input("العرض (سم)", min_value=0.0)
        H = c5.number_input("الارتفاع (سم)", min_value=0.0)
        D = st.number_input("العمق (سم)", min_value=0.0)

        # منع التكرار
        existing_names = [u['name'] for u in st.session_state.db]
        
        st.markdown("---")
        # خانات إضافية للدقة
        col_ex1, col_ex2, col_ex3 = st.columns(3)
        sh_n = col_ex1.number_input("الأرفف (عدد)", 0)
        dv_n = col_ex2.number_input("الفواصل (عدد)", 0)
        dr_n = col_ex3.number_input("الأدراج (عدد)", 0)

        if st.button("💾 تثبيت الوحدة في الجرد", use_container_width=True):
            if not u_name:
                st.error("⚠️ يرجى إدخال اسم الوحدة")
            elif u_name in existing_names:
                st.error(f"⚠️ الاسم '{u_name}' موجود مسبقاً! يرجى استخدام اسم فريد لمنع تكرار الجرد.")
            elif W <= 0 or H <= 0:
                st.error("⚠️ يرجى التأكد من المقاسات")
            else:
                st.session_state.db.append({
                    'name': u_name, 'type': u_type, 'qty': qty, 'W': W, 'H': H, 'D': D,
                    'sh_n': sh_n, 'dv_n': dv_n, 'dr_n': dr_n
                })
                st.success(f"تمت إضافة {u_name} بنجاح")
                st.rerun()if st.session_state.db:
        st.divider()
        total_m, total_t, total_f = 0, 0, 0
        total_joints, total_handles, total_hinges = 0, 0, 0

        for u in st.session_state.db:
            # 1. معادلات التخصيم (المثبتة)
            h_ded = 13 if (u['type'] == "وحدة سفلية" or u['type'] == "دولاب خزين") else 5
            h_b, w_b, d_b = u['H'] - h_ded, u['W'] - 5, u['D'] - 5
            
            # 2. جرد الألومنيوم
            if u['type'] == "وحدة سفلية":
                u_m = (h_b*2 + w_b*3 + d_b*2); u_t = (h_b*2 + w_b*1 + d_b*2)
            else:
                u_m = (h_b*2 + w_b*2); u_t = (h_b*2 + w_b*2 + d_b*4)
            
            # إضافة الرفوف والفواصل (تخصيم الألومنيوم)
            u_m += (u['sh_n'] * 4 * (u['W']-5)) + (u['dv_n'] * 4 * (u['H']-h_ded))
            
            # 3. جرد الإكسسوارات (الدقة المطلوبة)
            total_joints += 8 * u['qty'] # زوايا تجميع الهيكل
            total_handles += (2 if u['dr_n'] == 0 else u['dr_n']) * u['qty'] # مقابض
            total_hinges += 4 * u['qty'] # مفصلات تقديرية

            total_m += u_m * u['qty']; total_t += u_t * u['qty']
            total_f += ((w_b*h_b) + (w_b*d_b) + (h_b*d_b*2)) * u['qty']

            # عرض الجداول
            st.markdown(f'<div class="unit-card"><h3>📦 الوحدة: {u["name"]} | المصمم: م/ ياسين علاء</h3>', unsafe_allow_html=True)
            c_a, c_b = st.columns(2)
            with c_a:
                st.table(pd.DataFrame({"الألومنيوم": ["ارتفاع", "عرض", "عمق"], "مفرد": [h_b, w_b, d_b], "متقارب": [h_b, w_b, d_b]}))
            with c_b:
                st.table(pd.DataFrame({"الفيبر": ["ضهرية", "أرضية", "أجناب"], "المقاس": [f"{w_b}×{h_b}", f"{w_b}×{d_b}", f"{h_b}×{d_b}"]}))
            st.markdown('</div>', unsafe_allow_html=True)

        # 4. الفاتورة النهائية الشاملة
        st.markdown(f'<div class="total-box"><h2>📊 التقرير النهائي للجرد - إعداد م/ ياسين علاء</h2>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        r1.metric("ألومنيوم مفرد (عود)", f"{total_m/600:.2f}")
        r2.metric("ألومنيوم متقارب (عود)", f"{total_t/600:.2f}")
        r3.metric("فيبر (لوح)", f"{total_f/36400:.2f}")
        
        st.write("---")
        st.write("**📦 جرد الإكسسوارات الدقيق:**")
        ix1, ix2, ix3 = st.columns(3)
        ix1.write(f"✅ عدد زوايا التجميع: {total_joints} قطعة")
        ix2.write(f"✅ عدد المقابض المطلوبة: {total_handles} قطعة")
        ix3.write(f"✅ عدد المفصلات (تقديري): {total_hinges} قطعة")
        
        if st.button("🗑️ مسح المشروع بالكامل"): st.session_state.db = []; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; margin-top:30px;'>تمت البرمجة بواسطة المهندس ياسين علاء © 2026</p>", unsafe_allow_html=True)# --- [ الجزء الثالث والأخير: تقارير الطباعة والتوقيع النهائي ] ---
# برمجة المهندس ياسين علاء

        # 5. قسم الطباعة والتصدير (Layout for Print)
        st.divider()
        st.subheader("🖨️ خيارات الطباعة والتصدير")
        
        col_print1, col_print2 = st.columns(2)
        
        with col_print1:
            if st.button("📄 تجهيز أمر الشغل للطباعة", use_container_width=True):
                st.toast("جاري تحضير الملف للطباعة...")
                # ملاحظة: في streamlit الطباعة تتم عبر Ctrl+P من المتصفح
                # هذا الزر يمكن برمجته لاحقاً لتصدير PDF احترافي
        
        with col_print2:
            # إضافة زر لتحميل البيانات كملف Excel للجرد المخزني
            if st.session_state.db:
                df_export = pd.DataFrame(st.session_state.db)
                csv = df_export.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 تحميل جدول المقاسات (Excel/CSV)",
                    data=csv,
                    file_name=f'Project_Yassin_Alaa_{datetime.now().strftime("%Y%m%d")}.csv',
                    mime='text/csv',
                    use_container_width=True
                )

        # 6. التوقيع النهائي الثابت (Footer)
        st.markdown(f"""
            <div style="
                margin-top: 100px;
                padding: 40px;
                background-color: #f8f9fa;
                border-radius: 20px;
                border: 2px dashed #2c3e50;
                text-align: center;
            ">
                <h2 style="color: #2c3e50; margin-bottom: 10px;">نظام Kitchen Pro ERP المعتمد</h2>
                <p style="font-size: 20px; color: #7f8c8d;">تمت مراجعة الحسابات وتدقيق التخصيم برمجياً</p>
                <div style="
                    font-size: 32px; 
                    font-weight: 900; 
                    color: #f39c12; 
                    margin-top: 15px;
                    border-top: 1px solid #ddd;
                    padding-top: 15px;
                ">
                    بواسطة م/ ياسين علاء
                </div>
                <p style="margin-top: 10px; font-weight: bold; color: #2c3e50;">إصدار 2026 | الدقة الفنية القصوى</p>
            </div>
        """, unsafe_allow_html=True)

    else:
        # رسالة تظهر في حالة فراغ المشروع (واجهة م/ ياسين علاء)
        st.markdown("""
            <div style="text-align: center; margin-top: 50px; padding: 50px; background: #fdfdfd; border-radius: 20px; border: 1px solid #eee;">
                <h3 style="color: #bdc3c7;">لا توجد وحدات في أمر التشغيل حالياً</h3>
                <p style="color: #bdc3c7;">يرجى استخدام نموذج الإدخال بالأعلى لإضافة المقاسات وبدء التخصيم</p>
                <div style="font-size: 50px; color: #eee; margin-top: 20px;">🏗️</div>
            </div>
        """, unsafe_allow_html=True)

# إضافة ذيل الصفحة الثابت لجميع الصفحات
st.markdown("""
    <style>
    .footer-fixed {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #2c3e50;
        text-align: center;
        padding: 5px;
        font-size: 12px;
        border-top: 1px solid #eee;
        z-index: 100;
    }
    </style>
    <div class="footer-fixed">
        نظام Kitchen Pro - تطوير وبرمجة م/ ياسين علاء © 2026
    </div>
""", unsafe_allow_html=True)
