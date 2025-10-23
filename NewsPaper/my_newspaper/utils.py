import random
from .models import Post

post_types = ['NW', 'AR']

authors_ids = [1, 2, 3, 4, 5, 6, 7]

def gen_post():
    for i in range(4, 51):
        kwargs = {
            'author_id': random.choice(authors_ids),
            'post_types': random.choice(post_types),
            'title': f"Заголовок поста {i}",
            'text_post': f"Содержание поста {i}"
        }
        Post.objects.create(**kwargs)
    print('Все посты успешно добавлены')

def create_or_edit(context, request_path):
    if "create" in request_path:
        title = 'Добавление'
    elif "edit" in request_path:
        title = 'Редактирование'
    else:
        title = 'Удаление'

    if 'news' in request_path:
        title += ' новости'
    else:
        title += ' статьи'

    context['create_or_edit'] = title
    return context