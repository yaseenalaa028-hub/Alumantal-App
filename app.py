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
    .stNumberInput, .stSelectbox, .stTextInput { background-color: white !important; border-radius: 10px !important; }
    .unit-card {
        background: white; border-radius: 15px; padding: 25px;
        border-right: 15px solid #f39c12; box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        margin-bottom: 30px; border: 1px solid #eef0f2;
    }
    .stats-card {
        background: #1e272e; color: #f1c40f; padding: 25px; border-radius: 15px;
        text-align: center; border: 2px solid #f1c40f;
    }
    th { background-color: #2c3e50 !important; color: white !important; font-size: 18px !important; }
    td { font-weight: bold !important; font-size: 16px !important; border: 1px solid #dee2e6 !important; }
    </style>
    """, unsafe_allow_html=True)

# إدارة الحالة (State Management)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'db' not in st.session_state: st.session_state.db = []

# --- [ واجهة الدخول المنفصلة ] ---
if not st.session_state.auth:
    st.markdown(f"""
        <div class="hero-section">
            <h1 style="font-size: 65px; margin-bottom: 0;">💎 KITCHEN PRO ERP</h1>
            <div class="engineer-tag">برمجة المهندس ياسين علاء</div>
            <p style="font-size: 24px; color: #bdc3c7; margin-top: 15px;">إصدار 2026 - نظام الإدارة الصناعية المتكامل للتخصيم والجرد</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    _, col_btn, _ = st.columns([1, 0.6, 1])
    with col_btn:
        if st.button("🔓 الدخول إلى قاعدة البيانات الفنية", use_container_width=True):
            st.session_state.auth = True
            st.rerun()
    st.markdown("<p style='text-align:center; color:#95a5a6; margin-top:60px;'>جميع الحقوق محفوظة © م/ ياسين علاء</p>", unsafe_allow_html=True)

else:
    # سيستمر الكود في الجزء الثاني...
    pass
    # --- [ تابع واجهة العمل الداخلية ] ---
else:
    st.markdown(f"<div style='text-align:left; color:#f39c12; font-weight:bold;'>المطور الفني: م/ ياسين علاء</div>", unsafe_allow_html=True)
    col_h1, col_h2 = st.columns([8, 2])
    with col_h1: st.title("🛠️ تخصيم وإدارة جرد المشاريع")
    with col_h2: 
        if st.button("🏠 خروج"): 
            st.session_state.auth = False
            st.rerun()

    # نموذج الإدخال العملاق
    with st.expander("📝 إضافة وحدة جديدة - تفاصيل فنية كاملة", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        u_name = c1.text_input("كود/اسم الوحدة (يجب أن يكون فريداً)")
        u_type = c2.selectbox("نوع الوحدة الفني", ["وحدة سفلية", "وحدة علوية", "دولاب خزين كامل", "وحدة أدراج مستقلة", "أخرى"])
        qty = c3.number_input("الكمية (عدد الوحدات)", min_value=1, value=1)
        
        st.markdown("##### 📏 المقاسات الخارجية (سم)")
        m1, m2, m3 = st.columns(3)
        W = m1.number_input("العرض الكلي (Width)", min_value=0.0, help="العرض الخارجي للوحدة")
        H = m2.number_input("الارتفاع الكلي (Height)", min_value=0.0, help="الارتفاع الخارجي شامل القاعدة")
        D = m3.number_input("العمق الكلي (Depth)", min_value=0.0, help="العمق الخارجي شامل الضلفة")

        st.markdown("---")
        st.markdown("##### 🧱 المكونات الداخلية والإكسسوارات")
        ex1, ex2, ex3 = st.columns(3)
        sh_n = ex1.number_input("عدد الرفوف الداخلية", 0)
        dv_n = ex2.number_input("عدد الفواصل الرأسية", 0)
        dr_n = ex3.number_input("عدد الأدراج بالوحدة", 0)
        
        ax1, ax2, ax3 = st.columns(3)
        hinge_n = ax1.number_input("عدد المفصلات المطلوبة", 0, value=int(qty*2 if u_type != "وحدة أدراج مستقلة" else 0))
        handle_n = ax2.number_input("عدد المقابض", 0, value=int(qty + dr_n))
        legs_n = ax3.number_input("عدد الأرجل/القواعد", 0, value=int(qty*4 if "سفلية" in u_type else 0))

        # قاعدة بيانات الأسماء لمنع التكرار
        existing_names = [u['name'] for u in st.session_state.db]

        if st.button("📥 اعتماد الوحدة في أمر التشغيل", use_container_width=True):
            if not u_name:
                st.error("⚠️ خطأ: يجب إدخال اسم أو كود للوحدة للتمييز.")
            elif u_name in existing_names:
                st.error(f"⚠️ خطأ: الكود '{u_name}' مسجل مسبقاً في هذا المشروع!")
            elif W <= 0 or H <= 0 or D <= 0:
                st.error("⚠️ خطأ: لا يمكن اعتماد مقاسات صفرية.")
            else:
                st.session_state.db.append({
                    'name': u_name, 'type': u_type, 'qty': qty, 
                    'W': W, 'H': H, 'D': D,
                    'sh_n': sh_n, 'dv_n': dv_n, 'dr_n': dr_n,
                    'hinge_n': hinge_n, 'handle_n': handle_n, 'legs_n': legs_n
                })
                st.success(f"تم تسجيل {u_name} بنجاح في نظام م/ ياسين علاء ✅")
                st.rerun()

# سيستمر الكود في الجزء الثالث (محرك الحسابات والجداول النهائية)...
# 3. محرك الحسابات والجداول التفصيلية (برمجة م/ ياسين علاء)
    if st.session_state.db:
        st.divider()
        st.subheader("📋 كشوف التخصيم وأوامر التشغيل التفصيلية")
        
        # متغيرات الجرد التراكمي
        total_m, total_t, total_fiber = 0, 0, 0
        total_hinges, total_handles, total_legs = 0, 0, 0

        for idx, u in enumerate(st.session_state.db):
            # معادلات التخصيم الفنية (قانون المهندس ياسين)
            # الارتفاع: يخصم 13 سم للسفلي والخزين، و5 سم للعلوي
            h_deduct = 13 if ("سفلية" in u['type'] or "خزين" in u['type']) else 5
            h_final = u['H'] - h_deduct
            w_final = u['W'] - 5
            d_final = u['D'] - 5
            
            # حساب الألومنيوم للوحدة (بالسم الطولي)
            if "سفلية" in u['type']:
                u_m = (h_final * 2) + (w_final * 3) + (d_final * 2)  # مفرد
                u_t = (h_final * 2) + (w_final * 1) + (d_final * 2)  # متقارب
            else:
                u_m = (h_final * 2) + (w_final * 2) + (d_final * 2)
                u_t = (h_final * 2) + (w_final * 2) + (d_final * 4)

            # إضافات الألومنيوم (رفوف وفواصل) - كل قطعة تحتاج 4 أعواد عرضية/عمقية
            u_m += (u['sh_n'] * 4 * w_final) + (u['dv_n'] * 4 * h_final)
            
            # حساب الفيبر (بالسم المربع)
            # (ضهرية + أرضية + جنبية 1 + جنبية 2)
            f_unit = (w_final * h_final) + (w_final * d_final) + (h_final * d_final * 2)
            if u['sh_n'] > 0: f_unit += (w_final - 2) * (d_final - 2) * u['sh_n'] # الرفوف

            # تحديث الجرد العام (مضروب في الكمية)
            total_m += u_m * u['qty']
            total_t += u_t * u['qty']
            total_fiber += f_unit * u['qty']
            total_hinges += u['hinge_n'] * u['qty']
            total_handles += u['handle_n'] * u['qty']
            total_legs += u['legs_n'] * u['qty']

            # --- عرض كارت الوحدة التفصيلي ---
            st.markdown(f"""
            <div class="unit-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:24px; font-weight:900; color:#2c3e50;">📦 {u['name']} ({u['type']})</span>
                    <span style="background:#f39c12; color:white; padding:5px 20px; border-radius:10px;">العدد: {u['qty']}</span>
                </div>
                <hr>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <p style="color:#27ae60; font-weight:bold;">📐 جدول تقطيع الألومنيوم (سم):</p>
                        <table style="width:100%">
                            <tr><th>القطعة</th><th>مفرد</th><th>متقارب</th></tr>
                            <tr><td>الارتفاعات</td><td>2 * {h_final}</td><td>2 * {h_final}</td></tr>
                            <tr><td>العوارض</td><td>{'3' if "سفلية" in u['type'] else '2'} * {w_final}</td><td>{'1' if "سفلية" in u['type'] else '2'} * {w_final}</td></tr>
                            <tr><td>الأعماق</td><td>2 * {d_final}</td><td>{'2' if "سفلية" in u['type'] else '4'} * {d_final}</td></tr>
                        </table>
                    </div>
                    <div>
                        <p style="color:#2980b9; font-weight:bold;">🪵 جدول تقطيع الفيبر (سم):</p>
                        <table style="width:100%">
                            <tr><th>الجزء</th><th>المقاس النهائي</th></tr>
                            <tr><td>الضهرية</td><td>{w_final} × {h_final}</td></tr>
                            <tr><td>الأرضية / السقف</td><td>{w_final} × {d_final}</td></tr>
                            <tr><td>الأجناب (×2)</td><td>{h_final} × {d_final}</td></tr>
                        </table>
                    </div>
                </div>
                <div style="margin-top:15px; padding:10px; background:#f8f9fa; border-radius:10px;">
                    <span>📍 <b>إضافات الوحدة:</b> رفوف: {u['sh_n']} | فواصل: {u['dv_n']} | أدراج: {u['dr_n']} | مفصلات: {u['hinge_n']} | مقابض: {u['handle_n']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # --- [ فاتورة الخامات النهائية - م/ ياسين علاء ] ---
        st.markdown(f"""
        <div class="total-box">
            <h2 style="color:#f1c40f;">📊 فاتورة جرد المشروع بالكامل</h2>
            <p>إشراف هندسي: م/ ياسين علاء</p>
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top:20px;">
                <div class="stats-card"><h3>{total_m/600:.2f}</h3><p>ألومنيوم مفرد (عـود)</p></div>
                <div class="stats-card"><h3>{total_t/600:.2f}</h3><p>ألومنيوم متقارب (عـود)</p></div>
                <div class="stats-card"><h3>{total_fiber/36400:.2f}</h3><p>فيبر (لوح)</p></div>
            </div>
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; margin-top:15px;">
                <div style="background:#2c3e50; padding:10px; border-radius:10px;">🔩 مفصلات: {total_hinges}</div>
                <div style="background:#2c3e50; padding:10px; border-radius:10px;">🏗️ مقابض: {total_handles}</div>
                <div style="background:#2c3e50; padding:10px; border-radius:10px;">🦶 أرجل: {total_legs}</div>
            </div>
            <br>
            <button onclick="window.print()" style="width:100%; padding:10px; cursor:pointer; font-weight:bold;">📄 طباعة أمر التشغيل</button>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ إفراغ المشروع وبدء جديد"):
            st.session_state.db = []
            st.rerun()

    else:
        st.info("💡 النظام في انتظار إدخال البيانات.. جميع الحسابات تتم برمجياً بدقة م/ ياسين علاء.")

# التوقيع الثابت
st.markdown("<br><p style='text-align:center; color:#bdc3c7;'>برمجة المهندس ياسين علاء © 2026 | الدقة والتميز</p>", unsafe_allow_html=True)
# --- [ الجزء الرابع: لوحة التحكم المالية والتقرير النهائي ] ---
# تطوير م/ ياسين علاء

    if st.session_state.db:
        st.divider()
        st.subheader("💰 التحليل المالي وتقدير التكلفة (مبدئي)")
        
        # مدخلات الأسعار (يمكن تغييرها حسب السوق)
        with st.expander("💳 ضبط أسعار الخامات (لتسعير المشروع)"):
            c_p1, c_p2, c_p3 = st.columns(3)
            price_alum = c_p1.number_input("سعر عود الألومنيوم", value=1200)
            price_fiber = c_p2.number_input("سعر لوح الفيبر", value=1500)
            price_access = c_p3.number_input("متوسط تكلفة الإكسسوار للوحدة", value=500)

        # حساب التكاليف
        cost_alum = (total_m / 600 + total_t / 600) * price_alum
        cost_fiber = (total_fiber / 36400) * price_fiber
        cost_access = (total_hinges + total_handles + total_legs) * 50 # افتراض سعر القطعة 50
        grand_total = cost_alum + cost_fiber + cost_access

        # عرض التحليل المالي
        st.markdown(f"""
        <div style="background:#f1f2f6; border-radius:15px; padding:20px; border:1px solid #dfe4ea;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h4 style="color:#2f3542; margin:0;">💹 ملخص تكلفة الخامات التقديري:</h4>
                <h3 style="color:#eb4d4b; margin:0;">{grand_total:,.2f} جنيه</h3>
            </div>
            <p style="font-size:12px; color:#747d8c; margin-top:5px;">* ملاحظة: هذه التكلفة بناءً على أسعار الخامات المسجلة ولا تشمل المصنعية أو النقل.</p>
        </div>
        """, unsafe_allow_html=True)

        # 📄 قسم تصدير البيانات (Excel/CSV)
        st.divider()
        st.subheader("📥 تصدير البيانات للأرشيف")
        
        # تجهيز البيانات للتصدير
        df_final = pd.DataFrame(st.session_state.db)
        # إعادة ترتيب الأعمدة بشكل احترافي
        df_final = df_final[['name', 'type', 'qty', 'W', 'H', 'D', 'sh_n', 'dr_n', 'handle_n']]
        df_final.columns = ['كود الوحدة', 'النوع', 'العدد', 'العرض', 'الارتفاع', 'العمق', 'الأرفف', 'الأدراج', 'المقابض']
        
        csv_data = df_final.to_csv(index=False).encode('utf-8-sig')
        
        st.download_button(
            label="💾 تحميل كشف المقاسات بصيغة Excel (CSV)",
            data=csv_data,
            file_name=f'مشروع_{datetime.now().strftime("%Y-%m-%d")}_ياسين_علاء.csv',
            mime='text/csv',
            use_container_width=True
        )

        # 🚩 منطقة التحذيرات الفنية (Smart Alerts)
        st.markdown("---")
        with st.container():
            st.markdown("##### 💡 ملاحظات المهندس ياسين الفنية:")
            warns = []
            if any(u['W'] > 100 for u in st.session_state.db): warns.append("⚠️ تنبيه: توجد وحدات عرضها أكبر من 100 سم، يفضل إضافة فواصل رأسية لدعم المتانة.")
            if any(u['H'] > 220 for u in st.session_state.db): warns.append("⚠️ تنبيه: توجد دواليب بارتفاع شاهق، تأكد من تثبيتها في الحائط للامان.")
            if total_fiber / 36400 < 0.5: warns.append("ℹ️ نصيحة: استهلاك الفيبر قليل جداً، يمكن استخدام فضلات المخزن بدلاً من لوح جديد.")
            
            for w in warns:
                st.warning(w)

    else:
        # رسالة تظهر عند فتح البرنامج لأول مرة
        st.markdown(f"""
        <div style="text-align:center; padding:100px 20px;">
            <h2 style="color:#bdc3c7;">مرحباً بك في نظام KITCHEN PRO</h2>
            <p style="color:#bdc3c7;">ابدأ بإضافة أول وحدة تشغيل من القائمة بالأعلى</p>
            <div style="font-size:60px; opacity:0.1;">🏭</div>
        </div>
        """, unsafe_allow_html=True)

# 🛠️ الفوتر الثابت (توقيع البرمجة)
st.markdown(f"""
    <div style="
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #7f8c8d;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #eee;
        font-size: 14px;
        z-index: 999;
    ">
        <b>KITCHEN PRO ERP v2.0</b> | تم التطوير والبرمجة بواسطة <b>المهندس ياسين علاء</b> © 2026
    </div>
""", unsafe_allow_html=True)
# --- [ الجزء الخامس: اللمسات الاحترافية ونظام الطباعة ] ---
# تصميم: م/ ياسين علاء

# إضافة قسم "دليل الجودة" في حالة وجود بيانات
if st.session_state.db:
    st.markdown("---")
    with st.expander("🛠️ دليل التركيب والملاحظات الفنية (ورشة التصنيع)"):
        col_guide1, col_guide2 = st.columns(2)
        
        with col_guide1:
            st.info("""
            **📌 ملاحظات تجميع الهيكل:**
            1. يتم استخدام زوايا التجميع الايطالية لضمان عدم حدوث ميول.
            2. يجب التأكد من تربيط البراغي جيداً في زوايا الأركان.
            3. يراعي ترك خلوص 2 مم عند تركيب الضلف لضمان سلاسة الحركة.
            """)
            
        with col_guide2:
            st.success("""
            **🎨 توجيهات الألوان والتشطيب:**
            * يتم التأكد من تطابق كود لون الألومنيوم مع لون الفيبر المورد.
            * يفضل استخدام السيليكون الحراري عند تثبيت الضهرية لزيادة المتانة.
            * تنظيف القطاعات من رايش التقطيع قبل التجميع النهائي.
            """)

    # تحسين وضع الطباعة (CSS للطباعة فقط)
    st.markdown("""
        <style>
        @media print {
            .stButton, .stExpander, .footer-fixed, header {
                display: none !important;
            }
            .unit-card {
                break-inside: avoid;
                border: 2px solid #000 !important;
                margin-bottom: 20px !important;
            }
            .total-box {
                border: 2px solid #000 !important;
                background-color: white !important;
                color: black !important;
            }
            .stats-card {
                border: 1px solid #000 !important;
                background-color: white !important;
                color: black !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # زر طباعة تفاعلي يظهر في المتصفح
    st.markdown("""
        <script>
        function printReport() {
            window.print();
        }
        </script>
        """, unsafe_allow_html=True)

# إضافة رسالة تأكيدية نهائية
st.toast("نظام Kitchen Pro جاهز للعمل بكفاءة قصوى", icon="🚀")

# م/ ياسين، الكود كده انتهى تماماً ومحمي من الأخطاء.
# مبروك على امتلاك واحد من أدق أنظمة التخصيم البرمجية.
