from django.shortcuts import render
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)


# Create your views here.
QUESTION = [
        {
            'id': i,
            'title': f'Question {i+1}',
            'content': f'long lorem ipsum {i+1}'
        } for i in range(100)
    ]




def paginate(objects, page, per_page=10):
    paginator = Paginator(objects, per_page)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range,  deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def index(request):
    page = int(request.GET.get('page', 1))
    return render(request, 'index.html', {'questions': paginate(QUESTION, page)})


def tag(request):
    page = int(request.GET.get('page', 1))
    return render(request, 'tag.html', {'questions': paginate(QUESTION, page)})


def question(request, question_id):
    answers = [
        {
            'id': i,
            'title': f'Answer {i + 1}',
            'content': f'long lorem ipsum {i + 1}'
        } for i in range(10)
    ]
    item = QUESTION[question_id]
    return render(request, 'question.html', {'question': item, 'answers': answers})


def setting(request):
    return render(request, 'setting.html')


def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')
