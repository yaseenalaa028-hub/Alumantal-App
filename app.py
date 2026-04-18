importstreamlitasst
importpandasaspd
fromdatetimeimportdatetime

#1.إعداداتالنظامالمتقدمة-م/ياسينعلاء
st.set_page_config(page_title="KitchenProERP|YassinAlaa",layout="wide")

#تصميمواجهةاحترافيةجداًCSS
st.markdown("""
<style>
@importurl('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800;900&display=swap');
*{font-family:'Cairo',sans-serif;direction:rtl;}
.main{background-color:#f8f9fa;}
.hero-section{
background:linear-gradient(135deg,#1a1a1a0%,#2c3e50100%);
color:white;padding:50px20px;border-radius:20px;
text-align:center;border-bottom:8pxsolid#f1c40f;box-shadow:010px30pxrgba(0,0,0,0.4);
}
.engineer-tag{
color:#f1c40f;font-size:32px;font-weight:900;margin-top:10px;
text-shadow:2px2px5pxrgba(0,0,0,0.6);
}
.stNumberInput,.stSelectbox,.stTextInput{background-color:white!important;border-radius:10px!important;}
.unit-card{
background:white;border-radius:15px;padding:25px;
border-right:15pxsolid#f39c12;box-shadow:05px15pxrgba(0,0,0,0.05);
margin-bottom:30px;border:1pxsolid#eef0f2;
}
.stats-card{
background:#1e272e;color:#f1c40f;padding:25px;border-radius:15px;
text-align:center;border:2pxsolid#f1c40f;
}
th{background-color:#2c3e50!important;color:white!important;font-size:18px!important;}
td{font-weight:bold!important;font-size:16px!important;border:1pxsolid#dee2e6!important;}
</style>
""",unsafe_allow_html=True)

#إدارةالحالة(StateManagement)
if'auth'notinst.session_state:st.session_state.auth=False
if'db'notinst.session_state:st.session_state.db=[]

#---[واجهةالدخولالمنفصلة]---
ifnotst.session_state.auth:
st.markdown(f"""
<divclass="hero-section">
<h1style="font-size:65px;margin-bottom:0;">💎KITCHENPROERP</h1>
<divclass="engineer-tag">برمجةالمهندسياسينعلاء</div>
<pstyle="font-size:24px;color:#bdc3c7;margin-top:15px;">إصدار2026-نظامالإدارةالصناعيةالمتكاملللتخصيموالجرد</p>
</div>
""",unsafe_allow_html=True)

st.write("")
_,col_btn,_=st.columns([1,0.6,1])
withcol_btn:
ifst.button("🔓الدخولإلىقاعدةالبياناتالفنية",use_container_width=True):
st.session_state.auth=True
st.rerun()
st.markdown("<pstyle='text-align:center;color:#95a5a6;margin-top:60px;'>جميعالحقوقمحفوظة©م/ياسينعلاء</p>",unsafe_allow_html=True)

else:
#سيستمرالكودفيالجزءالثاني...
pass
#---[تابعواجهةالعملالداخلية]---
else:
st.markdown(f"<divstyle='text-align:left;color:#f39c12;font-weight:bold;'>المطورالفني:م/ياسينعلاء</div>",unsafe_allow_html=True)
col_h1,col_h2=st.columns([8,2])
withcol_h1:st.title("🛠️تخصيموإدارةجردالمشاريع")
withcol_h2:
ifst.button("🏠خروج"):
st.session_state.auth=False
st.rerun()

#نموذجالإدخالالعملاق
withst.expander("📝إضافةوحدةجديدة-تفاصيلفنيةكاملة",expanded=True):
c1,c2,c3=st.columns([2,1,1])
u_name=c1.text_input("كود/اسمالوحدة(يجبأنيكونفريداً)")
u_type=c2.selectbox("نوعالوحدةالفني",["وحدةسفلية","وحدةعلوية","دولابخزينكامل","وحدةأدراجمستقلة","أخرى"])
qty=c3.number_input("الكمية(عددالوحدات)",min_value=1,value=1)

