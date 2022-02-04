from django.shortcuts import redirect, render

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Task
from .forms import TaskForm


def loginUser(request):

    if request.method == 'POST':
        ## lower kvůli registraci, kde se jméno dává do loweru
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        ## kontrola udaju s User tabulkou
        user = authenticate(request, username=username, password=password)

        ## když uživatel není prázdný, logneme ho
        if user is not None:
            login(request, user)
        else:
            messages.error(request, 'špatné jméno nebo heslo')

    data = {}
    try:
        return render(request, 'base/profile.html', data)
    except:
        return redirect('home')


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    users = User.objects.all()
    data = {'users': users}

    if request.method == 'POST':
        loginUser(request)

    return render(request, 'base/home.html', data)
    #return HttpResponse


## nelze prohlížet profily bez přihlášení
@login_required(login_url='home')
def userProfile(request, pk):
    
    ## aktuální stránka zkoumaného uživatele
    user = User.objects.get(id=pk)

    ## propojení uživatele s přidělenými úkoly
    tasks = Task.objects.filter(user=user)

    task_count = tasks.count()

    data = {'user': user, 'tasks': tasks, 'count': task_count}
    return render(request, 'base/profile.html', data)


def registerUser(request):
    ## django funkce s default formulářem pro vytvoření účtu
    form = UserCreationForm()

    if request.method == 'POST':
        ## request.POST = heslo, jmeno a vsechno ostatni
        form = UserCreationForm(request.POST)

        if form.is_valid():
            ## tímhle se "zmrazi v case" a data se muzou ocistit a upravit pro spravny parsovani
            user = form.save(commit=False)

            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'nastala chyba během registrace')
            
    
    return render(request, 'base/register.html', {'form': form})


@login_required(login_url='home')
def addTask(request, pk):
    
    ## stránka nějakého uživatele
    user = User.objects.get(id=pk)

    ## kontrola profilů -> nelze přidávat úkoly na cizí
    if checkUser(user, request.user):
        return render(request, 'base/error.html', {'user': user})

    ## vytvořený formulář z forms.py, kontrola aby se přiřadilo user.id
    form = TaskForm()

    if request.method == 'POST':

        form = TaskForm(request.POST)

        if form.is_valid():
            
            ## zmrazení formu, aby se neukládal
            task = form.save(commit=False)

            ## doplnění ID do formu, uživateli se automaticky přidá a nemusí ho řešit skrz formulář
            task.user_id = user.id
            task.save()

            ## vrať se na profil uživatele
            return userProfile(request, user.id)

        else:
            print("nastala chyba ve vytvareni formu")

    data = {'form': form}
    return render(request, 'base/task_add.html', data)


@login_required(login_url='home')
def updateTask(request, pk):

    user = request.user
    task = Task.objects.get(id=pk)

    ## kontrola profilů -> nelze upravovat cizí úkoly
    if checkUser(task.user, request.user):
        return render(request, 'base/error.html', {'user': task.user})
    
    ## instance je k předvyplnění atributů
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task = form.save()

            ## vrať se na profil uživatele
            return userProfile(request, user.id)

        else:
            print("nastala chyba ve vytvareni formulare")

    data = {'task': task, 'user': user, 'form': form}
    return render(request, 'base/task_update.html', data)


@login_required(login_url='home')
def removeTask(request, pk):
    task = Task.objects.get(id=pk)
    user = request.user

    if checkUser(task.user, request.user):
        return render(request, 'base/error.html', {'user': task.user})

    if request.method == 'POST':
        task.delete()
        return userProfile(request, user.id)

    return render(request, 'base/task_remove.html', {'obj': task})


## pokud stránka uživatele není přihlášeného uživatele, systém nepustí dál
def checkUser(userPage, userLogged):
    if userPage != userLogged:
        return True