import json, jwt, bcrypt

from django.core.exceptions import MultipleObjectsReturned
from django.db.utils        import IntegrityError
from django.http            import JsonResponse
from django.views           import View
from django.utils           import timezone

from my_settings     import SECRET_KEY
from user.models     import User, Follow
from authorization   import Authorize
from user.validators import (
    validate_email, 
    validate_password, 
    validate_name, 
    validate_phone_number
)

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if not validate_email(data['email']):
                return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status = 400)
            
            if not validate_password(data['password']):
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status = 400)
            
            if not validate_name(data['name']):
                return JsonResponse({'MESSAGE':'INVALID_NAME'}, status = 400)
            
            if not validate_phone_number(data['phone_number']):
                return JsonResponse({'MESSAGE':'INVALID_PHONE_NUMBER'}, status = 400)
            
            encoded_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            User.objects.create(
                name         = data['name'],
                nickname     = data['nickname'],
                email        = data['email'],
                phone_number = data['phone_number'],
                password     = encoded_password.decode('utf-8'),
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

        except IntegrityError:
            return JsonResponse({'MESSAGE':'USER_ALREADY_EXISTS'}, status=400)

class SigninView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = User.objects.get(email=data['email'])
            if bcrypt.checkpw(
                data['password'].encode('utf-8'), 
                user.password.encode('utf-8')
                ):
                encoded_jwt = jwt.encode(
                    {
                        'user_id' : user.pk,
                        'exp'     : timezone.localtime() + timezone.timedelta(days=3)
                    }, 
                    SECRET_KEY, 
                    algorithm='HS256'
                )
                return JsonResponse({'MESSAGE':'SUCCESS', 'ACCESS_TOKEN':encoded_jwt}, status=200)

            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except MultipleObjectsReturned:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class FollowView(View):
    @Authorize
    def get(self, request, user_id):
        try:
            signed_user = request.user
            followee    = User.objects.get(pk=user_id)
            
            if signed_user.id == user_id:
                return JsonResponse({"MESSAGE":"CAN'T_FOLLOW_SELF"}, status=400)

            if Follow.objects.filter(followee=followee, follower=signed_user).exists():
                Follow.objects.get(followee=followee, follower=signed_user).delete()
                return JsonResponse({"MESSAGE":"UNFOLLOWED"}, status=200)
                
            Follow.objects.create(
                followee = followee,
                follower = signed_user
            )
            return JsonResponse({"MESSAGE":"FOLLOWED"}, status=201)

        except ValueError:
            return JsonResponse({"MESSAGE": "ERROR"}, status=400)

class FollowerView(View):
    def get(self, request, user_id):
        try:
            user      = User.objects.get(pk=user_id)
            user_info = {
                'nickname' : user.nickname,
                'followers': len(Follow.objects.filter(follow_user=user))
            }
            return JsonResponse({"MESSAGE":user_info}, status=200)

        except:
            return JsonResponse({"MESSAGE": "ERROR"}, status=400)