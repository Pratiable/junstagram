import jwt

from django.core.exceptions import MultipleObjectsReturned
from django.http.response   import JsonResponse

from my_settings import SECRET_KEY
from user.models import User

class CheckLogin:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            signed_user = User.objects.get(id=decoded_token['user_id'])
            request.user = signed_user #request에 user정보 담아서 안에서 사용
            return self.func(self, request, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'MESSAGE':'EXPIRED_TOKEN'}, status=400)
        
        except jwt.InvalidSignatureError:
            return JsonResponse({'MESSAGE':'INVALID_TOKEN'}, status=400)
        
        except MultipleObjectsReturned:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=400)