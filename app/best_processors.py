def best_processor(request):
    paths = {'/', '/index/'}#, '/question/', '/login/', '/tag/', '/signup/', '/index/'}
    members = [
        {
            'text': f'Member {i + 1}',
            'raiting': 10-i,
        } for i in range(5)
    ]
    return {'members': members}