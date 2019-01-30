from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render, redirect
from .form import UserLoginForm, UserCreateForm
from .models import User
import datetime


def make_account(request):
    page_name = "アカウント作成ページ"
    now = datetime.datetime.now()  # mycalendarは日付がurlについていないとダメなので、それ用。

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_check = request.POST['password_check']

        form = UserLoginForm(request.POST) #login用のモデルインスタンスを保存するので、LoginFormと比較＆保存する。CreateFormと比較すると、password_checkが足りない.

        if form.is_valid() and password == password_check:
            user = form.save()
            login(request, user)
            return redirect('/mycalendar/' + now.strftime('%Y') + '/' + now.strftime('%m') + '/' + now.strftime('%d') + '/')
        else:
            warning_text = '適切な値を入力してください'
            form = UserCreateForm()
            context = {'page_name': page_name,'warning_text':warning_text,'form':form }

    else:
        form = UserCreateForm()
        context = {'page_name': page_name,'form':form }

    return render(request, 'login/make_account.html', context)


def login_member(request):
    page_name = "ログインページ"
    now = datetime.datetime.now() #mycalendarは日付がurlについていないとダメなので、それ用。

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user_isActive = False
        user = authenticate(username=username,password=password)
        if user != 'None':
            user_isActive = True
        user_name = User.objects.filter(username=username)
        
        for item in user_name:
            print(item)
            if item.password == password: #マッチしたユーザの中でパスワードが一致したもののみを取り出す作業。
                user = item
                user_isActive = True

        if user_isActive: #管理者の場合は、パスワードが暗号化されているのでuser.is_activeで通る
            login(request, user)
            return redirect('/mycalendar/' + now.strftime('%Y') + '/' + now.strftime('%m') + '/' + now.strftime('%d') + '/')
        else:
            print("ログイン失敗")
            warning_text = '適切な値を入力してください'
            form = AuthenticationForm()
            context = {'page_name': page_name,'warning_text':warning_text,'form':form }

    else:
        form = AuthenticationForm()
        context = {'page_name': page_name,'form':form }

    return render(request, 'login/login.html', context)

def logout_member(request):
    logout(request)
    return redirect('/')
