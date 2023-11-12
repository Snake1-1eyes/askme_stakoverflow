def sections_processor(request):
    authorised_paths = {'/', '/question/', '/login/', '/tag/', '/signup/'}
    is_authorized = False
    if request.get_full_path() in authorised_paths:
        is_authorized = True
    return {'is_authorized': is_authorized}

