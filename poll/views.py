from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, CommentForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .models import Document, ControlVote, Category, Comment
from .forms import ChangeForm
from django.http import HttpResponse, Http404


def homeView(request):
    return render(request, "poll/home.html")


def registrationView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['confirm_password']:
                obj = form.save(commit=False)
                obj.set_password(obj.password)
                obj.save()
                messages.success(request, 'You have been registered.')
                return redirect('home')
            else:
                return render(request, "poll/registration.html", {'form': form, 'note': 'password must match'})
    else:
        form = RegistrationForm()

    return render(request, "poll/registration.html", {'form': form})


def loginView(request):
    if request.method == "POST":
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.success(request, 'Invalid username or password!')
            return render(request, "poll/login.html")
    else:
        return render(request, "poll/login.html")


@login_required
def logoutView(request):
    logout(request)
    return redirect('home')


@login_required
def dashboardView(request):
    return render(request, "poll/dashboard.html")


@login_required
def categoryView(request):
    obj = Category.objects.all()
    return render(request, "poll/category.html", {'obj': obj})


@login_required
def documentView(request, pos):
    obj = get_object_or_404(Category, pk=pos)
    if request.method == "POST":

        temp = ControlVote.objects.get_or_create(
            user=request.user, category=obj)[0]

        if temp.status == False:
            temp2 = Document.objects.get(pk=request.POST.get(obj.title))
            temp2.total_vote += 1
            temp2.save()
            temp.status = True
            temp.save()
            return HttpResponseRedirect('/category/')
        else:
            messages.success(
                request, 'you have already been voted this category.')
            return render(request, 'poll/document.html', {'obj': obj})
    else:
        return render(request, 'poll/document.html', {'obj': obj})


@login_required
def resultView(request):
    obj = Document.objects.all().order_by('category', '-total_vote')
    return render(request, "poll/result.html", {'obj': obj})


@login_required
# def documentDetailView(request, id):
#    obj = get_object_or_404(Document, pk=id)
#    return render(request, "poll/document_detail.html", {'obj': obj})
def documentDetailView(request, id):
    try:
        data = Document.objects.get(pk=id)
        comments = Comment.objects.filter(document=data)
    except Document.DoesNotExist:
        raise Http404('Data does not exist')

    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(user=form.cleaned_data.get('user'),
                                             body=form.cleaned_data['body'],
                                             document=data)
            comment.save()
            return redirect(f'/document/detail/{id}')
    else:
        form = CommentForm()

    context = {
        'data': data,
        'comment_form': form,
        'comments': comments,
    }
    return render(request, 'poll/document_detail.html', context)


@login_required
def changePasswordView(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "poll/password.html", {'form': form})


@login_required
def editProfileView(request):
    if request.method == "POST":
        form = ChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ChangeForm(instance=request.user)
    return render(request, "poll/edit_profile.html", {'form': form})
