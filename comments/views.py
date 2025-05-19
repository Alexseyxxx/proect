import logging
from typing import Literal

from django.views import View
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from comments.models import CommentReaction
from comments.models import Comments
from posts.models import Posts
from clients.models import Client

from django.conf import settings

logger = logging.getLogger()


class AddComment(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        client = request.user
        if not isinstance(client, Client):
            return JsonResponse(data={"error": "not authorized"})
        posts = Posts.objects.filter(id=pk)
        if not posts:
            return JsonResponse(
                data={"error": f"Post with id {pk} not found"}
            )
        comment = Comments(
            post=posts[0], user=client,
            text=request.POST.get("text")
        )
        comment.save()
        return redirect("pk_post", pk=pk)


class AddReply(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        client = request.user
        if not isinstance(client, Client):
            return JsonResponse(data={"error": "not authorized"})
        comments = Comments.objects.filter(id=pk)
        if not comments:
            return JsonResponse(
                data={"error": f"Comment with id {pk} not found"}
            )
        comment = Comments(
            post=comments[0].post,
            user=client,
            parent=comments[0],
            text=request.POST.get("text")
        )
        comment.save()
        return redirect("pk_post", pk=comments[0].post.pk)
    
class CommentLikeView(View):
    def post(self, request, pk, action):
        client = request.user
        if not isinstance(client, Client):
            return JsonResponse({"error": "not authorized"}, status=403)

        try:
            comment = Comments.objects.get(pk=pk)
        except Comments.DoesNotExist:
            return JsonResponse({"error": "Comment not found"}, status=404)

        # Если реакция уже существует, обновить её или удалить
        reaction = CommentReaction.objects.filter(user=client, comment=comment).first()

        if reaction and reaction.reaction == action:
            reaction.delete()  # удаляем реакцию, если повторное нажатие
        elif reaction:
            reaction.reaction = action  # обновляем реакцию
            reaction.save()
        else:
            CommentReaction.objects.create(user=client, comment=comment, reaction=action)

        return redirect(request.META.get("HTTP_REFERER", "base"))

