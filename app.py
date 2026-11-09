<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>حسابات ألمونتال | نظام إدارة مالي</title>
    
    <script src="https://www.gstatic.com/firebasejs/9.17.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.17.1/firebase-database-compat.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Cairo', sans-serif; }
        :root {
            --primary: #1a5276;
            --secondary: #2e86c1;
            --gold: #D4AF37;
            --success: #27ae60;
            --danger: #e74c3c;
            --warning: #f39c12;
            --dark: #1a1a2e;
            --light: #f4f6f9;
            --white: #ffffff;
        }
        body { background: var(--light); }
        
        header {
            background: var(--primary);
            color: white;
            padding: 10px 5%;
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        }
        .logo { font-size: 1.2rem; font-weight: 900; display: flex; align-items: center; gap: 8px; }
        .logo i { color: var(--gold); }
        .header-actions { display: flex; gap: 8px; flex-wrap: wrap; }
        .header-actions button {
            background: rgba(255,255,255,0.15);
            color: white;
            border: none;
            padding: 6px 14px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.8rem;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .header-actions button:hover { background: rgba(255,255,255,0.3); }
        
        .tabs {
            margin-top: 68px;
            background: white;
            padding: 0 5%;
            display: flex;
            gap: 3px;
            overflow-x: auto;
            border-bottom: 2px solid #e0e0e0;
            position: sticky;
            top: 58px;
            z-index: 90;
        }
        .tab {
            padding: 12px 18px;
            cursor: pointer;
            font-weight: 700;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: 0.3s;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.9rem;
        }
        .tab.active { color: var(--primary); border-bottom-color: var(--primary); }
        
        .container { padding: 20px 5%; max-width: 1400px; margin: 0 auto; }
        .page { display: none; }
        .page.active { display: block; }
        
        .summary-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .summary-card {
            background: white;
            padding: 18px;
            border-radius: 15px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
            text-align: center;
            border-top: 4px solid var(--primary);
        }
        .summary-card.income { border-top-color: var(--success); }
        .summary-card.expense { border-top-color: var(--danger); }
        .summary-card.remaining { border-top-color: var(--warning); }
        .summary-card h3 { font-size: 1.6rem; margin-bottom: 5px; }
        .summary-card p { color: #666; font-size: 0.85rem; }
        .summary-card.income h3 { color: var(--success); }
        .summary-card.expense h3 { color: var(--danger); }
        .summary-card.remaining h3 { color: var(--warning); }
        
        .table-container {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .table-header {
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
            border-bottom: 1px solid #eee;
        }
        .table-header h2 { font-size: 1.1rem; color: var(--primary); }
        table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
        th, td { padding: 10px 12px; text-align: right; border-bottom: 1px solid #eee; }
        th { background: var(--light); font-weight: 700; color: var(--primary); font-size: 0.85rem; }
        tr:hover { background: #f8f9fa; }
        .total-row { background: #fff3cd !important; font-weight: 900; }
        .total-row td { color: var(--primary); font-size: 1rem; }
        
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 700;
            font-size: 0.85rem;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }
        .btn-primary { background: var(--primary); color: white; }
        .btn-success { background: var(--success); color: white; }
        .btn-danger { background: var(--danger); color: white; }
        .btn-warning { background: var(--warning); color: white; }
        .btn-sm { padding: 4px 10px; font-size: 0.75rem; }
        
        .modal {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.7);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .modal.active { display: flex; }
        .modal-box {
            background: white;
            border-radius: 20px;
            width: 100%;
            max-width: 550px;
            max-height: 90vh;
            overflow-y: auto;
            padding: 25px;
        }
        .modal-box h2 { color: var(--primary); margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: 600; font-size: 0.9rem; }
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ddd;
            font-family: inherit;
        }
        .form-group input:focus, .form-group select:focus { outline: none; border-color: var(--primary); }
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .modal-actions { display: flex; gap: 10px; margin-top: 20px; justify-content: flex-end; }
        
        .payment-options { display: flex; gap: 15px; margin-top: 5px; }
        .payment-option {
            flex: 1;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 10px;
            cursor: pointer;
            text-align: center;
            font-weight: 700;
            transition: 0.2s;
        }
        .payment-option.selected { border-color: var(--success); background: #e8f8f0; color: var(--success); }
        
        .search-box { display: flex; gap: 10px; margin-bottom: 20px; }
        .search-box input {
            flex: 1;
            padding: 12px 20px;
            border-radius: 30px;
            border: 2px solid #ddd;
            font-size: 1rem;
        }
        .search-box input:focus { outline: none; border-color: var(--primary); }
        
        .weekly-container {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
        }
        .weekly-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .status-badge {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 8px 16px;
            border-radius: 25px;
            font-weight: 700;
            font-size: 0.8rem;
            z-index: 200;
        }
        .status-online { background: var(--success); color: white; }
        .status-offline { background: var(--warning); color: white; }
        
        @media (max-width: 700px) {
            .form-row { grid-template-columns: 1fr; }
            .table-container { overflow-x: auto; }
            table { min-width: 550px; }
            .payment-options { flex-direction: column; }
        }
    </style>
</head>
<body>

<header>
    <div class="logo"><i class="fas fa-utensils"></i> حسابات ألمونتال</div>
    <div class="header-actions">
        <button onclick="window.print()"><i class="fas fa-print"></i> طباعة</button>
        <button onclick="clearAllData()" style="background:rgba(231,76,60,0.3);"><i class="fas fa-trash"></i> مسح الكل</button>
    </div>
</header>

<div class="tabs">
    <div class="tab active" onclick="showPage('dashboard', this)"><i class="fas fa-chart-pie"></i> لوحة التحكم</div>
    <div class="tab" onclick="showPage('income', this)"><i class="fas fa-arrow-down"></i> الداخل</div>
    <div class="tab" onclick="showPage('expense', this)"><i class="fas fa-arrow-up"></i> الخارج</div>
    <div class="tab" onclick="showPage('weekly', this)"><i class="fas fa-calendar-week"></i> الجدول الأسبوعي</div>
    <div class="tab" onclick="showPage('search', this)"><i class="fas fa-search"></i> البحث</div>
</div>

<div class="container">

    <!-- لوحة التحكم -->
    <div class="page active" id="dashboard">
        <div class="summary-cards">
            <div class="summary-card income"><h3 id="totalIncome">0 ج</h3><p>إجمالي الداخل</p></div>
            <div class="summary-card expense"><h3 id="totalExpense">0 ج</h3><p>إجمالي الخارج</p></div>
            <div class="summary-card remaining"><h3 id="totalRemaining">0 ج</h3><p>الباقي من الداخل</p></div>
            <div class="summary-card"><h3 id="totalCount">0</h3><p>إجمالي العمليات</p></div>
        </div>
        <div class="table-container">
            <div class="table-header"><h2><i class="fas fa-clock"></i> آخر العمليات</h2></div>
            <div style="overflow-x:auto;">
                <table>
                    <thead><tr><th>النوع</th><th>الاسم / الجهة</th><th>المبلغ</th><th>طريقة الدفع</th><th>التاريخ والوقت</th></tr></thead>
                    <tbody id="recentTable"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- الداخل -->
    <div class="page" id="income">
        <div class="summary-cards">
            <div class="summary-card income"><h3 id="incomeTotal">0 ج</h3><p>إجمالي الداخل</p></div>
            <div class="summary-card remaining"><h3 id="incomeRemaining">0 ج</h3><p>الباقي بعد المصروفات</p></div>
        </div>
        <div class="table-container">
            <div class="table-header">
                <h2><i class="fas fa-arrow-down"></i> سجل الداخل</h2>
                <button class="btn btn-success" onclick="openIncomeModal()"><i class="fas fa-plus"></i> إضافة دخل</button>
            </div>
            <div style="overflow-x:auto;">
                <table>
                    <thead><tr><th>#</th><th>اسم العميل</th><th>السعر</th><th>طريقة الدفع</th><th>التاريخ والوقت</th><th>إجراءات</th></tr></thead>
                    <tbody id="incomeTable"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- الخارج -->
    <div class="page" id="expense">
        <div class="summary-cards">
            <div class="summary-card expense"><h3 id="expenseTotal">0 ج</h3><p>إجمالي الخارج</p></div>
        </div>
        <div class="table-container">
            <div class="table-header">
                <h2><i class="fas fa-arrow-up"></i> سجل الخارج</h2>
                <button class="btn btn-danger" onclick="openExpenseModal()"><i class="fas fa-plus"></i> إضافة مصروف</button>
            </div>
            <div style="overflow-x:auto;">
                <table>
                    <thead><tr><th>#</th><th>السعر</th><th>الجهة</th><th>التاريخ</th><th>طريقة الدفع</th><th>إجراءات</th></tr></thead>
                    <tbody id="expenseTable"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- الجدول الأسبوعي -->
    <div class="page" id="weekly">
        <div class="weekly-container">
            <div class="weekly-header">
                <h2><i class="fas fa-calendar-week"></i> الجدول الأسبوعي</h2>
                <button class="btn btn-primary" onclick="addWeeklyTable()"><i class="fas fa-plus"></i> جدول أسبوع جديد</button>
            </div>
            <div id="weeklyTablesList"></div>
        </div>
    </div>

    <!-- البحث -->
    <div class="page" id="search">
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 ابحث عن اسم عميل أو جهة أو مبلغ..." oninput="searchData()">
        </div>
        <div class="table-container">
            <div class="table-header"><h2><i class="fas fa-search"></i> نتائج البحث</h2></div>
            <div style="overflow-x:auto;">
                <table>
                    <thead><tr><th>النوع</th><th>الاسم / الجهة</th><th>المبلغ</th><th>طريقة الدفع</th><th>التاريخ والوقت</th></tr></thead>
                    <tbody id="searchTable"></tbody>
                </table>
            </div>
        </div>
    </div>

</div>

<!-- مودال الداخل -->
<div class="modal" id="incomeModal">
    <div class="modal-box">
        <h2><i class="fas fa-arrow-down"></i> إضافة دخل جديد</h2>
        <div class="form-group">
            <label>اسم العميل *</label>
            <input type="text" id="incomeName" placeholder="اسم العميل">
        </div>
        <div class="form-group">
            <label>السعر (جنيه) *</label>
            <input type="number" id="incomeAmount" placeholder="0">
        </div>
        <div class="form-group">
            <label>طريقة الدفع *</label>
            <div class="payment-options">
                <div class="payment-option" data-type="income" data-value="نقدي" onclick="selectPayment(this)">💵 نقدي</div>
                <div class="payment-option" data-type="income" data-value="تحويل" onclick="selectPayment(this)">🏦 تحويل</div>
            </div>
        </div>
        <div class="modal-actions">
            <button class="btn btn-success" onclick="saveIncome()"><i class="fas fa-save"></i> حفظ</button>
            <button class="btn btn-danger" onclick="closeModal('incomeModal')">إلغاء</button>
        </div>
    </div>
</div>

<!-- مودال الخارج -->
<div class="modal" id="expenseModal">
    <div class="modal-box">
        <h2><i class="fas fa-arrow-up"></i> إضافة مصروف جديد</h2>
        <div class="form-group">
            <label>السعر (جنيه) *</label>
            <input type="number" id="expenseAmount" placeholder="0">
        </div>
        <div class="form-group">
            <label>الجهة *</label>
            <input type="text" id="expenseParty" placeholder="مين اللي اتدفع له؟">
        </div>
        <div class="form-group">
            <label>التاريخ *</label>
            <input type="date" id="expenseDate">
        </div>
        <div class="form-group">
            <label>طريقة الدفع *</label>
            <div class="payment-options">
                <div class="payment-option" data-type="expense" data-value="نقدي" onclick="selectPayment(this)">💵 نقدي</div>
                <div class="payment-option" data-type="expense" data-value="تحويل" onclick="selectPayment(this)">🏦 تحويل</div>
            </div>
        </div>
        <div class="modal-actions">
            <button class="btn btn-danger" onclick="saveExpense()"><i class="fas fa-save"></i> حفظ</button>
            <button class="btn btn-danger" onclick="closeModal('expenseModal')">إلغاء</button>
        </div>
    </div>
</div>

<!-- حالة الاتصال -->
<div class="status-badge status-offline" id="statusBadge">📱 وضع محلي (البيانات على جهازك)</div>

<script>
    // ===== Firebase (اختياري - لو فشل يستخدم LocalStorage) =====
    let useFirebase = false;
    let db = null;
    
    try {
        const firebaseConfig = { databaseURL: "https://ded-el-kasr-default-rtdb.firebaseio.com/" };
        firebase.initializeApp(firebaseConfig);
        db = firebase.database();
        useFirebase = true;
        document.getElementById('statusBadge').className = 'status-badge status-online';
        document.getElementById('statusBadge').innerText = '☁️ متصل بالسحابة (من أي جهاز)';
    } catch(e) {
        console.log('Firebase غير متاح - استخدام LocalStorage');
    }

    // ===== البيانات =====
    let incomeData = JSON.parse(localStorage.getItem('incomeData') || '[]');
    let expenseData = JSON.parse(localStorage.getItem('expenseData') || '[]');
    let weeklyTables = JSON.parse(localStorage.getItem('weeklyTables') || '[]');
    let selectedPaymentIncome = '';
    let selectedPaymentExpense = '';

    // ===== حفظ محلي =====
    function saveLocal() {
        localStorage.setItem('incomeData', JSON.stringify(incomeData));
        localStorage.setItem('expenseData', JSON.stringify(expenseData));
        localStorage.setItem('weeklyTables', JSON.stringify(weeklyTables));
    }

    // ===== التبويبات =====
    function showPage(pageId, tab) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.getElementById(pageId).classList.add('active');
        tab.classList.add('active');
        if(pageId === 'dashboard') loadDashboard();
        if(pageId === 'income') loadIncome();
        if(pageId === 'expense') loadExpense();
        if(pageId === 'weekly') loadWeeklyTables();
        if(pageId === 'search') searchData();
    }

    // ===== اختيار طريقة الدفع =====
    function selectPayment(el) {
        const type = el.dataset.type;
        const parent = el.parentElement;
        parent.querySelectorAll('.payment-option').forEach(o => o.classList.remove('selected'));
        el.classList.add('selected');
        if(type === 'income') selectedPaymentIncome = el.dataset.value;
        else selectedPaymentExpense = el.dataset.value;
    }

    function closeModal(id) {
        document.getElementById(id).classList.remove('active');
        document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('selected'));
        selectedPaymentIncome = '';
        selectedPaymentExpense = '';
    }

    // ===== الداخل =====
    function openIncomeModal() {
        selectedPaymentIncome = '';
        document.getElementById('incomeName').value = '';
        document.getElementById('incomeAmount').value = '';
        document.getElementById('incomeModal').classList.add('active');
    }

    function saveIncome() {
        const name = document.getElementById('incomeName').value.trim();
        const amount = parseFloat(document.getElementById('incomeAmount').value);
        if(!name || !amount) { alert('أدخل اسم العميل والسعر'); return; }
        if(!selectedPaymentIncome) { alert('اختر طريقة الدفع'); return; }
        
        const now = new Date();
        const item = {
            id: Date.now().toString(),
            name: name,
            amount: amount,
            payment: selectedPaymentIncome,
            date: now.toLocaleDateString('ar-EG'),
            time: now.toLocaleTimeString('ar-EG'),
            timestamp: now.getTime()
        };
        
        incomeData.push(item);
        saveLocal();
        
        if(useFirebase && db) {
            db.ref('income').push(item).catch(e => console.log('Firebase error:', e));
        }
        
        alert('✅ تم الحفظ بنجاح');
        closeModal('incomeModal');
        loadIncome();
    }

    function loadIncome() {
        const table = document.getElementById('incomeTable');
        let html = '';
        let total = 0;
        const sorted = [...incomeData].sort((a,b) => b.timestamp - a.timestamp);
        if(sorted.length === 0) html = '<tr><td colspan="6" style="text-align:center;">لا يوجد دخل مسجل</td></tr>';
        sorted.forEach((item, idx) => {
            total += item.amount;
            html += `<tr>
                <td>${idx+1}</td>
                <td>${item.name}</td>
                <td style="color:var(--success); font-weight:700;">${item.amount} ج</td>
                <td>${item.payment}</td>
                <td>${item.date} - ${item.time}</td>
                <td><button class="btn btn-danger btn-sm" onclick="deleteIncome('${item.id}')"><i class="fas fa-trash"></i></button></td>
            </tr>`;
        });
        html += `<tr class="total-row"><td colspan="2">الإجمالي</td><td>${total} ج</td><td colspan="3"></td></tr>`;
        table.innerHTML = html;
        document.getElementById('incomeTotal').innerText = total + ' ج';
        const expTotal = expenseData.reduce((s, i) => s + i.amount, 0);
        document.getElementById('incomeRemaining').innerText = (total - expTotal) + ' ج';
    }

    function deleteIncome(id) {
        if(confirm('حذف هذا الدخل؟')) {
            incomeData = incomeData.filter(i => i.id !== id);
            saveLocal();
            if(useFirebase && db) db.ref('income').orderByChild('id').equalTo(id).once('value').then(s => s.forEach(c => c.ref.remove()));
            loadIncome();
        }
    }

    // ===== الخارج =====
    function openExpenseModal() {
        selectedPaymentExpense = '';
        document.getElementById('expenseAmount').value = '';
        document.getElementById('expenseParty').value = '';
        document.getElementById('expenseDate').value = new Date().toISOString().split('T')[0];
        document.getElementById('expenseModal').classList.add('active');
    }

    function saveExpense() {
        const amount = parseFloat(document.getElementById('expenseAmount').value);
        const party = document.getElementById('expenseParty').value.trim();
        const date = document.getElementById('expenseDate').value;
        if(!amount || !party) { alert('أدخل السعر والجهة'); return; }
        if(!selectedPaymentExpense) { alert('اختر طريقة الدفع'); return; }
        
        const now = new Date();
        const item = {
            id: Date.now().toString(),
            amount: amount,
            party: party,
            date: date || now.toLocaleDateString('ar-EG'),
            payment: selectedPaymentExpense,
            time: now.toLocaleTimeString('ar-EG'),
            timestamp: now.getTime()
        };
        
        expenseData.push(item);
        saveLocal();
        
        if(useFirebase && db) {
            db.ref('expense').push(item).catch(e => console.log('Firebase error:', e));
        }
        
        alert('✅ تم الحفظ بنجاح');
        closeModal('expenseModal');
        loadExpense();
    }

    function loadExpense() {
        const table = document.getElementById('expenseTable');
        let html = '';
        let total = 0;
        const sorted = [...expenseData].sort((a,b) => b.timestamp - a.timestamp);
        if(sorted.length === 0) html = '<tr><td colspan="6" style="text-align:center;">لا يوجد مصروفات</td></tr>';
        sorted.forEach((item, idx) => {
            total += item.amount;
            html += `<tr>
                <td>${idx+1}</td>
                <td style="color:var(--danger); font-weight:700;">${item.amount} ج</td>
                <td>${item.party}</td>
                <td>${item.date}</td>
                <td>${item.payment}</td>
                <td><button class="btn btn-danger btn-sm" onclick="deleteExpense('${item.id}')"><i class="fas fa-trash"></i></button></td>
            </tr>`;
        });
        html += `<tr class="total-row"><td>الإجمالي</td><td>${total} ج</td><td colspan="4"></td></tr>`;
        table.innerHTML = html;
        document.getElementById('expenseTotal').innerText = total + ' ج';
    }

    function deleteExpense(id) {
        if(confirm('حذف هذا المصروف؟')) {
            expenseData = expenseData.filter(i => i.id !== id);
            saveLocal();
            if(useFirebase && db) db.ref('expense').orderByChild('id').equalTo(id).once('value').then(s => s.forEach(c => c.ref.remove()));
            loadExpense();
        }
    }

    // ===== لوحة التحكم =====
    function loadDashboard() {
        let totalInc = 0, totalExp = 0;
        let recent = [];
        incomeData.forEach(v => {
            totalInc += v.amount;
            recent.push({ type: 'داخل', name: v.name, amount: v.amount, payment: v.payment, date: v.date, time: v.time, timestamp: v.timestamp });
        });
        expenseData.forEach(v => {
            totalExp += v.amount;
            recent.push({ type: 'خارج', name: v.party, amount: v.amount, payment: v.payment, date: v.date, time: v.time || '--', timestamp: v.timestamp });
        });
        recent.sort((a, b) => b.timestamp - a.timestamp);
        document.getElementById('totalIncome').innerText = totalInc + ' ج';
        document.getElementById('totalExpense').innerText = totalExp + ' ج';
        document.getElementById('totalRemaining').innerText = (totalInc - totalExp) + ' ج';
        document.getElementById('totalCount').innerText = recent.length;
        
        let html = '';
        recent.slice(0, 10).forEach(r => {
            const color = r.type === 'داخل' ? 'var(--success)' : 'var(--danger)';
            html += `<tr>
                <td style="color:${color}; font-weight:700;">${r.type}</td>
                <td>${r.name}</td>
                <td>${r.amount} ج</td>
                <td>${r.payment}</td>
                <td>${r.date} - ${r.time}</td>
            </tr>`;
        });
        document.getElementById('recentTable').innerHTML = html || '<tr><td colspan="5" style="text-align:center;">لا توجد عمليات</td></tr>';
    }

    // ===== البحث =====
    function searchData() {
        const query = document.getElementById('searchInput').value.trim().toLowerCase();
        if(!query) { document.getElementById('searchTable').innerHTML = '<tr><td colspan="5" style="text-align:center;">اكتب حاجة للبحث</td></tr>'; return; }
        
        let results = [];
        incomeData.forEach(v => {
            if(v.name.toLowerCase().includes(query) || String(v.amount).includes(query) || v.payment.toLowerCase().includes(query)) {
                results.push({ type: 'داخل', name: v.name, amount: v.amount, payment: v.payment, date: v.date, time: v.time, timestamp: v.timestamp });
            }
        });
        expenseData.forEach(v => {
            if(v.party.toLowerCase().includes(query) || String(v.amount).includes(query) || v.payment.toLowerCase().includes(query)) {
                results.push({ type: 'خارج', name: v.party, amount: v.amount, payment: v.payment, date: v.date, time: v.time || '--', timestamp: v.timestamp });
            }
        });
        results.sort((a, b) => b.timestamp - a.timestamp);
        let html = '';
        if(results.length === 0) html = '<tr><td colspan="5" style="text-align:center;">لا توجد نتائج</td></tr>';
        results.forEach(r => {
            const color = r.type === 'داخل' ? 'var(--success)' : 'var(--danger)';
            html += `<tr>
                <td style="color:${color}; font-weight:700;">${r.type}</td>
                <td>${r.name}</td>
                <td>${r.amount} ج</td>
                <td>${r.payment}</td>
                <td>${r.date} - ${r.time}</td>
            </tr>`;
        });
        document.getElementById('searchTable').innerHTML = html;
    }

    // ===== الجدول الأسبوعي =====
    function addWeeklyTable() {
        const title = prompt('اكتب عنوان الجدول الأسبوعي (مثال: جدول الأسبوع الأول):');
        if(!title) return;
        weeklyTables.push({
            id: Date.now().toString(),
            title: title,
            factoryBalance: 0,
            moneySpent: 0,
            timestamp: Date.now()
        });
        saveLocal();
        loadWeeklyTables();
    }

    function loadWeeklyTables() {
        const container = document.getElementById('weeklyTablesList');
        if(weeklyTables.length === 0) { container.innerHTML = '<p style="text-align:center; color:#666;">لا توجد جداول أسبوعية - اضغط "جدول أسبوع جديد"</p>'; return; }
        let html = '';
        weeklyTables.sort((a,b) => b.timestamp - a.timestamp).forEach(t => {
            html += `
                <div style="border:2px solid var(--primary); border-radius:15px; padding:15px; margin-bottom:15px; background:white;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:10px;">
                        <input type="text" value="${t.title}" onchange="updateWeeklyTitle('${t.id}', this.value)" style="flex:1; padding:8px; border-radius:8px; border:1px solid #ddd; font-weight:700; font-size:1rem;">
                        <button class="btn btn-danger btn-sm" onclick="deleteWeeklyTable('${t.id}')"><i class="fas fa-trash"></i> حذف</button>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
                        <div>
                            <label style="font-weight:700; font-size:0.85rem;">باقي في حساب المصنع</label>
                            <input type="number" value="${t.factoryBalance || 0}" onchange="updateWeeklyField('${t.id}', 'factoryBalance', this.value)" style="width:100%; padding:8px; border-radius:8px; border:1px solid #ddd;">
                        </div>
                        <div>
                            <label style="font-weight:700; font-size:0.85rem;">الفلوس اللي اتصرفت</label>
                            <input type="number" value="${t.moneySpent || 0}" onchange="updateWeeklyField('${t.id}', 'moneySpent', this.value)" style="width:100%; padding:8px; border-radius:8px; border:1px solid #ddd;">
                        </div>
                    </div>
                    <div style="background:#f0f0f0; padding:10px; border-radius:10px; text-align:center;">
                        <strong>الباقي النهائي: ${(t.factoryBalance || 0) - (t.moneySpent || 0)} ج</strong>
                    </div>
                </div>
            `;
        });
        container.innerHTML = html;
    }

    function updateWeeklyTitle(id, val) {
        const t = weeklyTables.find(x => x.id === id);
        if(t) { t.title = val; saveLocal(); }
    }
    function updateWeeklyField(id, field, val) {
        const t = weeklyTables.find(x => x.id === id);
        if(t) { t[field] = parseFloat(val) || 0; saveLocal(); loadWeeklyTables(); }
    }
    function deleteWeeklyTable(id) {
        if(confirm('حذف الجدول؟')) {
            weeklyTables = weeklyTables.filter(x => x.id !== id);
            saveLocal();
            loadWeeklyTables();
        }
    }

    function clearAllData() {
        if(confirm('مسح كل البيانات؟ (لا يمكن الرجوع)')) {
            localStorage.clear();
            incomeData = [];
            expenseData = [];
            weeklyTables = [];
            loadDashboard();
            alert('تم مسح كل البيانات');
            location.reload();
        }
    }

    // ===== التهيئة =====
    loadDashboard();
    loadIncome();
    loadExpense();
</script>
</body>
</html>