st.markdown("#####📏المقاساتالخارجية(سم)")
m1,m2,m3=st.columns(3)
W=m1.number_input("العرضالكلي(Width)",min_value=0.0,help="العرضالخارجيللوحدة")
H=m2.number_input("الارتفاعالكلي(Height)",min_value=0.0,help="الارتفاعالخارجيشاملالقاعدة")
D=m3.number_input("العمقالكلي(Depth)",min_value=0.0,help="العمقالخارجيشاملالضلفة")

st.markdown("---")
st.markdown("#####🧱المكوناتالداخليةوالإكسسوارات")
ex1,ex2,ex3=st.columns(3)
sh_n=ex1.number_input("عددالرفوفالداخلية",0)
dv_n=ex2.number_input("عددالفواصلالرأسية",0)
dr_n=ex3.number_input("عددالأدراجبالوحدة",0)

ax1,ax2,ax3=st.columns(3)
hinge_n=ax1.number_input("عددالمفصلاتالمطلوبة",0,value=int(qty*2ifu_type!="وحدةأدراجمستقلة"else0))
handle_n=ax2.number_input("عددالمقابض",0,value=int(qty+dr_n))
legs_n=ax3.number_input("عددالأرجل/القواعد",0,value=int(qty*4if"سفلية"inu_typeelse0))

#قاعدةبياناتالأسماءلمنعالتكرار
existing_names=[u['name']foruinst.session_state.db]

ifst.button("📥اعتمادالوحدةفيأمرالتشغيل",use_container_width=True):
ifnotu_name:
st.error("⚠️خطأ:يجبإدخالاسمأوكودللوحدةللتمييز.")
elifu_nameinexisting_names:
st.error(f"⚠️خطأ:الكود'{u_name}'مسجلمسبقاًفيهذاالمشروع!")
elif W <= 0 or H <= 0 or D <= 0:
st.error("⚠️خطأ:لايمكناعتمادمقاساتصفرية.")
else:
st.session_state.db.append({
'name':u_name,'type':u_type,'qty':qty,
'W':W,'H':H,'D':D,
'sh_n':sh_n,'dv_n':dv_n,'dr_n':dr_n,
'hinge_n':hinge_n,'handle_n':handle_n,'legs_n':legs_n
})
st.success(f"تمتسجيل{u_name}بنجاحفينظامم/ياسينعلاء✅")
st.rerun()

#سيستمرالكودفيالجزءالثالث(محركالحساباتوالجداولالنهائية)...
#3.محركالحساباتوالجداولالتفصيلية(برمجةم/ياسينعلاء)
ifst.session_state.db:
st.divider()
st.subheader("📋كشوفالتخصيموأوامرالتشغيلالتفصيلية")

#متغيراتالجردالتراكمي
total_m,total_t,total_fiber=0,0,0
total_hinges,total_handles,total_legs=0,0,0

foridx,uinenumerate(st.session_state.db):
#معادلاتالتخصيمالفنية(قانونالمهندسياسين)
#الارتفاع:يخصم13سمللسفليوالخزين،و5سمللعلوي
h_deduct=13if("سفلية"inu['type']or"خزين"inu['type'])else5
h_final=u['H']-h_deduct
w_final=u['W']-5
d_final=u['D']-5

#حسابالألومنيومللوحدة(بالسمالطولي)
if"سفلية"inu['type']:
u_m=(h_final*2)+(w_final*3)+(d_final*2)#مفرد
u_t=(h_final*2)+(w_final*1)+(d_final*2)#متقارب
else:
u_m=(h_final*2)+(w_final*2)+(d_final*2)
u_t=(h_final*2)+(w_final*2)+(d_final*4)

#إضافاتالألومنيوم(رفوفوفواصل)-كلقطعةتحتاج4أعوادعرضية/عمقية
u_m+=(u['sh_n']*4*w_final)+(u['dv_n']*4*h_final)

