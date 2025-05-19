from django.db import models
from django.utils import timezone

from clients.models import Client
from posts.models import Posts

class Comments(models.Model):
    post = models.ForeignKey(
        to=Posts,
        on_delete=models.CASCADE,
        related_name="post_comments",
        verbose_name="статья",
    )
    user = models.ForeignKey(
        to=Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_comments",
        verbose_name="автор комментария",
    )
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="child_comments",
        verbose_name="родительский комментарий",
    )
    text = models.TextField(
        verbose_name="текст комментария",
        max_length=2000,
    )
    date_created = models.DateTimeField(
        verbose_name="дата создания",
        default=timezone.now,
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"

    def __str__(self):
        return f"{self.user} | {self.text[:20]}..."

    @property
    def likes_count(self):
        return self.reactions.filter(reaction=CommentReaction.LIKE).count()

    @property
    def dislikes_count(self):
        return self.reactions.filter(reaction=CommentReaction.DISLIKE).count()


class CommentReaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    REACTION_CHOICES = [
        (LIKE, 'Лайк'),
        (DISLIKE, 'Дизлайк'),
    ]

    user = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
        related_name="comment_reactions"
    )
    comment = models.ForeignKey(
        to='Comments',
        on_delete=models.CASCADE,
        related_name="reactions"
    )
    reaction = models.CharField(
        max_length=7,
        choices=REACTION_CHOICES
    )

    class Meta:
        unique_together = ("user", "comment")

    def __str__(self):
        return f"{self.user} - {self.comment} - {self.reaction}"