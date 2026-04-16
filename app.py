<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نظام الورشة المعتمد v4.0</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
    <style>
        body { background-color: #f8f9fa; font-family: 'Segoe UI', sans-serif; padding: 20px; }
        .card { border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border: none; }
        .header-section { background: #2c3e50; color: white; border-radius: 15px 15px 0 0; padding: 20px; }
        .btn-calc { background: #27ae60; color: white; font-weight: bold; padding: 12px; border-radius: 8px; border: none; width: 100%; }
        .btn-calc:hover { background: #219150; }
        .res-box { display: none; margin-top: 20px; }
        .table-al { border-top: 4px solid #27ae60; }
        .table-fb { border-top: 4px solid #e67e22; }
        .badge-qty { background: #34495e; color: white; padding: 5px 12px; border-radius: 4px; }
    </style>
</head>
<body>

<div class="container">
    <div class="card">
        <div class="header-section text-center">
            <h3>🏗️ حاسبة الورشة (المهندس ياسين)</h3>
            <p class="mb-0 text-info">تحديث: فصل الفيبر + حساب الفواصل + الرفوف × 4</p>
        </div>
        <div class="card-body p-4">
            <div class="row g-3">
                <div class="col-md-3">
                    <label class="form-label">العرض الكلي</label>
                    <input type="number" id="w" class="form-control" value="100">
                </div>
                <div class="col-md-3">
                    <label class="form-label">الارتفاع الكلي</label>
                    <input type="number" id="h" class="form-control" value="90">
                </div>
                <div class="col-md-3">
                    <label class="form-label">العمق الكلي</label>
                    <input type="number" id="d" class="form-control" value="50">
                </div>
                <div class="col-md-3">
                    <label class="form-label">النوع</label>
                    <select id="u_type" class="form-select">
                        <option value="13">سفلية (تخصيم 13)</option>
                        <option value="5">علوية (تخصيم 5)</option>
                    </select>
                </div>
                <hr>
                <div class="col-md-4">
                    <label class="form-label text-primary fw-bold">عرض الرف</label>
                    <input type="number" id="sw" class="form-control" value="0">
                </div>
                <div class="col-md-4">
                    <label class="form-label text-primary fw-bold">عمق الرف</label>
                    <input type="number" id="sd" class="form-control" value="0">
                </div>
                <div class="col-md-4">
                    <label class="form-label text-primary fw-bold">عدد الرفوف</label>
                    <input type="number" id="sn" class="form-control" value="0">
                </div>
                <div class="col-12 text-center">
                    <button onclick="calculate()" class="btn-calc mt-3">🚀 استخراج التقارير الآن</button>
                </div>
            </div>
        </div>
    </div>

    <div id="resultArea" class="res-box">
        <div class="row g-4">
            <div class="col-md-6">
                <div class="card h-100 p-3">
                    <h5 class="text-success mb-3 fw-bold">📏 قائمة تقطيع الألمنيوم</h5>
                    <table class="table table-bordered text-center table-al">
                        <thead class="table-light">
                            <tr><th>البند</th><th>المقاس</th><th>العدد</th></tr>
                        </thead>
                        <tbody id="al_body"></tbody>
                    </table>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card h-100 p-3">
                    <h5 class="text-warning mb-3 fw-bold">🔲 قائمة تقطيع الفيبر</h5>
                    <table class="table table-bordered text-center table-fb">
                        <thead class="table-light">
                            <tr><th>البند</th><th>المقاس</th><th>العدد</th></tr>
                        </thead>
                        <tbody id="fb_body"></tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function calculate() {
    // جلب القيم
    const w = parseFloat(document.getElementById('w').value);
    const h = parseFloat(document.getElementById('h').value);
    const d = parseFloat(document.getElementById('d').value);
    const tax = parseFloat(document.getElementById('u_type').value);
    const sn = parseInt(document.getElementById('sn').value) || 0;
    const sw = parseFloat(document.getElementById('sw').value) || 0;
    const sd = parseFloat(document.getElementById('sd').value) || 0;

    // الحسابات
    const h_net = h - tax;
    const w_net = w - 5;
    const d_net = d - 5;

    // ملء جدول الألمنيوم
    let al_html = `
        <tr><td>قوائم الارتفاع</td><td class="fw-bold">${h_net}</td><td><span class="badge-qty">4</span></td></tr>
        <tr><td>عوارض العرض</td><td class="fw-bold">${w_net}</td><td><span class="badge-qty">4</span></td></tr>
        <tr><td>روابط العمق</td><td class="fw-bold">${d_net}</td><td><span class="badge-qty">4</span></td></tr>
    `;
    
    if(sn > 0) {
        al_html += `<tr><td>ألمنيوم عرض الرف</td><td class="fw-bold">${sw}</td><td><span class="badge-qty">${sn * 4}</span></td></tr>`;
        al_html += `<tr><td>ألمنيوم عمق الرف</td><td class="fw-bold">${sd}</td><td><span class="badge-qty">${sn * 4}</span></td></tr>`;
        al_html += `<tr><td>فواصل تدعيم</td><td class="fw-bold text-primary">${sw}</td><td><span class="badge-qty">${sn * 2}</span></td></tr>`;
    }
    document.getElementById('al_body').innerHTML = al_html;

    // ملء جدول الفيبر
    let fb_html = `<tr><td>فيبر الضهرية</td><td class="fw-bold">${w_net} × ${h_net}</td><td><span class="badge-qty">1</span></td></tr>`;
    if(sn > 0) {
        fb_html += `<tr><td>فيبر الرفوف (صافي)</td><td class="fw-bold text-danger">${sw - 5} × ${sd - 5}</td><td><span class="badge-qty">${sn}</span></td></tr>`;
    }
    document.getElementById('fb_body').innerHTML = fb_html;

    // إظهار النتائج
    document.getElementById('resultArea').style.display = 'block';
    window.scrollTo(0, document.body.scrollHeight);
}
</script>

</body>
</html>