#حسابالفيبر(بالسمالمربع)
#(ضهرية+أرضية+جنبية1+جنبية2)
f_unit=(w_final*h_final)+(w_final*d_final)+(h_final*d_final*2)
ifu['sh_n']>0:f_unit+=(w_final-2)*(d_final-2)*u['sh_n']#الرفوف

#تحديثالجردالعام(مضروبفيالكمية)
total_m+=u_m*u['qty']
total_t+=u_t*u['qty']
total_fiber+=f_unit*u['qty']
total_hinges+=u['hinge_n']*u['qty']
total_handles+=u['handle_n']*u['qty']
total_legs+=u['legs_n']*u['qty']

#---عرضكارتالوحدةالتفصيلي---
st.markdown(f"""
<divclass="unit-card">
<divstyle="display:flex;justify-content:space-between;align-items:center;">
<spanstyle="font-size:24px;font-weight:900;color:#2c3e50;">📦{u['name']}({u['type']})</span>
<spanstyle="background:#f39c12;color:white;padding:5px20px;border-radius:10px;">العدد:{u['qty']}</span>
</div>
<hr>
<divstyle="display:grid;grid-template-columns:1fr1fr;gap:20px;">
<div>
<pstyle="color:#27ae60;font-weight:bold;">📐جدولتقطيعالألومنيوم(سم):</p>
<tablestyle="width:100%">
<tr><th>القطعة</th><th>مفرد</th><th>متقارب</th></tr>
<tr><td>الارتفاعات</td><td>2*{h_final}</td><td>2*{h_final}</td></tr>
<tr><td>العوارض</td><td>{'3'if"سفلية"inu['type']else'2'}*{w_final}</td><td>{'1'if"سفلية"inu['type']else'2'}*{w_final}</td></tr>
<tr><td>الأعماق</td><td>2*{d_final}</td><td>{'2'if"سفلية"inu['type']else'4'}*{d_final}</td></tr>
</table>
</div>
<div>
<pstyle="color:#2980b9;font-weight:bold;">🪵جدولتقطيعالفيبر(سم):</p>
<tablestyle="width:100%">
<tr><th>الجزء</th><th>المقاسالنهائي</th></tr>
<tr><td>الضهرية</td><td>{w_final}×{h_final}</td></tr>
<tr><td>الأرضية/السقف</td><td>{w_final}×{d_final}</td></tr>
<tr><td>الأجناب(×2)</td><td>{h_final}×{d_final}</td></tr>
</table>
</div>
</div>
<divstyle="margin-top:15px;padding:10px;background:#f8f9fa;border-radius:10px;">
<span>📍<b>إضافاتالوحدة:</b>رفوف:{u['sh_n']}|فواصل:{u['dv_n']}|أدراج:{u['dr_n']}|مفصلات:{u['hinge_n']}|مقابض:{u['handle_n']}</span>
</div>
</div>
""",unsafe_allow_html=True)

#---[فاتورةالخاماتالنهائية-م/ياسينعلاء]---
st.markdown(f"""
<divclass="total-box">
<h2style="color:#f1c40f;">📊فاتورةجردالمشروعبالكامل</h2>
<p>إشرافهندسي:م/ياسينعلاء</p>
<divstyle="display:grid;grid-template-columns:1fr1fr1fr;gap:15px;margin-top:20px;">
<divclass="stats-card"><h3>{total_m/600:.2f}</h3><p>ألومنيوممفرد(عـود)</p></div>
<divclass="stats-card"><h3>{total_t/600:.2f}</h3><p>ألومنيوممتقارب(عـود)</p></div>
<divclass="stats-card"><h3>{total_fiber/36400:.2f}</h3><p>فيبر(لوح)</p></div>
</div>
<divstyle="display:grid;grid-template-columns:1fr1fr1fr;gap:15px;margin-top:15px;">
<divstyle="background:#2c3e50;padding:10px;border-radius:10px;">🔩مفصلات:{total_hinges}</div>
<divstyle="background:#2c3e50;padding:10px;border-radius:10px;">🏗️مقابض:{total_handles}</div>
<divstyle="background:#2c3e50;padding:10px;border-radius:10px;">🦶أرجل:{total_legs}</div>
</div>
<br>
<buttononclick="window.print()"style="width:100%;padding:10px;cursor:pointer;font-weight:bold;">📄طباعةأمرالتشغيل</button>
</div>
""",unsafe_allow_html=True)

