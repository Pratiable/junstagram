from django.http.response import JsonResponse
from django.views         import View

from user.models            import User
from follows.models         import Follow
from postings.authorization import Authorize

class FollowView(View):
    @Authorize
    def get(self, request, user_id):
        try:
            signed_user = request.user
            follow_user = User.objects.get(pk=user_id)
            
            if signed_user.id == user_id:
                return JsonResponse({"MESSAGE":"CAN'T_FOLLOW_SELF"})

            if Follow.objects.filter(follow_user=follow_user, followers=signed_user).exists():
                Follow.objects.get(follow_user=follow_user, followers=signed_user).delete()
                return JsonResponse({"MESSAGE":"UNFOLLOWED"}, status=200)
                
            Follow.objects.create(
                follow_user = follow_user,
                followers = signed_user
            )
            return JsonResponse({"MESSAGE":"FOLLOWED"}, status=201)

        except ValueError:
            return JsonResponse({"MESSAGE": "ERROR"}, status=400)

class FollowerView(View):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user_info = {
                'nickname' : user.nickname,
                'followers' : len(Follow.objects.filter(follow_user=user))
            }
            return JsonResponse({"MESSAGE":user_info}, status=200)

        except Exception as e:
            return JsonResponse({"MESSAGE": "ERROR"}, status=400)
