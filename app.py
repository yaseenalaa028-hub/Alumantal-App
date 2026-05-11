<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>DOGGA SYSTEM - تخصيم الدرف والمقابض</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Tahoma', 'Segoe UI', 'Cairo', sans-serif;
        }

        body {
            background: radial-gradient(circle at top right, #0d1117, #050505, #020c1b);
            color: #d9a066;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        h1 {
            color: #0096ff;
            text-align: center;
            text-shadow: 0 0 30px #0096ff;
            font-size: 2rem;
            margin-bottom: 10px;
        }

        h2, h3 {
            color: #d9a066;
            text-align: center;
            margin: 20px 0 15px;
        }

        .card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            border: 1px solid rgba(217, 160, 102, 0.4);
            padding: 20px;
            margin-bottom: 20px;
            backdrop-filter: blur(5px);
        }

        .grid-2, .grid-3 {
            display: grid;
            gap: 15px;
        }

        .grid-2 { grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); }
        .grid-3 { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }

        input, select, textarea {
            width: 100%;
            padding: 12px;
            background: #0d1117;
            border: 1px solid #0096ff;
            border-radius: 10px;
            color: #0096ff;
            font-size: 16px;
            outline: none;
        }

        input:focus, select:focus, textarea:focus {
            border-color: #d9a066;
            box-shadow: 0 0 10px rgba(217, 160, 102, 0.3);
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #d9a066;
        }

        button {
            background: rgba(0, 150, 255, 0.1);
            border: 2px solid #0096ff;
            color: #0096ff;
            padding: 12px 24px;
            border-radius: 30px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 10px;
        }

        button:hover {
            background: #d9a066;
            color: #1a1614;
            border-color: #d9a066;
            transform: scale(1.02);
        }

        .btn-small {
            padding: 8px 16px;
            font-size: 14px;
            width: auto;
        }

        .success {
            background: rgba(0, 255, 100, 0.2);
            border: 1px solid #00ff64;
            color: #00ff64;
            padding: 10px;
            border-radius: 10px;
            margin: 10px 0;
        }

        .warning {
            background: rgba(255, 100, 0, 0.2);
            border: 1px solid #ff6400;
            color: #ffa064;
            padding: 10px;
            border-radius: 10px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }

        th, td {
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid rgba(217, 160, 102, 0.3);
        }

        th {
            background: rgba(0, 150, 255, 0.2);
            color: #0096ff;
        }

        .expander {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            margin: 10px 0;
        }

        .expander-header {
            padding: 15px;
            cursor: pointer;
            background: rgba(0, 150, 255, 0.1);
            border-radius: 15px;
            font-weight: bold;
        }

        .expander-content {
            padding: 15px;
            display: none;
        }

        .expander.open .expander-content {
            display: block;
        }

        .metric {
            background: rgba(0, 150, 255, 0.15);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
        }

        .metric-value {
            font-size: 28px;
            font-weight: bold;
            color: #0096ff;
        }

        hr {
            border-color: rgba(217, 160, 102, 0.3);
            margin: 20px 0;
        }

        .nav-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        @media (max-width: 600px) {
            body { padding: 10px; }
            h1 { font-size: 1.5rem; }
            button { font-size: 14px; }
        }
    </style>
