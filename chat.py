
import math
 
class Bank:
#ده الكونستراكتور بياخد 1 attribute  

    def __init__(self, customer_list=None):
        self.customer_list = []
        self.transactions = []

        if customer_list:
            for item in customer_list:
                if isinstance(item, dict):
                    customer_id = str(item.get("id", "")).strip()
                    balance = self.validate_amount(
                        item.get("balance", 0)
                    )

                    if customer_id and balance is not None:
                        if balance >= 0 and not self.find_customer(customer_id):
                            self.customer_list.append({
                                "id": customer_id,
                                "balance": balance
                            })

    # Validate amounts
    def validate_amount(self, amount):
        try:
            amount = float(amount)
            if math.isfinite(amount):
                return amount
            return None
        except (ValueError, TypeError):
            return None

    # Find customer
    def find_customer(self, customer_id):
        for customer in self.customer_list:
            if customer["id"] == str(customer_id):
                return customer
        return None

    # Add customer
    def add_customer(self, customer_id, balance=0):
        customer_id = str(customer_id).strip()
        balance = self.validate_amount(balance)

        if not customer_id:
            return "Invalid customer ID."

        if balance is None or balance < 0:
            return "Invalid balance."

        if self.find_customer(customer_id):
            return "Customer already exists."

        self.customer_list.append({
            "id": customer_id,
            "balance": balance
        })

        return "Customer added successfully."

    # Show customer balance
    def show_balance(self, customer_id):
        customer = self.find_customer(customer_id)

        if customer is None:
            return "Customer not found."

        return customer["balance"]

    # Deposit
    def deposit_money(self, customer_id, amount):
        customer = self.find_customer(customer_id)
        amount = self.validate_amount(amount)

        if customer is None:
            return "Customer not found."

        if amount is None or amount <= 0:
            return "Invalid amount."

        customer["balance"] += amount

        self.transactions.append({
            "type": "deposit",
            "customer_id": str(customer_id),
            "amount": amount
        })

        return "Deposit successful."

    # Withdraw
    def withdraw_money(self, customer_id, amount):
        customer = self.find_customer(customer_id)
        amount = self.validate_amount(amount)

        if customer is None:
            return "Customer not found."

        if amount is None or amount <= 0:
            return "Invalid amount."

        if customer["balance"] < amount:
            return "Insufficient balance."

        customer["balance"] -= amount

        self.transactions.append({
            "type": "withdraw",
            "customer_id": str(customer_id),
            "amount": amount
        })

        return "Withdraw successful."

    # Transfer money
    def transfer_money(self, sender_id, receiver_id, amount):
        sender = self.find_customer(sender_id)
        receiver = self.find_customer(receiver_id)
        amount = self.validate_amount(amount)

        if sender is None or receiver is None:
            return "Customer not found."

        if sender_id == receiver_id:
            return "Cannot transfer to the same account."

        if amount is None or amount <= 0:
            return "Invalid amount."

        if sender["balance"] < amount:
            return "Insufficient balance."

        sender["balance"] -= amount
        receiver["balance"] += amount

        self.transactions.append({
            "type": "transfer_out",
            "customer_id": str(sender_id),
            "amount": amount,
            "to": str(receiver_id)
        })

        self.transactions.append({
            "type": "transfer_in",
            "customer_id": str(receiver_id),
            "amount": amount,
            "from": str(sender_id)
        })

        return "Transfer successful."

    # Customer statistics
    def calculate_number_customer(self):
        if not self.customer_list:
            return "No customers found."

        sorted_customers = sorted(
            self.customer_list,
            key=lambda x: (
                0, int(x["id"])
            ) if x["id"].isdigit() else (
                1, x["id"]
            )
        )

        total_balance = sum(
            customer["balance"]
            for customer in self.customer_list
        )

        return {
            "total_balance": total_balance,
            "smallest_id": sorted_customers[0]["id"],
            "largest_id": sorted_customers[-1]["id"],
            "total_customers": len(self.customer_list)
        }

    # Transaction history
    def transaction_history(self, customer_id):
        if not self.find_customer(customer_id):
            return "Customer not found."

        history = [
            transaction
            for transaction in self.transactions
            if transaction["customer_id"] == str(customer_id)
        ]

        return history if history else "No transactions found."

    # Transaction statistics
    def average_access(self):
        if not self.transactions:
            return "No transactions found."

        deposits = [
            t["amount"] for t in self.transactions
            if t["type"] == "deposit"
        ]

        withdrawals = [
            t["amount"] for t in self.transactions
            if t["type"] == "withdraw"
        ]

        return {
            "total_operations": len(self.transactions),
            "deposit_count": len(deposits),
            "withdraw_count": len(withdrawals),
            "average_transaction": sum(
                t["amount"] for t in self.transactions
            ) / len(self.transactions)
        }



