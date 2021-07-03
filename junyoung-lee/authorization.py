import jwt

from django.core.exceptions import MultipleObjectsReturned
from django.http.response   import JsonResponse

from user.models import User
from my_settings import SECRET_KEY

class Authorize:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        try:
            token         = request.headers.get('Authorization')
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            signed_user   = User.objects.get(id=decoded_token['user_id'])
            request.user  = signed_user
            return self.func(self, request, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'MESSAGE':'EXPIRED_TOKEN'}, status=400)
        
        except jwt.InvalidSignatureError:
            return JsonResponse({'MESSAGE':'INVALID_TOKEN'}, status=400)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE':"CHECK_AUTH_KEY_NAME"}, status=400)
        
        except MultipleObjectsReturned:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=400)