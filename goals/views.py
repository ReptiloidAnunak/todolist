
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView,
                                     ListCreateAPIView)
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.serializers import (GoalCatCreateSerializer, GoalCategorySerializer, GoalCreateSerializer,
                               GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer,
                               BoardCreateSerializer, BoardSerializer)
from goals.permissions import BoardPermissions, GoalCategoryPermission, GoalCategoryCreatePermission
from filters import GoalDateFilter, GoalCategoryBoardFilter


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCatCreateSerializer
    permission_classes = [permissions.IsAuthenticated, GoalCategoryCreatePermission]


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    filterset_fields = ["board"]
    filterset_class = GoalCategoryBoardFilter

    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False)

    def get_permissions(self):
        self.permission_classes = [permissions.IsAuthenticated]

        if self.request.method not in permissions.SAFE_METHODS:
            self.permission_classes = [GoalCategoryPermission]
        return super(GoalCategoryView, self).get_permissions()

    def perform_destroy(self, instance):
        cat_goals = Goal.objects.filter(category=instance.id)

        for goal in cat_goals:
            goal.is_deleted = True
            goal.category = None
            goal.save()
        instance.is_deleted = True
        instance.delete()
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class GoalListView(ListAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]
    filter_backends = [
                       DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter
                        ]
    filterset_class = GoalDateFilter

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCommentListView(ListAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["created", "updated"]
    filterset_fields = ["goal"]
    ordering = "-id"

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)


class GoalCommentCrateView(CreateAPIView):
    model = GoalComment
    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user)


class BoardCreateView(CreateAPIView):
    model = Board
    queryset = Board.objects.all()
    serializer_class = BoardCreateSerializer
    permissions_classes = [permissions.IsAuthenticated]


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user,
                                    is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance


class BoardListView(ListAPIView):
    model = Board
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["title", "created"]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user, is_deleted=False
        )