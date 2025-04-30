from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('schedule/', views.schedule, name='schedule'),

    path('register_user/', views.register_user, name="register_user"),
    path('login_user/', views.login_user, name="login_user"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('delete_user/<int:user_id>/', views.delete_user, name="delete_user"),

    path('profile_list/', views.profile_list, name="profile_list"),
    path('update_profile/<int:profile_id>/', views.update_profile, name="update_profile"),

    path('lesson_list/', views.lesson_list, name="lesson_list"),
    path('add_lesson/', views.add_lesson, name="add_lesson"),
    path('delete_lesson/<int:lesson_id>/', views.delete_lesson, name="delete_lesson"),
    path('lesson_details/<int:lesson_id>/', views.lesson_details, name="lesson_details"),

    path('profile_lesson/', views.profile_lesson, name="profile_lesson"),

    path('commission/', views.commission, name="commission"),
    # path('commission/<int:profile_id>/', views.commission, name="commission_profile"),
]