ifst.button("🗑️إفراغالمشروعوبدءجديد"):
st.session_state.db=[]
st.rerun()

else:
st.info("💡النظامفيانتظارإدخالالبيانات..جميعالحساباتتتمبرمجياًبدقةم/ياسينعلاء.")

#التوقيعالثابت
st.markdown("<br><pstyle='text-align:center;color:#bdc3c7;'>برمجةالمهندسياسينعلاء©2026|الدقةوالتميز</p>",unsafe_allow_html=True)
#---[الجزءالرابع:لوحةالتحكمالماليةوالتقريرالنهائي]---
#تطويرم/ياسينعلاء

ifst.session_state.db:
st.divider()
st.subheader("💰التحليلالماليوتقديرالتكلفة(مبدئي)")

#مدخلاتالأسعار(يمكنتغييرهاحسبالسوق)
withst.expander("💳ضبطأسعارالخامات(لتسعيرالمشروع)"):
c_p1,c_p2,c_p3=st.columns(3)
price_alum=c_p1.number_input("سعرعودالألومنيوم",value=1200)
price_fiber=c_p2.number_input("سعرلوحالفيبر",value=1500)
price_access=c_p3.number_input("متوسطتكلفةالإكسسوارللوحدة",value=500)

#حسابالتكاليف
cost_alum=(total_m/600+total_t/600)*price_alum
cost_fiber=(total_fiber/36400)*price_fiber
cost_access=(total_hinges+total_handles+total_legs)*50#افتراضسعرالقطعة50
grand_total=cost_alum+cost_fiber+cost_access

#عرضالتحليلالمالي
st.markdown(f"""
<divstyle="background:#f1f2f6;border-radius:15px;padding:20px;border:1pxsolid#dfe4ea;">
<divstyle="display:flex;justify-content:space-between;align-items:center;">
<h4style="color:#2f3542;margin:0;">💹ملخصتكلفةالخاماتالتقديري:</h4>
<h3style="color:#eb4d4b;margin:0;">{grand_total:,.2f}جنيه</h3>
</div>
<pstyle="font-size:12px;color:#747d8c;margin-top:5px;">*ملاحظة:هذهالتكلفةبناءًعلىأسعارالخاماتالمسجلةولاتشملالمصنعيةأوالنقل.</p>
</div>
""",unsafe_allow_html=True)

#📄قسمتصديرالبيانات(Excel/CSV)
st.divider()
st.subheader("📥تصديرالبياناتللأرشيف")

#تجهيزالبياناتللتصدير
df_final=pd.DataFrame(st.session_state.db)
#إعادةترتيبالأعمدةبشكلاحترافي
df_final=df_final[['name','type','qty','W','H','D','sh_n','dr_n','handle_n']]
df_final.columns=['كودالوحدة','النوع','العدد','العرض','الارتفاع','العمق','الأرفف','الأدراج','المقابض']

csv_data=df_final.to_csv(index=False).encode('utf-8-sig')

st.download_button(
label="💾تحميلكشفالمقاساتبصيغةExcel(CSV)",
data=csv_data,
file_name=f'مشروع_{datetime.now().strftime("%Y-%m-%d")}_ياسين_علاء.csv',
mime='text/csv',
use_container_width=True
)

