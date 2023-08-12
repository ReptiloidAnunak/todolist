
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView,
                                     )
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from goals.serializers import (GoalCatCreateSerializer, GoalCategorySerializer, GoalCreateSerializer,
                               GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer,
                               BoardCreateSerializer, BoardSerializer)
from goals.permissions import BoardPermissions, GoalCategoryPermission, GoalPermission
from goals.filters import GoalDateFilter, GoalCategoryBoardFilter


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCatCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


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

    def get_queryset(self) -> list:
        """Фильтрует категории исключительно
        для участников доски"""
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer

    def get_queryset(self) -> list:
        """Фильтрует категории исключительно
        для участников доски"""
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False)

    def get_permissions(self):
        """Ограничивает права на изменение категорий читателю
        и неаутентифицированным пользователям"""
        self.permission_classes = [permissions.IsAuthenticated]

        if self.request.method not in permissions.SAFE_METHODS:
            self.permission_classes = [GoalCategoryPermission]
        return super(GoalCategoryView, self).get_permissions()

    def perform_destroy(self, instance):
        """Переводит категорию в статус is_deleted
        вместо полного ее удаления из базы данных"""
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
        """Фильтрует цели исключительно
        для участников доски"""
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            is_deleted=False,
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer

    def get_queryset(self):
        """Фильтрует цели исключительно
        для участников доски"""
        return Goal.objects.filter(
            category__board__participants__user=self.request.user,
            is_deleted=False)

    def get_permissions(self):
        """В случае использования метода GET дает доступ к просмотру
        аутентифицированному пользователю.
        В случае попытки изменения цели задействует GoalPermission"""
        self.permission_classes = [permissions.IsAuthenticated]

        if self.request.method not in permissions.SAFE_METHODS:
            self.permission_classes = [GoalPermission]
        return super(GoalView, self).get_permissions()

    def perform_destroy(self, instance):
        """Переводит цель в статус is_deleted
        вместо полного удаления из базы данных"""
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCommentListView(ListAPIView):
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["created", "updated"]
    filterset_fields = ["goal"]
    ordering = "-id"

    def get_queryset(self):
        """Фильтрует комментарии к целям
        исключительно для участников доски"""
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


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
        """Позволяет редактировать и удалять комментарий
         только его автору"""
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
        """Позволяет видеть доску исключительно ее участникам"""
        return Board.objects.filter(participants__user=self.request.user,
                                    is_deleted=False)

    def perform_destroy(self, instance: Board):
        """Переводит доску в статус is_deleted вместо полного ее удаления из базы данных,
        а также связанные с ней категории. Цели переводятся в архив
        для возможного дальнейшего перераспределения"""
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
        """Позволяет видеть список досок исключительно их участникам"""
        return Board.objects.filter(
            participants__user=self.request.user, is_deleted=False
        )
