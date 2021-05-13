import requests

django_url = 'http://127.0.0.1:8000/bot_handler/'


def create_request(word):
    print(f'Trying to connect to {django_url}')
    print(f'Creating Session')
    with requests.Session() as session:
        print(f'Getting Session with {django_url}')
        response = session.get(django_url)
        print(f'Server Response: {response.content}')

        csrf = session.cookies['csrftoken']
        print(f'CSRF: {csrf}')
        headers = {'X-CSRFToken': csrf}
        data = {'word': word}

        try:
            response = session.post(django_url, json=data, headers=headers)
            print(f'Server Response: {response }')
        except Exception as e:
            print(f'Error: {e}')
            return False
        else:
            return True
