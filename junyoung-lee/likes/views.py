from django.http.response import JsonResponse
from django.views         import View

from likes.models           import Like
from postings.authorization import Authorize

class LikeView(View):
    @Authorize
    def get(self, request, postpk):
        signed_user = request.user

        if Like.objects.filter(user=signed_user, post_id=postpk).exists():
            Like.objects.get(user=signed_user, post_id=postpk).delete()
            return JsonResponse({"MESSAGE":"SUCCESS"}, status = 200)

        Like.objects.create(
            user    = signed_user,
            post_id = postpk
        )
        return JsonResponse({"MESSAGE":"SUCCESS"}, status = 201)
