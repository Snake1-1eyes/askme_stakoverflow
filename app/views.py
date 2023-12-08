from django.contrib import auth, messages
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from .models import Question, Answer, Tag, Profile, Rating
from django.core.paginator import Paginator
from .forms import LoginForm, RegisterForm, EditProfileForm, NewQuestionForm, NewAnswerForm


def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    p_page = paginator.get_page(page)
    return [p_page, paginator.get_elided_page_range(number=p_page.number,
                                                    on_each_side=2,
                                                    on_ends=1)]


def anonymous_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def index(request):
    page, page_range = paginate(Question.objects.new_questions(), request.GET.get('page', 1))
    return render(request, "index.html", {'items': page, 'page_range': page_range})


def tag(request, tag_id):
    tag_item = get_object_or_404(Tag.objects.all(), id=tag_id)
    page, page_range = paginate(Question.objects.tag_questions(tag_id), request.GET.get('page', 1))
    return render(request, "tag.html", {'items': page, 'page_range': page_range, 'tag': tag_item})


def question(request, question_id):
    item = get_object_or_404(Question.objects.all(), id=question_id)
    user = request.user

    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
        belonging = True if item.author == profile else False
    else:
        belonging = False

    if request.method == 'GET':
        new_answer_form = NewAnswerForm()
    if request.method == 'POST':
        new_answer_form = NewAnswerForm(request.POST)
        if new_answer_form.is_valid():
            new_answer_form.save(request, question_id)
            anchor_answer = Answer.objects.last_right_question_answers(item.id)
            anchor = 'question' if anchor_answer is None else str(anchor_answer.id)
            return redirect(reverse('question', args=[question_id]) + '#' + anchor)

    page, page_range = paginate(Answer.objects.right_question_answers(item.id), request.GET.get('page', 1))
    return render(request, "question.html",
                  {'question': item, 'belonging': belonging, 'items': page,
                   'page_range': page_range, 'form': new_answer_form})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def setting(request):
    if request.method == 'GET':
        edit_profile_form = EditProfileForm(instance=request.user)
    if request.method == 'POST':
        edit_profile_form = EditProfileForm(request.POST, instance=request.user)
        if edit_profile_form.is_valid():
            user = edit_profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
    return render(request, 'setting.html', {'form': edit_profile_form})


@login_required(login_url='login', redirect_field_name='continue')
def ask(request):
    if request.method == 'GET':
        new_question_form = NewQuestionForm()
    if request.method == 'POST':
        new_question_form = NewQuestionForm(request.POST)
        if new_question_form.is_valid():
            new_question = new_question_form.save(request)
            return redirect(reverse('question', args=[new_question.id]))
    return render(request, 'ask.html', {'form': new_question_form})


# reverse('index')
@csrf_protect
def login(request):
    print(request.GET)
    print(request.POST)
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, 'Wrong password or user does not exist.')
                login_form.add_error('username', '')
                login_form.add_error('password', '')
    return render(request, 'login.html', context={'form': login_form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@csrf_protect
@anonymous_required(login_url='index', redirect_field_name='continue')
def signup(request):
    if request.method == 'GET':
        register_form = RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            try:
                user = register_form.save()
                auth.login(request, user)
                return redirect(request.GET.get('continue', '/'))
            except IntegrityError:
                register_form.add_error(None, 'This User already exists!')
    return render(request, 'signup.html', {'form': register_form})
