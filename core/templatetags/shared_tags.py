from django import template

from core.models import ProcessFeedback

register = template.Library()


@register.simple_tag
def user_has_published_process_feedback(user, process):
    return ProcessFeedback.objects.filter(
        process=process, created_by=user
    ).exists()