</head>
<body>
<div class="container">
    <h1>⚡ DOGGA SYSTEM - تخصيم الدرف والمقابض</h1>
    <p style="text-align: center; color: #d9a066;">إدارة المشاريع | حفظ تلقائي | تخصيم دقيق</p>

    <!-- شريط التنقل -->
    <div class="nav-buttons">
        <button onclick="showPage('main')" style="flex:1">🏠 الرئيسية</button>
        <button onclick="showPage('deduction')" style="flex:1">📦 تخصيم المشروع</button>
        <button onclick="showPage('handles')" style="flex:1">🔧 تخصيم الدرف والمقابض</button>
        <button onclick="showPage('inventory')" style="flex:1">📊 المخزون والتقارير</button>
    </div>

    <!-- الصفحة الرئيسية -->
    <div id="page-main" class="page">
        <div class="card">
            <h3>📋 ملخص المشروع</h3>
            <div id="project-summary"></div>
            <hr>
            <h3>📝 ملاحظات المشروع</h3>
            <textarea id="project-notes" rows="4" placeholder="اكتب ملاحظاتك هنا... (تحفظ تلقائياً)"></textarea>
            <div style="display: flex; gap: 10px; margin-top: 10px;">
                <button onclick="clearAllData()" style="background: rgba(255,0,0,0.2); border-color:#ff4444; color:#ff8888;">🗑️ حذف كل البيانات</button>
            </div>
        </div>
    </div>

    <!-- صفحة تخصيم الدرف والمقابض -->
    <div id="page-handles" class="page" style="display:none">
        <div class="card">
            <h3>🔧 تخصيم الدرف والمقابض</h3>
            <div class="warning" style="margin-bottom:15px">
                📏 الدرف: +7 سم هالك لكل قطعة<br>
                🔩 البلتي إن: (العرض + 2) ÷ 2، بدون هالك<br>
                🪵 الكلادينج: على مقاس الدرفة
            </div>

            <div class="grid-2">
                <div>
                    <label>📏 عرض الرف (سم)</label>
                    <input type="number" id="handle-width" value="100" step="1">
                </div>
                <div>
                    <label>📐 ارتفاع الرف (سم) - للكلادينج</label>
                    <input type="number" id="handle-height" value="50" step="1">
                </div>
            </div>

            <div class="grid-3">
                <div>
                    <label>🔩 عدد مقابض بلتي إن</label>
                    <input type="number" id="balti-qty" value="0" min="0">
                </div>
                <div>
                    <label>🥢 عدد مقابض درف (سوستة)</label>
                    <input type="number" id="darf-qty" value="0" min="0">
                </div>
                <div>
                    <label>🪵 عدد ألواح الكلادينج</label>
                    <input type="number" id="cladding-qty" value="0" min="0">
                </div>
            </div>

            <div>
                <label>🏷️ اسم الوحدة</label>
                <input type="text" id="handle-unit-name" placeholder="مثال: رف سفلي 120 سم">
            </div>

            <button onclick="addHandlesToProject()">✅ إضافة للمشروع</button>
        </div>

        <div class="card">
            <h3>📋 آخر المقابض المضافة</h3>
            <div id="handles-preview"></div>
        </div>
    </div>

    <!-- صفحة التخصيم الرئيسي -->
    <div id="page-deduction" class="page" style="display:none">
        <div class="card">
            <h3>🏗️ إضافة وحدة جديدة</h3>
            <div class="grid-2">
                <div><label>اسم الوحدة</label><input type="text" id="unit-name" placeholder="مثال: سفلي 80"></div>
                <div><label>نوع الوحدة</label>
                    <select id="unit-type">
                        <option>سفلي</option><option>علوي</option><option>دولاب خزين</option><option>مطبقيه</option>
                    </select>
                </div>
                <div><label>العرض الكلي (سم)</label><input type="number" id="unit-w" value="0" step="0.1"></div>
                <div><label>الارتفاع الكلي (سم)</label><input type="number" id="unit-h" value="0" step="0.1"></div>
                <div><label>العمق الكلي (سم)</label><input type="number" id="unit-d" value="0" step="0.1"></div>
            </div>

            <h3>📦 الأرفف (خانتين منفصلتين)</h3>
            <div class="grid-2">
                <div class="card">
                    <h4 style="color:#00ff64">🟢 فيبر</h4>
                    <label>عرض الرف</label><input type="number" id="shelf-fibre-w" value="0">
                    <label>عمق الرف</label><input type="number" id="shelf-fibre-d" value="0">
                    <label>العدد</label><input type="number" id="shelf-fibre-q" value="0">
                </div>
                <div class="card">
                    <h4 style="color:#ffaa00">🟡 أمونيا</h4>
                    <label>عرض الرف</label><input type="number" id="shelf-ammonia-w" value="0">
                    <label>عمق الرف</label><input type="number" id="shelf-ammonia-d" value="0">
                    <label>العدد</label><input type="number" id="shelf-ammonia-q" value="0">
                </div>
            </div>

            <div class="grid-3">
                <div><label>ارتفاع الفاصل</label><input type="number" id="v-h" value="0"></div>
                <div><label>عمق الفاصل</label><input type="number" id="v-d" value="0"></div>
                <div><label>عدد الفواصل</label><input type="number" id="v-q" value="0"></div>
            </div>

            <div class="grid-3">
                <div><label>عرض الدرج</label><input type="number" id="dr-w" value="0"></div>
                <div><label>عمق الدرج</label><input type="number" id="dr-d" value="0"></div>
                <div><label>عدد الأدراج</label><input type="number" id="dr-q" value="0"></div>
            </div>

            <button onclick="addUnitToProject()">✅ إضافة الوحدة للمشروع</button>
        </div>
    </div>

    <!-- صفحة المخزون والتقارير -->
    <div id="page-inventory" class="page" style="display:none">
        <div class="card">
            <h3>📊 استهلاك الخامات</h3>
            <div id="inventory-content"></div>
            <button onclick="exportToCSV()">📥 تحميل تقرير CSV</button>
        </div>
    </div>
