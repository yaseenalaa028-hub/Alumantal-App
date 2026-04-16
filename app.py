from flask import Flask, render_template_string, request

app = Flask(__name__)

# كود الواجهة والمنطق في ملف واحد لضمان التحديث
HTML_SOURCE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>نظام الورشة المعتمد v3.0</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
    <style>
        body { background-color: #f0f2f5; font-family: 'Segoe UI', sans-serif; }
        .card { border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .res-al { border-top: 5px solid #28a745; }
        .res-fb { border-top: 5px solid #fd7e14; }
        .badge-dark { background-color: #343a40; color: white; padding: 5px 10px; border-radius: 5px; }
    </style>
</head>
<body class="container py-4">
    <div class="card p-4 mb-4">
        <h3 class="text-center mb-4 text-primary">🏗️ حاسبة التخصيم التفصيلي - المهندس ياسين</h3>
        <form method="POST">
            <div class="row g-3">
                <div class="col-md-3">
                    <label>العرض الكلي (W)</label>
                    <input type="number" step="0.1" name="w_val" class="form-control" value="{{w_val}}" required>
                </div>
                <div class="col-md-3">
                    <label>الارتفاع الكلي (H)</label>
                    <input type="number" step="0.1" name="h_val" class="form-control" value="{{h_val}}" required>
                </div>
                <div class="col-md-3">
                    <label>العمق الكلي (D)</label>
                    <input type="number" step="0.1" name="d_val" class="form-control" value="{{d_val}}" required>
                </div>
                <div class="col-md-3">
                    <label>نوع الوحدة</label>
                    <select name="u_type" class="form-select">
                        <option value="سفلية" {% if u_type == 'سفلية' %}selected{% endif %}>سفلية (تخصيم 13)</option>
                        <option value="علوية" {% if u_type == 'علوية' %}selected{% endif %}>علوية (تخصيم 5)</option>
                    </select>
                </div>
                <div class="col-md-4">
                    <label>عرض الرف</label>
                    <input type="number" step="0.1" name="s_w" class="form-control" value="{{s_w}}">
                </div>
                <div class="col-md-4">
                    <label>عمق الرف</label>
                    <input type="number" step="0.1" name="s_d" class="form-control" value="{{s_d}}">
                </div>
                <div class="col-md-4">
                    <label>عدد الرفوف</label>
                    <input type="number" name="s_n" class="form-control" value="{{s_n}}">
                </div>
                <div class="col-12 text-center mt-3">
                    <button type="submit" class="btn btn-success btn-lg px-5">🚀 تحديث وإصدار التخصيم</button>
                </div>
            </div>
        </form>
    </div>

    {% if al_data %}
    <div class="row g-4">
        <div class="col-md-6">
            <div class="card p-3 res-al h-100">
                <h5 class="text-success fw-bold">📏 قائمة تقطيع الألمنيوم</h5>
                <table class="table table-sm mt-2">
                    <thead><tr><th>البيان</th><th>المقاس</th><th>العدد</th></tr></thead>
                    <tbody>
                        {% for row in al_data %}
                        <tr><td>{{row.name}}</td><td class="fw-bold">{{row.size}}</td><td><span class="badge-dark">{{row.qty}}</span></td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card p-3 res-fb h-100">
                <h5 class="text-warning fw-bold">🔲 قائمة تقطيع الفيبر</h5>
                <table class="table table-sm mt-2">
                    <thead><tr><th>البيان</th><th>المقاس (صافي)</th><th>العدد</th></tr></thead>
                    <tbody>
                        {% for row in fb_data %}
                        <tr><td>{{row.name}}</td><td class="fw-bold text-danger">{{row.size}}</td><td><span class="badge-dark">{{row.qty}}</span></td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def run_app():
    # قيم افتراضية
    ctx = {'w_val':100, 'h_val':90, 'd_val':50, 's_w':0, 's_d':0, 's_n':0, 'u_type':'سفلية', 'al_data':None, 'fb_data':None}
    
    if request.method == 'POST':
        try:
            w = float(request.form.get('w_val', 0))
            h = float(request.form.get('h_val', 0))
            d = float(request.form.get('d_val', 0))
            ut = request.form.get('u_type')
            sn = int(request.form.get('s_n', 0))
            sw = float(request.form.get('s_w', 0))
            sd = float(request.form.get('s_d', 0))

            # التخصيمات
            h_res = h - 13 if ut == "سفلية" else h - 5
            w_res, d_res = w - 5, d - 5

            # تجميع الألمنيوم
            al = [
                {'name': 'قوائم الارتفاع', 'size': h_res, 'qty': 4},
                {'name': 'عوارض العرض', 'size': w_res, 'qty': 4},
                {'name': 'روابط العمق', 'size': d_res, 'qty': 4}
            ]
            if sn > 0:
                al.append({'name': 'ألمنيوم عرض الرف', 'size': sw, 'qty': sn * 4})
                al.append({'name': 'ألمنيوم عمق الرف', 'size': sd, 'qty': sn * 4})
                al.append({'name': 'فواصل تدعيم (ألمنيوم)', 'size': sw, 'qty': sn * 2})

            # تجميع الفيبر
            fb = [{'name': 'فيبر الضهرية', 'size': f"{w_res} × {h_res}", 'qty': 1}]
            if sn > 0:
                fb.append({'name': 'فيبر الرفوف (صافي)', 'size': f"{sw - 5} × {sd - 5}", 'qty': sn})

            # تحديث الـ Context
            ctx.update({'w_val':w, 'h_val':h, 'd_val':d, 's_w':sw, 's_d':sd, 's_n':sn, 'u_type':ut, 'al_data':al, 'fb_data':fb})
        except: pass
        
    return render_template_string(HTML_SOURCE, **ctx)

if __name__ == '__main__':
    # تشغيل مع خاصية التحديث التلقائي (Debug Mode)
    app.run(debug=True, port=5000)