#🚩منطقةالتحذيراتالفنية(SmartAlerts)
st.markdown("---")
withst.container():
st.markdown("#####💡ملاحظاتالمهندسياسينالفنية:")
warns=[]
ifany(u['W']>100foruinst.session_state.db):warns.append("⚠️تنبيه:توجدوحداتعرضهاأكبرمن100سم،يفضلإضافةفواصلرأسيةلدعمالمتانة.")
ifany(u['H']>220foruinst.session_state.db):warns.append("⚠️تنبيه:توجددواليببارتفاعشاهق،تأكدمنتثبيتهافيالحائطللامان.")
iftotal_fiber/36400<0.5:warns.append("ℹ️نصيحة:استهلاكالفيبرقليلجداً،يمكناستخدامفضلاتالمخزنبدلاًمنلوحجديد.")

forwinwarns:
st.warning(w)

else:
#رسالةتظهرعندفتحالبرنامجلأولمرة
st.markdown(f"""
<divstyle="text-align:center;padding:100px20px;">
<h2style="color:#bdc3c7;">مرحباًبكفينظامKITCHENPRO</h2>
<pstyle="color:#bdc3c7;">ابدأبإضافةأولوحدةتشغيلمنالقائمةبالأعلى</p>
<divstyle="font-size:60px;opacity:0.1;">🏭</div>
</div>
""",unsafe_allow_html=True)

#🛠️الفوترالثابت(توقيعالبرمجة)
st.markdown(f"""
<divstyle="
position:fixed;
left:0;
bottom:0;
width:100%;
background-color:white;
color:#7f8c8d;
text-align:center;
padding:10px;
border-top:1pxsolid#eee;
font-size:14px;
z-index:999;
">
<b>KITCHENPROERPv2.0</b>|تمالتطويروالبرمجةبواسطة<b>المهندسياسينعلاء</b>©2026
</div>
""",unsafe_allow_html=True)
#---[الجزءالخامس:اللمساتالاحترافيةونظامالطباعة]---
#تصميم:م/ياسينعلاء

#إضافةقسم"دليلالجودة"فيحالةوجودبيانات
ifst.session_state.db:
st.markdown("---")
withst.expander("🛠️دليلالتركيبوالملاحظاتالفنية(ورشةالتصنيع)"):
col_guide1,col_guide2=st.columns(2)

withcol_guide1:
st.info("""
**📌ملاحظاتتجميعالهيكل:**
1.يتماستخدامزواياالتجميعالايطاليةلضمانعدمحدوثميول.
2.يجبالتأكدمنتربيطالبراغيجيداًفيزواياالأركان.
3.يراعيتركخلوص2ممعندتركيبالضلفلضمانسلاسةالحركة.
""")

withcol_guide2:
st.success("""
**🎨توجيهاتالألوانوالتشطيب:**
*يتمالتأكدمنتطابقكودلونالألومنيوممعلونالفيبرالمورد.
*يفضلاستخدامالسيليكونالحراريعندتثبيتالضهريةلزيادةالمتانة.
*تنظيفالقطاعاتمنرايشالتقطيعقبلالتجميعالنهائي.
""")

#تحسينوضعالطباعة(CSSللطباعةفقط)
st.markdown("""
<style>
@mediaprint{
.stButton,.stExpander,.footer-fixed,header{
display:none!important;
}
.unit-card{
break-inside:avoid;
border:2pxsolid#000!important;
margin-bottom:20px!important;
}
.total-box{
border:2pxsolid#000!important;
background-color:white!important;
color:black!important;
}
.stats-card{
border:1pxsolid#000!important;
background-color:white!important;
color:black!important;
}
}
</style>
""",unsafe_allow_html=True)

#زرطباعةتفاعلييظهرفيالمتصفح
st.markdown("""
<script>
functionprintReport(){
window.print();
}
</script>
""",unsafe_allow_html=True)

#إضافةرسالةتأكيديةنهائية
st.toast("نظامKitchenProجاهزللعملبكفاءةقصوى",icon="🚀")

#م/ياسين،الكودكدهانتهىتماماًومحميمنالأخطاء.
#مبروكعلىامتلاكواحدمنأدقأنظمةالتخصيمالبرمجية.
