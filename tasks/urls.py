from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('tasks/',views.task_list,name='task_list'),
    path('tasks/create/',views.create_task,name='create_task'),
    path('tasks/update/<int:pk>/',views.update_task,name='update_task'),
    path('tasks/delete/<int:pk>/',views.delete_task,name='delete_task'),
    path('tasks/complete/<int:pk>/',views.complete_task,name='complete_task'),
    path('tasks/incomplete/<int:pk>/',views.incomplete_task,name='incomplete_task'),
    path('profile/',views.profile,name='profile'),
]