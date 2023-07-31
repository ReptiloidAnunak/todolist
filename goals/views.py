from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView,
                                     ListCreateAPIView)
from rest_framework import permissions
from rest_framework import filters, response
from rest_framework.pagination import LimitOffsetPagination

from goals.models import GoalCategory, Goal, GoalComment
from goals.serializers import (GoalCatCreateSerializer, GoalCategorySerializer, GoalCreateSerializer,
                               GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer)
from filters import GoalDateFilter


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCatCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

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
    queryset = GoalComment.objects.all()
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    ordering_fields = ["created", "updated"]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]


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

