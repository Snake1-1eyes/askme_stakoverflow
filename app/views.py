from django.shortcuts import render
from django.core.paginator import Paginator


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
    return paginator.page(page)


def index(request):
    page = int(request.GET.get('page', 1))
    return render(request, 'index.html', {'questions': paginate(QUESTION, page)})


def question(request, question_id):
    item = QUESTION[question_id]
    return render(request, 'question.html', {'question': item})
