from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import logupForm, loginForm

def aboutProject(request):
    return render(request, 'aboutProject.html')
def aboutUs(request):
    return render(request, 'aboutUs.html')
def faq(request):
    return render(request, 'faq.html')
def home(request):
    return render(request, 'home.html')
def login(request):
    out = ''
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            import sqlite3
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            con = sqlite3.connect('hackathonSQLite.db')
            cur = con.cursor()
            cur.execute(f'''SELECT id, password from login WHERE name = "{name}" ''')
            passwordTrue = cur.fetchall()
            id = passwordTrue[0][0]
            if passwordTrue == []:
                return HttpResponseRedirect('http://127.0.0.1:8000/logup/')
            if passwordTrue[0][1] == password:
                outt = HttpResponseRedirect('/')
                outt.set_cookie("id", id, max_age=7*24*60*60)
                return outt
            else:
                out = 'Неверный пароль'
    else:
        form = loginForm()
    return render(request, 'login.html', {'form': form, 'out': out})
def logup(request):
    def checkString(x):
        s = 'abcdefghijklmnopqrstuvwxyz_1234567890'
        x = x.lower()
        t = True
        for i in x:
            if not(i in s):
                t = False
        return t
    def checkName(cur):
        cur.execute(f'''SELECT name from login WHERE name = "{name}" ''')
        if cur.fetchall() == []:
            if checkString(name):
                return [True, '']
            else:
                return [False, 'Логин может состоять из латиницы, чисел или нижнего подчёркивания ']
        else:
            return [False, 'Логин уже занят']
    out = ''
    if request.method == 'POST':
        form = logupForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            password1 = form.cleaned_data['password1']
            if len(password) >= 8 and password1 == password:
                import sqlite3
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                email = email.replace('@', '|')
                con = sqlite3.connect('hackathonSQLite.db')
                cur = con.cursor()
                checkName = checkName(cur)
                if checkName[0]:
                    cur.execute(f'''SELECT name from login;''')
                    cur.execute(f"""INSERT INTO login VALUES(?, ?, ?, ?, ?);""", (len(cur.fetchall()), name, password, email))
                    con.commit()
                else:
                    out = checkName[1]
            else:
                if password1 != password:
                    out = 'Пароли не совпадают'
                else:
                    out = 'Пароль должен быть длинее 8 символов'
    else:
        form = logupForm()
    return render(request, 'logup.html', {'form': form, 'out': out})