# ---------------- WEB DASHBOARD ----------------
# Run: python chat.py, then open http://127.0.0.1:8000
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json

initial_customers = [
    {"id":"12","balance":1000},{"id":"44","balance":2500},
    {"id":"55","balance":500},{"id":"60","balance":3000},
    {"id":"70","balance":1500},{"id":"80","balance":4000}
]
my_bank = Bank(initial_customers)
PAGE = r'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>نَقد | لوحة البنك</title>
<style>
:root{--bg:#f4f7f4;--surface:#fff;--ink:#182b25;--muted:#718079;--line:#e7eee9;--green:#167653;--shadow:0 14px 40px #193b2a12} [data-theme=dark]{--bg:#101b17;--surface:#182720;--ink:#eff8f1;--muted:#a0b2a8;--line:#2b3e34;--green:#62c796;--shadow:0 14px 40px #0005}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Tahoma,Arial,sans-serif;transition:.2s}button,input,select{font:inherit}.layout{max-width:1400px;margin:auto;display:grid;grid-template-columns:230px 1fr;min-height:100vh}.side{padding:26px 20px;background:var(--surface);border-left:1px solid var(--line)}.brand{font-size:23px;font-weight:bold;margin-bottom:40px}.brand i{display:inline-grid;place-items:center;background:#167653;color:white;border-radius:13px;width:40px;height:40px;font-style:normal;margin-left:8px}.nav{display:grid;gap:8px}.nav a{color:var(--muted);padding:13px;border-radius:12px;text-decoration:none}.nav a:first-child,.nav a:hover{background:#16765318;color:var(--green)}.note{margin-top:40px;background:linear-gradient(140deg,#167653,#0b523c);color:white;border-radius:16px;padding:18px;line-height:1.7}.main{padding:28px clamp(18px,4vw,48px)}.top{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px}.top h1{font-size:27px;margin:7px 0}.muted,small{color:var(--muted)}button{cursor:pointer}.toggle,.secondary{border:1px solid var(--line);background:var(--surface);color:var(--ink);padding:11px 14px;border-radius:11px}.welcome{border-radius:21px;padding:25px 30px;background:linear-gradient(110deg,#166c4c,#218960);color:white;display:flex;justify-content:space-between;align-items:center}.welcome h2{margin:0 0 8px}.welcome p{margin:0;color:#ddf2e5}.stats,.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:18px 0 25px}.stat,.panel{background:var(--surface);border:1px solid var(--line);border-radius:17px;padding:19px;box-shadow:var(--shadow)}.stat strong{display:block;font-size:25px;margin:13px 0 5px}.heading{display:flex;justify-content:space-between;align-items:center;margin:24px 0 12px}.heading h2{font-size:19px;margin:0}.cards{grid-template-columns:1fr 1fr;margin:0}.money{height:175px;border-radius:18px;color:white;padding:21px 24px;position:relative;overflow:hidden;background:linear-gradient(130deg,#182f47,#247c70)}.money.token{background:linear-gradient(130deg,#725023,#daa94a)}.money:after{content:'';position:absolute;width:180px;height:180px;left:-35px;bottom:-120px;border:1px solid #ffffff55;border-radius:50%;box-shadow:0 0 0 22px #ffffff10}.money h3{margin:9px 0}.amount{font-size:29px;font-weight:bold}.symbol{position:absolute;left:22px;top:18px;font-size:34px}.lower{display:grid;grid-template-columns:1.2fr .8fr;gap:14px;margin-top:17px}.panel h3{margin-top:0}.form{display:grid;grid-template-columns:1fr 1fr;gap:9px}.form input,.form select{min-width:0;padding:12px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink)}.wide{grid-column:span 2}.primary{border:0;background:var(--green);color:white;padding:11px 16px;border-radius:10px}.result{color:var(--green);font-size:13px;margin-top:10px;min-height:18px}.row{display:flex;justify-content:space-between;border-bottom:1px solid var(--line);padding:9px 0;font-size:13px}.row:last-child{border:0}.row small{display:block;margin-top:4px}.footer{text-align:center;color:var(--muted);font-size:11px;padding:24px}@media(max-width:850px){.layout{grid-template-columns:1fr}.side{padding:12px 18px;border-left:0;border-bottom:1px solid var(--line)}.brand{margin:0}.nav,.note{display:none}.lower{grid-template-columns:1fr}}@media(max-width:560px){.stats{grid-template-columns:1fr}.cards{grid-template-columns:1fr}.welcome{display:block}.welcome small{display:block;margin-top:15px}.form{grid-template-columns:1fr}.wide{grid-column:auto}.top h1{font-size:22px}}
</style></head><body><div class="layout"><aside class="side"><div class="brand"><i>ن</i>نَقد</div><nav class="nav"><a href="#">◫　نظرة عامة</a><a href="#packages">▤　رزم المال</a><a href="#ops">↔　العمليات</a><a href="#activity">◷　سجل النشاط</a></nav><div class="note"><b>أموالك في أمان</b><br>تابع رصيدك وحركات حسابك من مكان واحد.</div></aside><main class="main"><header class="top"><div><small>لوحة التحكم / نظرة عامة</small><h1>أهلاً بيك 👋</h1></div><button class="toggle" id="theme">☾　الوضع الداكن</button></header><section class="welcome"><div><h2>إدارة مالية أسهل، كل يوم</h2><p>تفاصيل حسابك ورزمك المالية في واجهة واحدة.</p></div><small id="today" style="color:#d1eadb"></small></section><section class="stats"><article class="stat"><span class="muted">إجمالي الأرصدة</span><strong id="total">—</strong><small>مجموع أرصدة العملاء</small></article><article class="stat"><span class="muted">عدد العملاء</span><strong id="customers">—</strong><small>حسابات نشطة</small></article><article class="stat"><span class="muted">العمليات المسجلة</span><strong id="opsCount">—</strong><small>إيداع وسحب وتحويل</small></article></section><div class="heading" id="packages"><h2>رزمك المالية</h2><small>عرض توضيحي للأرصدة والرموز</small></div><section class="cards"><article class="money"><span class="symbol">💵</span><small>رزمة نقدية</small><h3>دولار أمريكي</h3><div class="amount">$100</div><small style="color:#e1eee8">ورقة نقدية من فئة 100 دولار</small></article><article class="money token"><span class="symbol">🪙</span><small>أصول رقمية</small><h3>رزمة Money Token</h3><div class="amount">MT × 100</div><small style="color:#fff4d9">رموز تجريبية للعرض داخل الواجهة</small></article></section><div class="lower"><section class="panel" id="ops"><h3>عملية سريعة</h3><form class="form" id="form"><select id="action"><option value="balance">عرض الرصيد</option><option value="deposit">إيداع</option><option value="withdraw">سحب</option><option value="transfer">تحويل</option><option value="add">إضافة عميل</option></select><input id="customer" placeholder="رقم العميل" required><input id="amount" type="number" min="0.01" step="0.01" placeholder="المبلغ"><input id="receiver" placeholder="رقم المستلم (للتحويل)"><button class="primary wide">تنفيذ العملية</button></form><div id="result" class="result"></div></section><section class="panel" id="activity"><h3>آخر العمليات</h3><div id="transactions" class="muted">لا توجد عمليات حتى الآن</div></section></div><div class="footer">نَقد — لوحة مالية تجريبية</div></main></div>
<script>
const fmt=n=>new Intl.NumberFormat('en-US',{minimumFractionDigits:2,maximumFractionDigits:2}).format(n);document.getElementById('today').textContent=new Intl.DateTimeFormat('ar-EG',{weekday:'long',year:'numeric',month:'long',day:'numeric'}).format(new Date());let theme=localStorage.getItem('naqed-theme')||'light';document.documentElement.dataset.theme=theme;const tb=document.getElementById('theme');function label(){tb.textContent=theme==='dark'?'☀　الوضع الفاتح':'☾　الوضع الداكن'}label();tb.onclick=()=>{theme=theme==='dark'?'light':'dark';document.documentElement.dataset.theme=theme;localStorage.setItem('naqed-theme',theme);label()};async function load(){try{let d=await(await fetch('/api/summary')).json();document.getElementById('total').textContent=fmt(d.total_balance);document.getElementById('customers').textContent=d.total_customers;document.getElementById('opsCount').textContent=d.total_operations;let box=document.getElementById('transactions');box.innerHTML='';if(!d.transactions.length){box.textContent='لا توجد عمليات حتى الآن';return}d.transactions.slice(-5).reverse().forEach(t=>{let row=document.createElement('div');row.className='row';let names={deposit:'إيداع',withdraw:'سحب',transfer_out:'تحويل صادر',transfer_in:'تحويل وارد'};row.innerHTML=`<span>${names[t.type]||t.type}<small>العميل ${t.customer_id}</small></span><b>${t.type.includes('out')||t.type==='withdraw'?'-':'+'}${fmt(t.amount)}</b>`;box.appendChild(row)})}catch(e){document.getElementById('result').textContent='تعذر الاتصال بالخادم.'}}document.getElementById('form').onsubmit=async e=>{e.preventDefault();let data={action:action.value,customer_id:customer.value,amount:amount.value,receiver_id:receiver.value};let res=document.getElementById('result');try{let d=await(await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})).json();res.textContent=d.message;if(d.ok)load()}catch(e){res.textContent='تعذر تنفيذ العملية.'}};load();
</script></body></html>'''
class DashboardHandler(BaseHTTPRequestHandler):
    def reply(self,data,status=200,content_type='application/json; charset=utf-8'):
        body=data if isinstance(data,bytes) else json.dumps(data,ensure_ascii=False).encode('utf-8')
        self.send_response(status);self.send_header('Content-Type',content_type);self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
    def do_GET(self):
        if self.path=='/api/summary':
            stat=my_bank.calculate_number_customer()
            if not isinstance(stat,dict): stat={'total_balance':0,'total_customers':0}
            self.reply({**stat,'total_operations':len(my_bank.transactions),'transactions':my_bank.transactions[-20:]})
        elif self.path in ('/','/index.html'): self.reply(PAGE.encode('utf-8'),content_type='text/html; charset=utf-8')
        else: self.reply({'message':'Not found'},404)
    def do_POST(self):
        if self.path!='/api/action': self.reply({'ok':False,'message':'المسار غير موجود.'},404);return
        try: data=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))) or b'{}')
        except (ValueError,json.JSONDecodeError): self.reply({'ok':False,'message':'البيانات غير صالحة.'},400);return
        action=data.get('action');cid=str(data.get('customer_id','')).strip();amount=data.get('amount','');ok=False
        if action=='balance':
            value=my_bank.show_balance(cid);message=f'الرصيد الحالي: {value:.2f}' if isinstance(value,(int,float)) else value;ok=isinstance(value,(int,float))
        elif action=='deposit': message=my_bank.deposit_money(cid,amount);ok=message=='Deposit successful.'
        elif action=='withdraw': message=my_bank.withdraw_money(cid,amount);ok=message=='Withdraw successful.'
        elif action=='transfer': message=my_bank.transfer_money(cid,str(data.get('receiver_id','')).strip(),amount);ok=message=='Transfer successful.'
        elif action=='add': message=my_bank.add_customer(cid,amount or 0);ok=message=='Customer added successfully.'
        else: self.reply({'ok':False,'message':'اختار عملية صحيحة.'},400);return
        self.reply({'ok':ok,'message':message})
    def log_message(self,format,*args): print('[web] '+format%args)
if __name__=='__main__':
    server=ThreadingHTTPServer(('127.0.0.1',8000),DashboardHandler)
    print('Bank dashboard: http://127.0.0.1:8000 | Ctrl+C to stop')
    try: server.serve_forever()
    except KeyboardInterrupt: print('\nServer stopped.')
    finally: server.server_close()
