from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import calendar
import datetime
now = datetime.datetime.now()

from .forms import LessonForm, SignUpForm, UserProfileForm
from .models import Lesson, Notification, Profile

@login_required(login_url='/login_user/')
def home(request):
    if request.user.is_authenticated:
        lesson_list = Lesson.objects.all().order_by('-date_created')
        lessons = []
        for lesson in lesson_list:
            date = datetime.datetime(now.year, now.month, now.day)
            start_date = datetime.datetime(lesson.start_date.year, lesson.start_date.month, lesson.start_date.day)
            end_date = datetime.datetime(lesson.end_date.year, lesson.end_date.month, lesson.end_date.day)
            if start_date <= date <= end_date:
                lessons.append(lesson)
                # if request.user.profile.contract_type == '下請け':
                #     for genba in lessons:
                #         if genba.head_person != request.user.profile or request.user.profile not in lesson.attendees.all():
                #             lessons.remove(lesson)
        if request.method == "POST":
            content = request.POST.get("content")
            author = User.objects.get(id=request.user.id)
            notification = Notification.objects.create(content=content, author=author)
            notification.save()
        notifications = Notification.objects.all().order_by('-date_created')
        return render(request, "home.html", {"lesson_list":lesson_list, "lessons": lessons, "notifications": notifications})
    else:
        messages.success(request, "请先登录。")
        return redirect("login_user")

def schedule(request):
    if request.user.is_authenticated:
        lesson_list = Lesson.objects.all().order_by('-date_created')
        lessons_today = []
        for lesson in lesson_list:
            date = datetime.datetime(now.year, now.month, now.day)
            start_date = datetime.datetime(lesson.start_date.year, lesson.start_date.month, lesson.start_date.day)
            end_date = datetime.datetime(lesson.end_date.year, lesson.end_date.month, lesson.end_date.day)
            if start_date <= date <= end_date:
                lessons_today.append(lesson)
                # if request.user.profile.contract_type == '下請け':
                #     for lesson in lessons_today:
                #         if lesson.head_person != request.user.profile or request.user.profile not in lesson.attendees.all():
                #             lessons_today.remove(lesson)
    year = int(now.year)
    month = int(now.month)
    cal = calendar.HTMLCalendar().formatmonth(year, month)
    cal = cal.replace('<td ', '<td width="150" height="150" hover')
    cal = mark_safe(cal)
    if request.user.is_authenticated:
         context = {
            "lesson_list": lesson_list,
            "lessons_today":lessons_today,
            "year": year,
            "month": month,
            "cal": cal,
        }
         return render(request, "schedule.html", context=context)
    else:
        return redirect('login_user')
    
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.profile:
                messages.success(request, (f"{user.profile}， 欢迎回来。"))
            else:
                messages.success(request, ("欢迎回来。"))
            return redirect("home")
        else:
            messages.success(request, ("账号或者是密码错误。请再试一次。"))
            return redirect("login_user")
    else:
        return render(request, "authentication/login.html", {}) 
    
@login_required(login_url='/login_user/')
def logout_user(request):
    logout(request)
    messages.success(request, ("已退出。下次再见。"))
    return redirect("login_user")