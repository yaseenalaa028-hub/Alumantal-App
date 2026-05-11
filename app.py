<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>ضجة سيستم - تخصيص المونتال والدرف والكلادينج</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Cairo', 'Tajawal', 'Tahoma', sans-serif;
        }

        body {
            background: #f0f2f5;
            min-height: 100vh;
            padding: 15px;
        }

        .app-wrapper {
            max-width: 700px;
            margin: 0 auto;
        }

        .header {
            background: linear-gradient(135deg, #1e3a5f, #0f2b3d);
            border-radius: 30px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        .logo {
            width: 65px;
            height: 65px;
            background: #ffc107;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 10px;
            font-size: 2rem;
        }

        .header h1 { color: white; font-size: 1.6rem; }
        .header p { color: rgba(255,255,255,0.8); font-size: 0.65rem; }

        .main-menu {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .menu-card {
            flex: 1;
            background: white;
            border-radius: 20px;
            padding: 15px 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            min-width: 100px;
        }

        .menu-card:hover {
            transform: translateY(-3px);
            background: #fff3cd;
            border-color: #ffc107;
        }

        .menu-icon { font-size: 1.8rem; margin-bottom: 8px; }
        .menu-card h3 { color: #1e3a5f; font-size: 0.9rem; }
        .menu-card p { color: #6c757d; font-size: 0.65rem; margin-top: 3px; }

        .tab-bar {
            display: flex;
            background: #e9ecef;
            border-radius: 50px;
            padding: 4px;
            margin-bottom: 20px;
            gap: 4px;
        }

        .tab {
            flex: 1;
            text-align: center;
            padding: 10px;
            border-radius: 40px;
            cursor: pointer;
            color: #495057;
            font-weight: bold;
            font-size: 0.8rem;
            transition: 0.3s;
        }

        .tab.active {
            background: linear-gradient(135deg, #1e3a5f, #0f2b3d);
            color: white;
        }

        .card {
            background: white;
            border-radius: 20px;
            padding: 18px;
            margin-bottom: 18px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .card-title {
            color: #1e3a5f;
            font-size: 1rem;
            margin-bottom: 12px;
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 8px;
            border-right: 3px solid #ffc107;
            padding-right: 10px;
        }

        .input-group { margin-bottom: 12px; }
        .input-group label { display: block; color: #495057; font-size: 0.7rem; margin-bottom: 4px; font-weight: 600; }
        .input-group input, .input-group select {
            width: 100%;
            padding: 10px;
            background: #fff9e6;
            border: 1px solid #ffc107;
            border-radius: 12px;
            color: #1e3a5f;
            font-size: 0.85rem;
        }
        .input-group input:focus { outline: none; border-color: #1e3a5f; background: white; }

        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #1e3a5f, #0f2b3d);
            border: none;
            border-radius: 25px;
            color: white;
            font-size: 0.9rem;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
            margin-top: 8px;
        }

        button:hover { opacity: 0.9; transform: scale(1.01); }
        .btn-outline { background: transparent; border: 1px solid #1e3a5f; color: #1e3a5f; }

        .result-box {
            background: #f8f9fa;
            border-radius: 16px;
            padding: 12px;
            margin-top: 12px;
            max-height: 260px;
            overflow-y: auto;
            border: 1px solid #e0e0e0;
        }

        .result-item {
            background: #fff9e6;
            padding: 8px;
            margin: 6px 0;
            border-radius: 10px;
            font-size: 0.75rem;
            border-right: 3px solid #ffc107;
            color: #1e3a5f;
        }

        .stat-card {
            background: #f8f9fa;
            border-radius: 16px;
            padding: 10px;
            text-align: center;
            margin-bottom: 8px;
            border: 1px solid #e0e0e0;
        }

        .stat-number { font-size: 1.3rem; font-weight: bold; color: #1e3a5f; }

        .excel-table { overflow-x: auto; margin: 12px 0; }
        .excel-table table { width: 100%; border-collapse: collapse; font-size: 0.7rem; }
        .excel-table th, .excel-table td { padding: 8px 5px; text-align: center; border-bottom: 1px solid #e0e0e0; }
        .excel-table th { background: #1e3a5f; color: white; }
        .excel-table input { width: 65px; padding: 5px; background: #fff9e6; border: 1px solid #ffc107; border-radius: 8px; text-align: center; }

        .total-cost { font-size: 1.1rem; font-weight: bold; color: #1e3a5f; text-align: center; padding: 10px; background: #fff9e6; border-radius: 16px; margin-top: 8px; border: 1px solid #ffc107; }
        .shelf-item { background: #f8f9fa; border-radius: 12px; padding: 10px; margin-bottom: 10px; border: 1px solid #e0e0e0; }
        .footer { text-align: center; padding: 12px; background: white; border-radius: 20px; margin-top: 10px; color: #6c757d; font-size: 0.6rem; border: 1px solid #e0e0e0; }
        .toast { position: fixed; bottom: 30px; left: 20px; right: 20px; background: #28a745; color: white; text-align: center; padding: 10px; border-radius: 25px; font-size: 0.8rem; z-index: 1000; }

        @media (max-width: 550px) {
            .menu-card h3 { font-size: 0.65rem; }
            .menu-icon { font-size: 1.2rem; }
            .tab { font-size: 0.6rem; padding: 6px; }
        }
    </style>
</head>
<body>
<div class="app-wrapper">

    <div class="header">
        <div class="logo">🎯</div>
        <h1>ضجة سيستم</h1>
        <p>نظام تخصيص المونتال والفيبر والدرف والكلادينج</p>
    </div>

    <div id="mainScreen">
        <div class="main-menu">
            <div class="menu-card" onclick="showScreen('deduction')">
                <div class="menu-icon">📦</div>
                <h3>تخصيص الوحدات</h3>
                <p>مونتال · فيبر · أمونيا</p>
            </div>
            <div class="menu-card" onclick="showScreen('handles')">
                <div class="menu-icon">🔧</div>
                <h3>تخصيم الدرف</h3>
                <p>درف · بلتي إن · كلادينج</p>
            </div>
            <div class="menu-card" onclick="showScreen('inventory')">
                <div class="menu-icon">📊</div>
                <h3>حساب الخامات</h3>
                <p>جرد وتسعير</p>
            </div>
        </div>
        <div class="footer">
            برمجة المهندس ياسين علاء © 2025<br>
            جميع الحقوق محفوظة - ضجة سيستم
        </div>
    </div>

    <div id="deductionScreen" style="display:none;">
        <div class="tab-bar">
            <div class="tab" onclick="goBack()">🏠 الرئيسية</div>
        </div>
        <div id="deductionContent"></div>
    </div>

    <div id="handlesScreen" style="display:none;">
        <div class="tab-bar">
            <div class="tab" onclick="goBack()">🏠 الرئيسية</div>
        </div>
        <div id="handlesContent"></div>
    </div>

    <div id="inventoryScreen" style="display:none;">
        <div class="tab-bar">
            <div class="tab" onclick="goBack()">🏠 الرئيسية</div>
        </div>
        <div id="inventoryContent"></div>
    </div>

</div>

<script>
    let projectData = [];
    let shelfCount = 1;
    let currentPreview = [];
    let currentHandles = [];
    let prices = {};

    function loadData() {
        let saved = localStorage.getItem("doga_project");
        if(saved) projectData = JSON.parse(saved);
        let savedPrices = localStorage.getItem("doga_prices");
        if(savedPrices) prices = JSON.parse(savedPrices);
    }

    function saveData() {
        localStorage.setItem("doga_project", JSON.stringify(projectData));
        localStorage.setItem("doga_prices", JSON.stringify(prices));
    }

    function showToast(msg) {
        let t = document.createElement("div");
        t.className = "toast";
        t.innerText = msg;
        document.body.appendChild(t);
        setTimeout(()=>t.remove(), 2000);
    }

    function getStats() {
        let stats = {
            montaal: { مفرد:0, متقارب:0, "علبه درج":0, درف:0, "بلتي إن":0 },
            fibreArea: 0, ammoniaArea: 0, claddingArea: 0
        };
        const sheetSize = 280 * 130;
        
        projectData.forEach(i => {
            if(i.material === "مونتال") {
                let v = parseFloat(i.dimensions.split(" ")[0]) || 0;
                stats.montaal[i.type] = (stats.montaal[i.type] || 0) + (v * i.qty);
            }
            if(i.material === "درف") {
                let v = parseFloat(i.dimensions.split(" ")[0]) || 0;
                stats.montaal["درف"] += v * i.qty;
            }
            if(i.material === "بلتي إن") {
                let v = parseFloat(i.dimensions.split(" ")[0]) || 0;
                stats.montaal["بلتي إن"] += v * i.qty;
            }
            if(i.material === "فيبر" && i.dimensions.includes("×")) {
                let p = i.dimensions.split("×");
                let w = parseFloat(p[0]), h = parseFloat(p[1].split(" ")[0]);
                if(!isNaN(w)&&!isNaN(h)) stats.fibreArea += w * h * i.qty;
            }
            if(i.material === "أمونيا" && i.dimensions.includes("×")) {
                let p = i.dimensions.split("×");
                let w = parseFloat(p[0]), h = parseFloat(p[1].split(" ")[0]);
                if(!isNaN(w)&&!isNaN(h)) stats.ammoniaArea += w * h * i.qty;
            }
            if(i.material === "كلادينج" && i.dimensions.includes("×")) {
                let p = i.dimensions.split("×");
                let w = parseFloat(p[0]), h = parseFloat(p[1].split(" ")[0]);
                if(!isNaN(w)&&!isNaN(h)) stats.claddingArea += w * h * i.qty;
            }
        });
        return stats;
    }

    function renderMontalTab() {
        let shelvesHtml = "";
        for(let i=1; i<=shelfCount; i++) {
            shelvesHtml += `
                <div class="shelf-item">
                    <div class="card-title">📌 الرف رقم ${i}</div>
                    <div class="input-group"><label>عرض الرف ${i} (سم)</label><input type="number" id="shelf-w-${i}" value="0" step="0.1"></div>
                    <div class="input-group"><label>عمق الرف ${i} (سم)</label><input type="number" id="shelf-d-${i}" value="0" step="0.1"></div>
                    <div class="input-group"><label>عدد الرفوف ${i}</label><input type="number" id="shelf-q-${i}" value="0" min="0"></div>
                    ${i > 1 ? `<button class="btn-outline" onclick="removeShelf(${i})" style="margin-top:5px;">🗑️ حذف</button>` : ''}
                </div>
            `;
        }
        return `
            <div class="card">
                <div class="card-title">📏 بيانات الوحدة</div>
                <div class="input-group"><label>اسم الوحدة</label><input type="text" id="unit-name" placeholder="مثال: مطبخ سفلي"></div>
                <div class="input-group"><label>نوع الوحدة</label>
                    <select id="unit-type"><option>سفلي</option><option>علوي</option><option>دولاب خزين</option><option>مطبقيه</option></select>
                </div>
                <div class="input-group"><label>العرض الكلي (سم)</label><input type="number" id="unit-w" value="0" step="0.1"></div>
                <div class="input-group"><label>الارتفاع الكلي (سم)</label><input type="number" id="unit-h" value="0" step="0.1"></div>
                <div class="input-group"><label>العمق الكلي (سم)</label><input type="number" id="unit-d" value="0" step="0.1"></div>
            </div>
            <div class="card">
                <div class="card-title">📦 الأرفف</div>
                ${shelvesHtml}
                <button class="btn-outline" onclick="addShelf()">➕ إضافة رف جديد</button>
            </div>
            <div class="card">
                <div class="card-title">📐 الفواصل</div>
                <div class="input-group"><label>ارتفاع الفاصل (سم)</label><input type="number" id="v-h" value="0" step="0.1"></div>
                <div class="input-group"><label>عمق الفاصل (سم)</label><input type="number" id="v-d" value="0" step="0.1"></div>
                <div class="input-group"><label>عدد الفواصل</label><input type="number" id="v-q" value="0" min="0"></div>
            </div>
            <div class="card">
                <div class="card-title">🗄️ الأدراج</div>
                <div class="input-group"><label>عرض الدرج (سم)</label><input type="number" id="dr-w" value="0" step="0.1"></div>
                <div class="input-group"><label>عمق الدرج (سم)</label><input type="number" id="dr-d" value="0" step="0.1"></div>
                <div class="input-group"><label>عدد الأدراج</label><input type="number" id="dr-q" value="0" min="0"></div>
            </div>
            <button onclick="calculatePreview()">📐 معاينة التخصيم</button>
            <div id="previewResult"></div>
            <button onclick="saveUnit()" style="margin-top:10px;">💾 حفظ الوحدة</button>
        `;
    }

    function addShelf() { shelfCount++; renderMontalContent(); }
    function removeShelf(id) { if(shelfCount>1) shelfCount--; renderMontalContent(); }

    function calculatePreview() {
        const unitType = document.getElementById("unit-type").value;
        const W = parseFloat(document.getElementById("unit-w").value)||0;
        const H = parseFloat(document.getElementById("unit-h").value)||0;
        const D = parseFloat(document.getElementById("unit-d").value)||0;
        const vH = parseFloat(document.getElementById("v-h").value)||0;
        const vD = parseFloat(document.getElementById("v-d").value)||0;
        const vQ = parseInt(document.getElementById("v-q").value)||0;
        const drW = parseFloat(document.getElementById("dr-w").value)||0;
        const drD = parseFloat(document.getElementById("dr-d").value)||0;
        const drQ = parseInt(document.getElementById("dr-q").value)||0;
        if(W<=0||H<=0) { showToast("أدخل العرض والارتفاع"); return; }
        currentPreview = [];
        const hDed = (unitType==="سفلي"||unitType==="دولاب خزين")?13:5;
        const fH = H-hDed, fW = W-5, fD = D-5;
        if(unitType==="سفلي") {
            currentPreview.push({item:"قائم ارتفاع",type:"مفرد",size:fH,qty:2});
            currentPreview.push({item:"قائم ارتفاع",type:"متقارب",size:fH,qty:2});
            currentPreview.push({item:"عارضة عرض",type:"مفرد",size:fW,qty:3});
            currentPreview.push({item:"عارضة عرض",type:"متقارب",size:fW,qty:1});
            currentPreview.push({item:"رباط عمق",type:"مفرد",size:fD,qty:2});
            currentPreview.push({item:"رباط عمق",type:"متقارب",size:fD,qty:2});
        } else {
            currentPreview.push({item:"قائم ارتفاع",type:"مفرد",size:fH,qty:2});
            currentPreview.push({item:"قائم ارتفاع",type:"متقارب",size:fH,qty:2});
            currentPreview.push({item:"عارضة عرض",type:"مفرد",size:fW,qty:2});
            currentPreview.push({item:"عارضة عرض",type:"متقارب",size:fW,qty:2});
            currentPreview.push({item:"رباط عمق",type:"متقارب",size:fD,qty:4});
        }
        currentPreview.push({item:"ضهرية",type:"فيبر",size:`${fW}×${fH}`,qty:1});
        currentPreview.push({item:"أرضية",type:"فيبر",size:`${fW}×${fD}`,qty:1});
        if(unitType!=="سفلي") currentPreview.push({item:"سقفية",type:"فيبر",size:`${fW}×${fD}`,qty:1});
        currentPreview.push({item:"أجناب",type:"فيبر",size:`${fH}×${fD}`,qty:2});
        for(let i=1; i<=shelfCount; i++) {
            const sw = parseFloat(document.getElementById(`shelf-w-${i}`).value)||0;
            const sd = parseFloat(document.getElementById(`shelf-d-${i}`).value)||0;
            const sq = parseInt(document.getElementById(`shelf-q-${i}`).value)||0;
            if(sq>0 && sw>0 && sd>0) {
                currentPreview.push({item:`عرض رف ${i}`,type:"مفرد",size:sw,qty:sq*2});
                currentPreview.push({item:`عمق رف ${i}`,type:"مفرد",size:sd,qty:sq*2});
                currentPreview.push({item:`حشو رف ${i} (فيبر)`,type:"فيبر",size:`${sw-5}×${sd-5}`,qty:sq});
                currentPreview.push({item:`حشو رف ${i} (أمونيا)`,type:"أمونيا",size:`${sw-5}×${sd-5}`,qty:sq});
            }
        }
        if(vQ>0 && vH>0 && vD>0) {
            currentPreview.push({item:"ارتفاع فاصل",type:"مفرد",size:vH,qty:vQ*2});
            currentPreview.push({item:"عمق فاصل",type:"مفرد",size:vD,qty:vQ*2});
            currentPreview.push({item:"حشو فاصل (فيبر)",type:"فيبر",size:`${vH-5}×${vD-5}`,qty:vQ});
        }
        if(drQ>0 && drW>0 && drD>0) {
            currentPreview.push({item:"وش/ضهر درج",type:"علبه درج",size:drW-2.5,qty:drQ*2});
            currentPreview.push({item:"جنب درج",type:"علبه درج",size:drD,qty:drQ*2});
            currentPreview.push({item:"أرضية درج (فيبر)",type:"فيبر",size:`${drW-7.5}×${drD-5}`,qty:drQ});
        }
        let html = `<div class="result-box"><div style="color:#1e3a5f; font-weight:bold;">📋 معاينة التخصيم:</div>`;
        currentPreview.forEach(r => { html += `<div class="result-item">🔹 ${r.item} (${r.type}): ${r.size} سم × ${r.qty}</div>`; });
        html += `</div>`;
        document.getElementById("previewResult").innerHTML = html;
    }

    function saveUnit() {
        if(currentPreview.length === 0) { showToast("احسب التخصيم أولاً"); return; }
        const unitName = document.getElementById("unit-name").value || "وحدة جديدة";
        currentPreview.forEach(r => {
            projectData.push({
                unit: unitName,
                material: (r.type==="مفرد"||r.type==="متقارب"||r.type==="علبه درج")?"مونتال":r.type,
                item: r.item,
                dimensions: typeof r.size==="number"?`${r.size} سم`:`${r.size} سم`,
                qty: r.qty,
                type: r.type
            });
        });
        saveData();
        showToast(`✅ تم حفظ ${currentPreview.length} قطعة`);
        currentPreview = [];
        document.getElementById("previewResult").innerHTML = "";
    }

    function renderMontalContent() {
        document.getElementById("deductionContent").innerHTML = renderMontalTab();
    }

    function renderHandlesTab() {
        return `
            <div class="card">
                <div class="card-title">🔧 تخصيم الدرف والكلادينج</div>
                <div class="input-group"><label>📏 ارتفاع الدرفة (سم)</label><input type="number" id="handle-height" value="0" step="0.1"></div>
                <div class="input-group"><label>📐 عرض الدرفة (سم)</label><input type="number" id="handle-width" value="0" step="0.1"></div>
                <div class="input-group"><label>🔢 عدد الدرف</label><input type="number" id="handle-count" value="1" min="1"></div>
                <div class="input-group"><label>🏷️ اسم المشروع</label><input type="text" id="handle-name" placeholder="مثال: درفة مطبخ"></div>
            </div>
            <button onclick="calcHandles()">🔧 حساب تخصيم الدرف والكلادينج</button>
            <div id="handlesPreview"></div>
            <button onclick="saveHandles()" style="margin-top:10px;">💾 حفظ في المشروع</button>
        `;
    }

    function calcHandles() {
        const height = parseFloat(document.getElementById("handle-height").value)||0;
        const width = parseFloat(document.getElementById("handle-width").value)||0;
        const count = parseInt(document.getElementById("handle-count").value)||1;
        if(height<=0 || width<=0) { showToast("أدخل ارتفاع وعرض الدرفة"); return; }
        currentHandles = [];
        let totalCladdingArea = 0;
        const sheetSize = 280 * 130;
        
        for(let i=0; i<count; i++) {
            currentHandles.push({item:"جنب أمونيا",type:"أمونيا",size:height,qty:2});
            currentHandles.push({item:"مقبض بلتي إن",type:"بلتي إن",size:width,qty:1});
            currentHandles.push({item:"درفة عدية (سوستة)",type:"درف",size:width,qty:1});
            totalCladdingArea += height * width;
            currentHandles.push({item:"لوح كلادينج",type:"كلادينج",size:`${height}×${width}`,qty:1});
        }
        
        const requiredSheets = Math.ceil(totalCladdingArea / sheetSize);
        
        let summary = {};
        currentHandles.forEach(r => { let k=r.type+"_"+r.item; if(!summary[k]) summary[k]={...r,qty:0}; summary[k].qty+=r.qty; });
        let html = `<div class="result-box"><div style="color:#1e3a5f; font-weight:bold;">📋 تخصيم ${count} درفة:</div>`;
        for(let k in summary) {
            let s = summary[k];
            let icon = s.type==="أمونيا"?"🟡":s.type==="بلتي إن"?"🔩":s.type==="درف"?"🥢":"🪵";
            html += `<div class="result-item">${icon} ${s.item} (${s.type}): ${s.size} ${s.type==="كلادينج"?"سم":"سم"} × ${s.qty}</div>`;
        }
        html += `<div class="total-cost" style="margin-top:10px;">📦 ألواح الكلادينج المطلوبة: ${requiredSheets} لوح (مقاس 280×130 سم)</div>`;
        html += `</div>`;
        document.getElementById("handlesPreview").innerHTML = html;
    }

    function saveHandles() {
        if(currentHandles.length===0) { showToast("احسب التخصيم أولاً"); return; }
        const name = document.getElementById("handle-name").value.trim() || "درفة جديدة";
        currentHandles.forEach(r => {
            projectData.push({
                unit: name,
                material: r.type,
                item: r.item,
                dimensions: `${r.size} ${r.type==="كلادينج"?"سم":"سم"}`,
                qty: r.qty,
                type: r.type
            });
        });
        saveData();
        showToast(`✅ تم حفظ ${currentHandles.length} قطعة`);
        currentHandles = [];
        document.getElementById("handlesPreview").innerHTML = "";
    }

    function renderHandlesContent() {
        document.getElementById("handlesContent").innerHTML = renderHandlesTab();
    }

    function renderInventoryContent() {
        const stats = getStats();
        const sheetSize = 280 * 130;
        
        let sheetItems = [
            {name:"مونتال مفرد", qty:Math.ceil(stats.montaal["مفرد"]/600), unit:"عود", price:prices["مونتال مفرد"]||0},
            {name:"مونتال متقارب", qty:Math.ceil(stats.montaal["متقارب"]/600), unit:"عود", price:prices["مونتال متقارب"]||0},
            {name:"مونتال علبة درج", qty:Math.ceil(stats.montaal["علبه درج"]/600), unit:"عود", price:prices["مونتال علبة درج"]||0},
            {name:"عود درف", qty:Math.ceil(stats.montaal["درف"]/600), unit:"عود", price:prices["عود درف"]||0},
            {name:"عود بلتي إن", qty:Math.ceil(stats.montaal["بلتي إن"]/600), unit:"عود", price:prices["عود بلتي إن"]||0},
            {name:"لوح فيبر", qty:Math.ceil(stats.fibreArea/sheetSize), unit:"لوح", price:prices["لوح فيبر"]||0},
            {name:"لوح أمونيا", qty:Math.ceil(stats.ammoniaArea/sheetSize), unit:"لوح", price:prices["لوح أمونيا"]||0},
            {name:"لوح كلادينج", qty:Math.ceil(stats.claddingArea/sheetSize), unit:"لوح", price:prices["لوح كلادينج"]||0}
        ];
        
        let total = 0;
        let tableHtml = `<div class="excel-table"><table><thead><tr><th>الصنف</th><th>الكمية</th><th>الوحدة</th><th>السعر</th><th>الإجمالي</th></tr></thead><tbody>`;
        sheetItems.forEach((item,idx) => {
            let totalItem = item.qty * item.price;
            total += totalItem;
            tableHtml += `<tr>
                <td>${item.name}</td>
                <td>${item.qty}</td>
                <td>${item.unit}</td>
                <td><input type="number" id="price_${idx}" value="${item.price}" style="width:70px;" onchange="updatePrice(${idx}, '${item.name}')"></td>
                <td style="color:#1e3a5f; font-weight:bold;">${totalItem.toFixed(2)}</td>
            </tr>`;
        });
        tableHtml += `</tbody></table></div><div class="total-cost">💰 التكلفة الإجمالية: ${total.toFixed(2)} ج.م</div>`;
        
        let projectsList = `<div class="card" style="margin-top:15px;"><div class="card-title">📁 القطع المحفوظة (${projectData.length})</div>`;
        if(projectData.length===0) projectsList += `<p style="text-align:center;">لا توجد بيانات</p>`;
        else {
            projectData.slice().reverse().slice(0,20).forEach(i => {
                projectsList += `<div class="result-item">📌 ${i.unit} | ${i.material} | ${i.item} | ${i.dimensions} | ×${i.qty}</div>`;
            });
        }
        projectsList += `<button class="btn-outline" onclick="clearAll()" style="margin-top:10px;">🗑️ مسح كل البيانات</button></div>`;
        
        document.getElementById("inventoryContent").innerHTML = `
            <div class="card">
                <div class="card-title">📊 إحصائيات الخامات المطلوبة</div>
                <div class="stat-card"><div class="stat-number">${Math.ceil(stats.montaal["مفرد"]/600)}</div><div>عود مفرد</div></div>
                <div class="stat-card"><div class="stat-number">${Math.ceil(stats.montaal["متقارب"]/600)}</div><div>عود متقارب</div></div>
                <div class="stat-card"><div class="stat-number">${Math.ceil(stats.montaal["علبه درج"]/600)}</div><div>عود علبة درج</div></div>
                <div class="stat-card"><div class="stat-number">${Math.ceil(stats.montaal["درف"]/600)}</div><div>عود درف</div></div>
                <div class="stat-card"><div class="stat-number">${Math.ceil(stats.montaal["بلتي إن"]/600)}</div><div>عود بلتي إن</div></div>
                <div class="stat-card"><div class="stat-number">${Math.ceil(stats.fibreArea/sheetSize)}</div><div>لوح فيبر (280×130)</div></div>
                <div class="stat-card"><div class="stat-number">${Math.ceil(stats.ammoniaArea/sheetSize)}</div><div>لوح أمونيا (280×130)</div></div>
                <div class="stat-card"><div class="stat-number">${Math.ceil(stats.claddingArea/sheetSize)}</div><div>لوح كلادينج (280×130)</div></div>
            </div>
            <div class="card">
                <div class="card-title">💰 جدول التسعير (مفتوح للتعديل)</div>
                ${tableHtml}
            </div>
            ${projectsList}
            <button onclick="exportFullData()" style="margin-top:10px;">📥 تحميل تقرير CSV كامل</button>
        `;
    }

    function updatePrice(idx, name) {
        let newPrice = parseFloat(document.getElementById(`price_${idx}`).value) || 0;
        prices[name] = newPrice;
        localStorage.setItem("doga_prices", JSON.stringify(prices));
        renderInventoryContent();
        showToast(`✅ تم تحديث سعر ${name}`);
    }

    function exportFullData() {
        if(projectData.length===0) { alert("لا توجد بيانات للتصدير"); return; }
        let csv = "الوحدة,الخامة,القطعة,المقاس,العدد,النوع\n";
        projectData.forEach(i => { csv += `"${i.unit}","${i.material}","${i.item}","${i.dimensions}",${i.qty},"${i.type||"-"}"\n`; });
        const blob = new Blob(["\uFEFF"+csv], {type:"text/csv"});
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "doga_full_report.csv";
        link.click();
        showToast("📁 تم تصدير التقرير");
    }

    function clearAll() {
        if(confirm("⚠️ مسح كل البيانات؟ لا يمكن التراجع!")) {
            projectData = [];
            prices = {};
            saveData();
            showToast("🗑️ تم مسح كل البيانات");
            if(document.getElementById("inventoryContent")) renderInventoryContent();
            else if(document.getElementById("deductionContent")) renderMontalContent();
        }
    }

    function showScreen(screen) {
        document.getElementById("mainScreen").style.display = "none";
        document.getElementById("deductionScreen").style.display = screen === 'deduction' ? "block" : "none";
        document.getElementById("handlesScreen").style.display = screen === 'handles' ? "block" : "none";
        document.getElementById("inventoryScreen").style.display = screen === 'inventory' ? "block" : "none";
        
        if(screen === 'deduction') renderMontalContent();
        if(screen === 'handles') renderHandlesContent();
        if(screen === 'inventory') renderInventoryContent();
    }

    function goBack() {
        document.getElementById("mainScreen").style.display = "block";
        document.getElementById("deductionScreen").style.display = "none";
        document.getElementById("handlesScreen").style.display = "none";
        document.getElementById("inventoryScreen").style.display = "none";
    }

    loadData();
    goBack();
</script>
</body>
</html>
