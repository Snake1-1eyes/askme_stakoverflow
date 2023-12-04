from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Question, Answer, Tag, Profile, Rating
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
    p_page = paginator.get_page(page)
    return [p_page, paginator.get_elided_page_range(number=p_page.number,
                                                    on_each_side=2,
                                                    on_ends=1)]

'''def paginate(objects, page, per_page=10):
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
'''

def index(request):
    #page = int(request.GET.get('page', 1))
    #return render(request, 'index.html', {'questions': paginate(QUESTION, page)})
    page, page_range = paginate(Question.objects.new_questions(), request.GET.get('page', 1))
    return render(request, "index.html", {'items': page, 'page_range': page_range})


def tag(request, tag_id):
    #page = int(request.GET.get('page', 1))
    #return render(request, 'tag.html', {'questions': paginate(QUESTION, page)})
    tag_item = get_object_or_404(Tag.objects.all(), id=tag_id)
    page, page_range = paginate(Question.objects.tag_questions(tag_id), request.GET.get('page', 1))
    return render(request, "tag.html", {'items': page, 'page_range': page_range, 'tag': tag_item})


def question(request, question_id):
    '''answers = [
        {
            'id': i,
            'title': f'Answer {i + 1}',
            'content': f'long lorem ipsum {i + 1}'
        } for i in range(10)
    ]
    item = QUESTION[question_id]
    return render(request, 'question.html', {'question': item, 'answers': answers})'''
    item = get_object_or_404(Question.objects.all(), id=question_id)
    page, page_range = paginate(Answer.objects.right_question_answers(item.id), request.GET.get('page', 1))
    return render(request, "question.html", {'question': item, 'items': page, 'page_range': page_range})

def setting(request):
    return render(request, 'setting.html')


def ask(request):
    return render(request, 'ask.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')
