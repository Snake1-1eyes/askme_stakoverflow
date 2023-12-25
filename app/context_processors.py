from .models import Tag


def request_processor(request):
    tags = Tag.objects.top_tags()

    # Получаем имена пользователей
    tag_names = [{'tag_id': tag['id'], 'tag_name': tag['tag_name']} for tag in tags]

    return {'tag_names': tag_names}
