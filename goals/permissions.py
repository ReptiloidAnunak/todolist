from rest_framework import permissions
from goals.models import BoardParticipant, GoalCategory, Board


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
            board__participants__role__in=[1, 2]
        )
        cat_to_change = {goal.title: goal.id for goal in allowed_cat}
        return obj.id in cat_to_change.values()


class GoalCategoryCreatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        board = obj.board
        user = request.user
        allowed_boards = Board.objects.filter(participants__user=user,
                                              participants__role__in=[1, 2]
                                              )
        board_to_create_cat = {board.title: board.id for board in allowed_boards}
        print(board.id in board_to_create_cat.values())
        return board.id in board_to_create_cat.values()


