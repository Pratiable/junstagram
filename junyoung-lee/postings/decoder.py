from django.core.exceptions import MultipleObjectsReturned
from django.http.response import JsonResponse
from my_settings import SECRET_KEY
from user.models import User
import jwt

class TokenChecker:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Access-Token')
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            if User.objects.get(id=decoded_token['user_id']):
                return self.func(self, request)
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'MESSAGE':'EXPIRED_TOKEN'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=400)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        
        except MultipleObjectsReturned:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=400)