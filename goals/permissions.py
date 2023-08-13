from rest_framework import permissions
from goals.models import BoardParticipant, GoalCategory, Goal


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj,
            role=BoardParticipant.Role.owner).exists()


class GoalCategoryPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        user = request.user
        allowed_cat = GoalCategory.objects.filter(
            board__participants__user=user,
            board__participants__role__in=[BoardParticipant.Role.owner,
                                           BoardParticipant.Role.writer]
        )
        cat_to_change = {cat.title: cat.id for cat in allowed_cat}
        return obj.id in cat_to_change.values()


class GoalPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        user = request.user
        allowed_cat = GoalCategory.objects.filter(
            board__participants__user=user,
            board__participants__role__in=[BoardParticipant.Role.owner,
                                           BoardParticipant.Role.writer]
        )
        allowed_goals = Goal.objects.filter(
            category__board__participants__user=user,
            category__in=allowed_cat
        )
        goals_to_change = {goal.title: goal.id for goal in allowed_goals}
        return obj.id in goals_to_change.values()

