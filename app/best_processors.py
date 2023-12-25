from .models import Profile
def best_processor(request):
    profiles = Profile.objects.all()[:5]

    # Получаем имена пользователей
    user_names = [{'name': profile.user.username} for profile in profiles]

    return {'user_names': user_names}

