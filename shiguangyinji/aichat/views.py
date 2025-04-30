from django.http import JsonResponse
from django.views import View
from .postrequest import send
from .models import ChatInfo


class AIChat(View):
    hello = '您好啊！我是张伟，刚泡了一壶茶，正好闲下来。不知道您愿不愿意和我一起聊聊天，分享一下您的故事？我特别喜欢听别人的人生经历，总能从中学到很多。'

    def post(self, request, *args, **kwargs):
        q = request.POST.get('question')
        user = request.POST.get('user')
        cid = request.POST.get('conversation_id', '')
        print(f"Received question: {q}, user: {user}, conversation_id: {cid}")
        isOk, ret_conversation_id, ret_content, ret_status_code, ret_err_text = send(q, user, cid)
        if isOk:
            ChatInfo.objects.create(user=user, answer=ret_content, question=q)
            return JsonResponse({'errno': 0, 'conversation_id': ret_conversation_id, 'msg': ret_content})
        else:
            return JsonResponse({'errno': 1001, 'conversation_id': ret_conversation_id, 'msg': ret_err_text})

    def get(self, request, *args, **kwargs):
        return JsonResponse({'errno': 0, 'conversation_id': '', 'msg': self.hello})
