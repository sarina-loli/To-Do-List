from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth import login

from django.contrib.auth.decorators import login_required

from .models import Task
from .models import Profile

from .forms import RegisterForm
from .forms import TaskForm
from .forms import ProfileForm


def home(request):
    return render(request,'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request,user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form': form})


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    incomplete_tasks = tasks.filter(completed=False).count()
    context = {'total_tasks': total_tasks,'completed_tasks': completed_tasks,'incomplete_tasks': incomplete_tasks}
    return render(request,'dashboard.html',context)


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    query = request.GET.get('q')
    if query:
        tasks = tasks.filter(title__icontains=query)
    return render(request,'task_list.html',{'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request,'task_form.html',{'form': form})


@login_required
def update_task(request, pk):
    task = get_object_or_404(Task,pk=pk,user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request,'task_update.html',{'form': form})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task,pk=pk,user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request,'task_delete.html',{'task': task})


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task,pk=pk,user=request.user)
    task.completed = True
    task.save()
    return redirect('task_list')


@login_required
def incomplete_task(request, pk):
    task = get_object_or_404(Task,pk=pk,user=request.user)
    task.completed = False
    task.save()
    return redirect('task_list')

@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request,'profile.html',{'form': form})
# Create your views here.