</div>

<script>
    // ==================== البيانات والحفظ التلقائي ====================
    let projectData = [];
    let notes = "";

    function loadData() {
        const saved = localStorage.getItem("doga_project_data");
        if (saved) projectData = JSON.parse(saved);
        const savedNotes = localStorage.getItem("doga_project_notes");
        if (savedNotes) notes = savedNotes;
        document.getElementById("project-notes").value = notes;
        updateUI();
    }

    function saveData() {
        localStorage.setItem("doga_project_data", JSON.stringify(projectData));
        localStorage.setItem("doga_project_notes", document.getElementById("project-notes").value);
        notes = document.getElementById("project-notes").value;
        updateUI();
    }

    // ==================== دوال مساعدة ====================
    function addItem(unitName, category, itemName, length, qty, unitType, widthVal=null, heightVal=null) {
        projectData.push({
            unit: unitName,
            material: category,
            item: itemName,
            length: length,
            width: widthVal || length,
            height: heightVal || "-",
            qty: qty,
            type: unitType
        });
        saveData();
    }

    // ==================== تخصيم الدرف والمقابض ====================
    function addHandlesToProject() {
        const width = parseFloat(document.getElementById("handle-width").value);
        const height = parseFloat(document.getElementById("handle-height").value);
        const darfQty = parseInt(document.getElementById("darf-qty").value) || 0;
        const baltiQty = parseInt(document.getElementById("balti-qty").value) || 0;
        const claddingQty = parseInt(document.getElementById("cladding-qty").value) || 0;
        let unitName = document.getElementById("handle-unit-name").value.trim();
        if (!unitName) unitName = "وحدة غير مسماة";

        if (width <= 0) {
            alert("يرجى إدخال عرض الرف");
            return;
        }

        // الدرف +7 سم هالك
        for (let i = 0; i < darfQty; i++) {
            const darfSize = width + 7;
            addItem(unitName, "درف", `مقبض درف ${i+1}`, darfSize, 2, "درف");
        }

        // البلتي إن: (العرض + 2) / 2
        for (let i = 0; i < baltiQty; i++) {
            const baltiSize = (width + 2) / 2;
            addItem(unitName, "بلتي إن", `مقبض بلتي إن ${i+1}`, baltiSize, 2, "بلتي إن");
        }

        // الكلادينج: على مقاس الدرفة
        for (let i = 0; i < claddingQty; i++) {
            addItem(unitName, "كلادينج", `لوح كلادينج ${i+1}`, `${width}×${height}`, 1, "كلادينج", width, height);
        }

        alert(`✅ تمت الإضافة:\n- درف: ${darfQty*2} قطعة\n- بلتي إن: ${baltiQty*2} قطعة\n- كلادينج: ${claddingQty} لوح`);
        
        // تفريغ الحقول
        document.getElementById("darf-qty").value = "0";
        document.getElementById("balti-qty").value = "0";
        document.getElementById("cladding-qty").value = "0";
    }

    // ==================== إضافة وحدة كاملة ====================
    function addUnitToProject() {
        const unitName = document.getElementById("unit-name").value || "وحدة جديدة";
        const unitType = document.getElementById("unit-type").value;
        const W = parseFloat(document.getElementById("unit-w").value);
        const H = parseFloat(document.getElementById("unit-h").value);
        const D = parseFloat(document.getElementById("unit-d").value);

        if (W <= 0 || H <= 0) {
            alert("يرجى إدخال العرض والارتفاع");
            return;
        }

        const hDed = (unitType === "سفلي" || unitType === "دولاب خزين") ? 13 : 5;
        const fH = H - hDed;
        const fW = W - 5;
        const fD = D - 5;

        // ألومنيوم الهيكل
        if (unitType === "سفلي") {
            addItem(unitName, "ألومنيوم", "قائم ارتفاع", fH, 2, "مفرد");
            addItem(unitName, "ألومنيوم", "قائم ارتفاع", fH, 2, "متقارب");
            addItem(unitName, "ألومنيوم", "عارضة عرض", fW, 3, "مفرد");
            addItem(unitName, "ألومنيوم", "عارضة عرض", fW, 1, "متقارب");
            addItem(unitName, "ألومنيوم", "رباط عمق", fD, 2, "مفرد");
            addItem(unitName, "ألومنيوم", "رباط عمق", fD, 2, "متقارب");
        } else {
            addItem(unitName, "ألومنيوم", "قائم ارتفاع", fH, 2, "مفرد");
            addItem(unitName, "ألومنيوم", "قائم ارتفاع", fH, 2, "متقارب");
            addItem(unitName, "ألومنيوم", "عارضة عرض", fW, 2, "مفرد");
            addItem(unitName, "ألومنيوم", "عارضة عرض", fW, 2, "متقارب");
            addItem(unitName, "ألومنيوم", "رباط عمق", fD, 4, "متقارب");
        }

        // فيبر الهيكل
        addItem(unitName, "فيبر", "ضهرية", `${fW}×${fH}`, 1, "لوح");
        addItem(unitName, "فيبر", "أرضية", `${fW}×${fD}`, 1, "لوح");
        if (unitType !== "سفلي") addItem(unitName, "فيبر", "سقفية", `${fW}×${fD}`, 1, "لوح");
        addItem(unitName, "فيبر", "أجناب", `${fH}×${fD}`, 2, "لوح");

        // أرفف فيبر
        const sfw = parseFloat(document.getElementById("shelf-fibre-w").value);
        const sfd = parseFloat(document.getElementById("shelf-fibre-d").value);
        const sfq = parseInt(document.getElementById("shelf-fibre-q").value) || 0;
        if (sfq > 0 && sfw > 0 && sfd > 0) {
            addItem(unitName, "ألومنيوم", "عرض رف فيبر", sfw, sfq*2, "مفرد");
            addItem(unitName, "ألومنيوم", "عمق رف فيبر", sfd, sfq*2, "مفرد");
            addItem(unitName, "فيبر", "حشو رف فيبر", `${sfw-5}×${sfd-5}`, sfq, "لوح");
        }

        // أرفف أمونيا
        const saw = parseFloat(document.getElementById("shelf-ammonia-w").value);
        const sad = parseFloat(document.getElementById("shelf-ammonia-d").value);
        const saq = parseInt(document.getElementById("shelf-ammonia-q").value) || 0;
        if (saq > 0 && saw > 0 && sad > 0) {
            addItem(unitName, "ألومنيوم", "عرض رف أمونيا", saw, saq*2, "مفرد");
            addItem(unitName, "ألومنيوم", "عمق رف أمونيا", sad, saq*2, "مفرد");
            addItem(unitName, "أمونيا", "حشو رف أمونيا", `${saw-5}×${sad-5}`, saq, "لوح");
        }

        // فواصل
        const vh = parseFloat(document.getElementById("v-h").value);
        const vd = parseFloat(document.getElementById("v-d").value);
        const vq = parseInt(document.getElementById("v-q").value) || 0;
        if (vq > 0 && vh > 0 && vd > 0) {
            addItem(unitName, "ألومنيوم", "ارتفاع فاصل", vh, vq*2, "مفرد");
            addItem(unitName, "ألومنيوم", "عمق فاصل", vd, vq*2, "مفرد");
            addItem(unitName, "فيبر", "حشو فاصل", `${vh-5}×${vd-5}`, vq, "لوح");
        }

        // أدراج
        const dw = parseFloat(document.getElementById("dr-w").value);
        const dd = parseFloat(document.getElementById("dr-d").value);
        const dq = parseInt(document.getElementById("dr-q").value) || 0;
        if (dq > 0 && dw > 0 && dd > 0) {
            addItem(unitName, "ألومنيوم", "وش/ضهر درج", dw-2.5, dq*2, "علبه درج");
            addItem(unitName, "ألومنيوم", "جنب درج", dd, dq*2, "علبه درج");
            addItem(unitName, "فيبر", "أرضية درج", `${dw-7.5}×${dd-5}`, dq, "لوح");
        }

        alert(`✅ تمت إضافة الوحدة: ${unitName}`);
        
        // تفريغ الحقول
        document.getElementById("unit-w").value = "0";
        document.getElementById("unit-h").value = "0";
        document.getElementById("unit-d").value = "0";
    }

    // ==================== تحديث الواجهة ====================
    function updateUI() {
        // تحديث ملخص المشروع
        const summaryDiv = document.getElementById("project-summary");
        if (summaryDiv) {
            summaryDiv.innerHTML = `<div class="metric"><div class="metric-value">${projectData.length}</div><div>قطعة في المشروع</div></div>`;
        }

        // معاينة المقابض
        const handlesPreview = document.getElementById("handles-preview");
        if (handlesPreview) {
            const handles = projectData.filter(item => ["درف", "بلتي إن", "كلادينج"].includes(item.material));
            if (handles.length === 0) {
                handlesPreview.innerHTML = "<p>لا توجد مقابض مضافة بعد</p>";
            } else {
                let html = "<table><tr><th>الخامة</th><th>المقاس</th><th>العدد</th></tr>";
                handles.forEach(h => {
                    html += `<tr><td>${h.material}</td><td>${h.length}</td><td>${h.qty}</td></tr>`;
                });
                html += "</table>";
                handlesPreview.innerHTML = html;
            }
        }
    }

    // ==================== حساب المخزون ====================
    function updateInventory() {
        const inventoryDiv = document.getElementById("inventory-content");
        if (!inventoryDiv) return;

        // ألومنيوم
        let alumLengths = { مفرد: 0, متقارب: 0, "علبه درج": 0, درف: 0, "بلتي إن": 0 };
        let fibreArea = 0, ammoniaArea = 0;
        let claddingCount = 0;

        projectData.forEach(item => {
            if (item.material === "ألومنيوم") {
                let len = parseFloat(item.length);
                if (!isNaN(len)) alumLengths[item.type] = (alumLengths[item.type] || 0) + (len * item.qty);
            }
            if (item.material === "فيبر" && typeof item.length === "string" && item.length.includes("×")) {
                const parts = item.length.split("×");
                const w = parseFloat(parts[0]), h = parseFloat(parts[1]);
                if (!isNaN(w) && !isNaN(h)) fibreArea += w * h * item.qty;
            }
            if (item.material === "أمونيا" && typeof item.length === "string" && item.length.includes("×")) {
                const parts = item.length.split("×");
                const w = parseFloat(parts[0]), h = parseFloat(parts[1]);
                if (!isNaN(w) && !isNaN(h)) ammoniaArea += w * h * item.qty;
            }
            if (item.material === "كلادينج") claddingCount += item.qty;
            // درف وبلتي إن
            if (item.material === "درف") alumLengths["درف"] = (alumLengths["درف"] || 0) + (parseFloat(item.length) || 0) * item.qty;
            if (item.material === "بلتي إن") alumLengths["بلتي إن"] = (alumLengths["بلتي إن"] || 0) + (parseFloat(item.length) || 0) * item.qty;
        });

        let html = `<div class="grid-2">`;
        for (let type in alumLengths) {
            if (alumLengths[type] > 0) {
                const sticks = Math.ceil(alumLengths[type] / 600);
                html += `<div class="metric"><div class="metric-value">${sticks}</div><div>عود ${type}</div></div>`;
            }
        }
        const fibreSheets = Math.ceil(fibreArea / (280 * 130));
        const ammoniaSheets = Math.ceil(ammoniaArea / (280 * 130));
        html += `<div class="metric"><div class="metric-value">${fibreSheets}</div><div>لوح فيبر</div></div>`;
        html += `<div class="metric"><div class="metric-value">${ammoniaSheets}</div><div>لوح أمونيا</div></div>`;
        html += `<div class="metric"><div class="metric-value">${claddingCount}</div><div>لوح كلادينج</div></div>`;
        html += `</div><hr><div class="warning">📏 ملاحظة: الدرافيل طول 6 متر (600 سم)، البلتي إن بدون هالك، الكلادينج على مقاس الدرفة</div>`;

        inventoryDiv.innerHTML = html;
    }

    function exportToCSV() {
        if (projectData.length === 0) { alert("لا توجد بيانات للتصدير"); return; }
        let csv = "اسم الوحدة,الخامة,اسم القطعة,المقاس,العدد,نوع التخصيم\n";
        projectData.forEach(item => {
            csv += `"${item.unit}","${item.material}","${item.item}","${item.length}",${item.qty},"${item.type}"\n`;
        });
        const blob = new Blob(["\uFEFF" + csv], { type: "text/csv;charset=utf-8;" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "project_report.csv";
        link.click();
        URL.revokeObjectURL(link.href);
    }

    function clearAllData() {
        if (confirm("⚠️ هل أنت متأكد من حذف كل البيانات؟ لا يمكن التراجع!")) {
            projectData = [];
            notes = "";
            document.getElementById("project-notes").value = "";
            saveData();
            updateUI();
            alert("تم حذف جميع البيانات");
        }
    }

    // ==================== التنقل بين الصفحات ====================
    function showPage(page) {
        document.querySelectorAll(".page").forEach(p => p.style.display = "none");
        document.getElementById(`page-${page}`).style.display = "block";
        if (page === "inventory") updateInventory();
        if (page === "main") updateUI();
    }

    // ==================== التشغيل الأول ====================
    loadData();
    showPage("main");
    document.getElementById("project-notes").addEventListener("input", saveData);
</script>
</body>
</html>
