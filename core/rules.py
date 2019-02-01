import rules

from core.models import Process, ProcessFeedback


@rules.predicate
def is_admin_user(user, obj):
    return user.profile.is_admin


@rules.predicate
def is_manager_user(user, obj):
    return user.profile.is_manager


@rules.predicate
def is_publisher_user(user, obj):
    return user.profile.is_publisher


@rules.predicate
def is_process_member(user, process):
    """
    Checks whether the user is a member of a Process
    """
    assert isinstance(process, Process)
    return process.feedback_users.filter(pk=user.pk).exists()


@rules.predicate
def is_processfeedback_owner(user, process_feedback):
    """
    Checks whether the user is owner of a ProcessFeedback
    """
    assert isinstance(process_feedback, ProcessFeedback)
    return process_feedback.created_by == user


rules.add_perm('admin_user', is_admin_user)
rules.add_perm('manager_user', is_manager_user)
rules.add_perm('publisher_user', is_publisher_user)

rules.add_perm('core.list_process', is_manager_user | is_publisher_user)
rules.add_perm('core.view_process', is_manager_user | is_process_member)
rules.add_perm('core.create_process', is_manager_user)
rules.add_perm('core.update_process', is_manager_user)
rules.add_perm('core.delete_process', is_manager_user)

rules.add_perm('core.create_processfeedback', is_process_member)
rules.add_perm('core.update_processfeedback', is_processfeedback_owner)
