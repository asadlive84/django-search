import datetime

from django.shortcuts import render, redirect
from .forms import NewUserForm, SearchForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

from .models import SearchHistory, CustomUser
from .utils import email_check, search_history_info_saved, date_convert_to_str


def homepage(request):
    search_info = None
    homepage = True
    search = None
    user = request.user if request.user.is_authenticated else None
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')

            search_history_info_saved(search, user)

            search_info = SearchHistory.objects.filter(search_keyword__icontains=search)

            if search_info.count() < 1:
                search_info = None
    else:
        form = SearchForm()

    context = {
        "form": form,
        "search": search,
        "search_info": search_info,
        "homepage": homepage,
    }
    return render(request=request, template_name="main/home.html", context=context)


def register_request(request):
    tmp = False
    form = False
    exists_mail = False
    if request.user.is_authenticated:
        return redirect('main:homepage')
    else:
        tmp = "main/register.html"
        if request.method == "POST":
            form = NewUserForm(request.POST)
            emailCheck = email_check(request.POST["email"])
            exists_mail = True if emailCheck else False
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return redirect("main:homepage")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = NewUserForm()
    return render(request=request, template_name=tmp, context={"register_form": form, "exists_mail": exists_mail})


def login_request(request):
    if request.user.is_authenticated:
        return redirect('main:homepage')
    else:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                print("form is valid")
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect("main:homepage")
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:homepage")


def results(request):
    search_user = None
    keyword = None
    is_searched = None
    results = SearchHistory.objects.all()
    user = CustomUser.objects.all()
    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    search_keyword = request.POST.get('keyword')
    userlist = request.POST.getlist('users')
    if request.method == "POST":
        is_searched = True
        if search_keyword is not None or len(search_keyword) > 0:
            results = results.filter(search_keyword__icontains=search_keyword)
            keyword = search_keyword
        if userlist is not None:
            if userlist[0] != 'None':
                results = results.filter(user__in=userlist)
                search_user = CustomUser.objects.get(id=userlist[0]).email

        if from_date is not None:
            start_date = date_convert_to_str(from_date)
            if start_date is not None:
                results = results.filter(created_at__gte=start_date)

        if to_date is not None:
            end_date = date_convert_to_str(to_date)
            if end_date is not None:
                results = results.filter(created_at__lte=end_date)
    context = {
        "results": results.order_by('-updated_at', '-id'),
        "user": user,
        "from_date": from_date,
        "to_date": to_date,
        "is_searched": is_searched,
        "keyword": keyword,
        "search_user": search_user,
    }
    return render(request=request, template_name="main/results.html", context=context)
