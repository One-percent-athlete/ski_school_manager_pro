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

def lesson_list(request):
    if request.user.is_authenticated:
        lesson_list = Lesson.objects.all().order_by('-date_created')
        lessons_today = []
        result_list = []
        keyword = ''
        for lesson in lesson_list:
            date = datetime.datetime(now.year, now.month, now.day)
            start_date = datetime.datetime(lesson.start_date.year, lesson.start_date.month, lesson.start_date.day)
            end_date = datetime.datetime(lesson.end_date.year, lesson.end_date.month, lesson.end_date.day)
            if start_date <= date <= end_date:
                lessons_today.append(lesson)
        if request.method == "POST":
            keyword = request.POST['keyword']
            result_list = Lesson.objects.filter(id=keyword).order_by('-date_created')
        year = int(now.year)
        month = int(now.month)
        cal = calendar.HTMLCalendar().formatmonth(year, month)
        cal = cal.replace('<td ', '<td width="150" height="150" hover')
        cal = mark_safe(cal)
        context = {
            "lesson_list": lesson_list,
            "lessons_today":lessons_today,
            "result_list": result_list,
            "keyword": keyword,
            "year": year,
            "month": month,
            "cal": cal,
        }
        return render(request, "lesson/lesson_list.html", context=context)
    else:
        return redirect('login_user')
    
@login_required(login_url='/login_user/')
def delete_notification(request, notification_id):
    if request.user.is_authenticated:
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
        messages.success(request, "連絡事項已被。")
        return redirect("home")
    else:
        messages.success(request, "请先登录。")
        return redirect("login_user")
    
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.profile:
                messages.success(request, (f"{user.profile}, 欢迎回来。"))
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

@login_required(login_url='/login_user/')
def register_user(request):
    if request.user.is_superuser:
        form = SignUpForm()
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(username=username, password=password)
                messages.success(request, ("请输入简历。"))
                return redirect("update_profile", user.pk)
            else:
                messages.success(request, ("请再试一次。"))
                return redirect("register_user")
        else:
            return render(request, "authentication/register_user.html", {
                "form": form
            })
    else:
        messages.success(request, ("只有管理人员可以访问此页面。"))
        return redirect("login_user")
    
@login_required(login_url='/login_user/')
def delete_user(request, user_id):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=user_id)
        current_user.delete()
        messages.success(request, "简历消除了。")
        return redirect("profile_list")
    else:
        messages.success(request, "请先登录。")
        return redirect("home")
    
@login_required(login_url='/login_user/')
def profile_list(request):
    if request.user.is_authenticated:

        result_list = []
        keyword = ''
        if request.method == "POST":
            keyword = request.POST['keyword']
            result_list = Profile.objects.filter(id=keyword).order_by('-date_created')
        profiles = Profile.objects.all().order_by('-date_created')
        contract = request.user.profile.contract_type
        return render(request, "profile/profile_list.html", { "profiles": profiles, "contract": contract })
    else:
        return redirect('login_user')

@login_required(login_url='/login_user/')
def update_profile(request, profile_id):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            profile = Profile.objects.get(id=profile_id)
            form = UserProfileForm(request.POST or None, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "简历更新了。")
                return redirect("profile_list")
            return render(request, "profile/update_profile.html", {"form": form , "profile": profile })
        else:
            messages.success(request, "请先登录。")
            return redirect("login_user")
    else:
        messages.success(request, ("只有管理人员可以访问此页面。"))

# @login_required(login_url='/login_user/')
# def lesson_list(request):   
#     if request.user.is_authenticated:
#         lesson_list = Lesson.objects.all().order_by('-date_created')
#         lessons = []
#         if request.method == "POST":
#             keyword = request.POST['keyword']
#             result_list = Lesson.objects.filter(name__contains=keyword).order_by('-date_created')
#             return render(request, "lesson/lesson_search_list.html", {"result_list": result_list, "keyword": keyword})
#             # # if request.user.profile.contract_type == '下請け':
#             # #     for lesson in lesson_list:
#             # #         if lesson.head_person == request.user.profile or request.user.profile in lesson.attendees.all():
#             # #             lesson.append(lesson)
#             # else:
#                 # lessons = lesson_list
#     return render(request, "lesson/lesson_list.html", {"lessons": lessons})

@login_required(login_url='/login_user/')
def lesson_details(request, lesson_id):
    if request.user.is_authenticated:
        lesson = Lesson.objects.get(id=lesson_id)
        form = LessonForm(request.POST or None, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "课程更新了。")
            return redirect("lesson_list")
        return render(request, "lesson/lesson_details.html", {"form": form , "lesson": lesson })
    else:
        messages.success(request, "请先登录。")
        return redirect("login_user")

@login_required(login_url='/login_user/')
def add_lesson(request):
    form = LessonForm()
    if request.method == "POST":
        form = LessonForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("课程排好了。"))
            return redirect("lesson_list")
        else:
            messages.success(request, ("请再试一次。"))
            return redirect("lesson_list")
    else:
        return render(request, "lesson/add_lesson.html", {
            "form": form
        })
    
@login_required(login_url='/login_user/')
def delete_lesson(request, lesson_id):
    if request.user.is_authenticated:
        current_lesson = Lesson.objects.get(id=lesson_id)
        current_lesson.delete()
        messages.success(request, "课程已被消除。")
        return redirect("lesson_list")
    else:
        messages.success(request, "请先登录。")
        return redirect("login_user")
    
@login_required(login_url='/login_user/')
def profile_lesson(request):   
    if request.user.is_authenticated:
        profiles = Profile.objects.all()
        lessons = Lesson.objects.all().order_by('-date_created')
    return render(request, "lesson/profile_lesson.html", {"profiles": profiles, "lessons": lessons})

@login_required(login_url='/login_user/')
def commission(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            keyword = request.POST['keyword']
            profiles = Profile.objects.filter(fullname__contains=keyword).order_by('-date_created')
            return render(request, "commission.html", {"profiles": profiles, "keyword": keyword})
        else:
            profiles = Profile.objects.all()
            lessons = Lesson.objects.all()
            return render(request, "commission.html", { "profiles": profiles, "lessons": lessons })
    else:
        messages.success(request, "请先登录。")
        return redirect("login_user")
    