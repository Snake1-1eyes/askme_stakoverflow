def paginator_processor(request):
    paginator_paths = {'/', '/index/', '/question/', '/tag/'}
    is_paginate = False
    if request.get_full_path() in paginator_paths:
        is_paginate = True
    return {'is_paginate': is_paginate}