from flask import Flask, render_template_string, request

app = Flask(__name__)

# واجهة المستخدم (HTML + CSS) في ملف واحد
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نظام الورشة المعتمد - تخصيم متكامل</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.rtl.min.css">
    <style>
        body { background-color: #f4f7f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .main-card { border-radius: 15px; border: none; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-top: 30px; }
        .header-bg { background: linear-gradient(45deg, #2c3e50, #34495e); color: white; padding: 25px; border-radius: 15px 15px 0 0; }
        .result-header-al { background-color: #27ae60; color: white; padding: 10px; border-radius: 8px 8px 0 0; }
        .result-header-fb { background-color: #e67e22; color: white; padding: 10px; border-radius: 8px 8px 0 0; }
        .table-custom { background: white; border-radius: 0 0 8px 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .badge-count { background-color: #2c3e50; color: white; font-size: 0.9rem; }
    </style>
</head>
<body>
<div class="container pb-5">
    <div class="card main-card">
        <div class="header-bg text-center">
            <h2>🏗️ نظام التخصيم المعتمد (المهندس ياسين)</h2>
            <p class="mb-0">تقسيم تلقائي للألمنيوم والفيبر مع حساب الفواصل</p>
        </div>
        <div class="card-body p-4">
            <form method="POST">
                <div class="row g-3">
                    <div class="col-md-3">
                        <label class="form-label fw-bold">العرض الكلي (W)</label>
                        <input type="number" step="0.1" name="w" class="form-control" value="{{request.form.w or '100'}}" required>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label fw-bold">الارتفاع الكلي (H)</label>
                        <input type="number" step="0.1" name="h" class="form-control" value="{{request.form.h or '90'}}" required>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label fw-bold">العمق الكلي (D)</label>
                        <input type="number" step="0.1" name="d" class="form-control" value="{{request.form.d or '50'}}" required>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label fw-bold">نوع الوحدة</label>
                        <select name="u_type" class="form-select">
                            <option value="سفلية" {% if request.form.u_type == 'سفلية' %}selected{% endif %}>سفلية (تخصيم 13)</option>
                            <option value="علوية" {% if request.form.u_type == 'علوية' %}selected{% endif %}>علوية (تخصيم 5)</option>
                        </select>
                    </div>
                    <div class="col-md-4">
                        <label class="form-label">عرض الرف</label>
                        <input type="number" step="0.1" name="sh_w" class="form-control" value="{{request.form.sh_w or '0'}}">
                    </div>
                    <div class="col-md-4">
                        <label class="form-label">عمق الرف</label>
                        <input type="number" step="0.1" name="sh_d" class="form-control" value="{{request.form.sh_d or '0'}}">
                    </div>
                    <div class="col-md-4">
                        <label class="form-label">عدد الرفوف</label>
                        <input type="number" name="sh_n" class="form-control" value="{{request.form.sh_n or '0'}}">
                    </div>
                    <div class="col-12 text-center">
                        <button type="submit" class="btn btn-primary btn-lg px-5 mt-3 shadow">🚀 إصدار أمر التشغيل</button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    {% if results %}
    <div class="row mt-4 g-4">
        <div class="col-md-6">
            <div class="result-header-al text-center">
                <h5 class="mb-0">📏 مقاسات تقطيع الألمنيوم</h5>
            </div>
            <div class="table-custom">
                <table class="table table-hover mb-0 text-center border">
                    <thead class="table-light">
                        <tr>
                            <th>البند</th>
                            <th>المقاس (سم)</th>
                            <th>العدد</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in results.aluminum %}
                        <tr>
                            <td>{{ item.item }}</td>
                            <td class="fw-bold text-success">{{ item.size }}</td>
                            <td><span class="badge badge-count">{{ item.count }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <div class="col-md-6">
            <div class="result-header-fb text-center">
                <h5 class="mb-0">🔲 مقاسات تقطيع الفيبر</h5>
            </div>
            <div class="table-custom">
                <table class="table table-hover mb-0 text-center border">
                    <thead class="table-light">
                        <tr>
                            <th>البند</th>
                            <th>المقاس (عرض × ارتفاع)</th>
                            <th>العدد</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in results.fiber %}
                        <tr>
                            <td>{{ item.item }}</td>
                            <td class="fw-bold text-danger">{{ item.size }}</td>
                            <td><span class="badge badge-count">{{ item.count }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        try:
            w = float(request.form.get('w'))
            h = float(request.form.get('h'))
            d = float(request.form.get('d'))
            u_type = request.form.get('u_type')
            
            sh_n = int(request.form.get('sh_n', 0))
            sh_w = float(request.form.get('sh_w', 0))
            sh_d = float(request.form.get('sh_d', 0))

            # 1. حسابات الهيكل (ألمنيوم)
            h_net = h - 13 if u_type == "سفلية" else h - 5
            w_net, d_net = w - 5, d - 5

            aluminum = [
                {"item": "قوائم الارتفاع", "size": h_net, "count": 4},
                {"item": "عوارض العرض", "size": w_net, "count": 4},
                {"item": "روابط العمق", "size": d_net, "count": 4}
            ]
            
            # حسابات الرفوف (ألمنيوم وفواصل)
            if sh_n > 0:
                # ألمنيوم عرض الرف وعمق الرف (المقاس في 4 لكل رف)
                aluminum.append({"item": "ألمنيوم عرض الرف", "size": sh_w, "count": sh_n * 4})
                aluminum.append({"item": "ألمنيوم عمق الرف", "size": sh_d, "count": sh_n * 4})
                # إضافة فواصل الألمنيوم (التي تُنسى دائماً)
                aluminum.append({"item": "فواصل ألمنيوم (تدعيم)", "size": sh_w, "count": sh_n * 2})

            # 2. حسابات الفيبر
            fiber = [
                {"item": "فيبر الضهرية", "size": f"{w_net} × {h_net}", "count": 1}
            ]
            if sh_n > 0:
                # فيبر الرفوف (تخصيم 5 سم من مقاس الألمنيوم)
                fiber.append({"item": "فيبر الرفوف الصافي", "size": f"{sh_w - 5} × {sh_d - 5}", "count": sh_n})

            results = {"aluminum": aluminum, "fiber": fiber}
        except Exception as e:
            results = {"error": str(e)}

    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == '__main__':
    app.run(debug=True)
