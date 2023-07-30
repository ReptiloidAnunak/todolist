from rest_framework import serializers

from goals.models import GoalCategory, Goal, GoalComment
from core.serializers import UserDetailSerializer


class GoalCatCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.SlugRelatedField(read_only=False,
                                            required=True,
                                            queryset=GoalCategory.objects.all(),
                                            label="Категория",
                                            slug_field="title")

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")
        return value


class GoalSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    category = serializers.SlugRelatedField(read_only=False,
                                            required=True,
                                            queryset=GoalCategory.objects.all(),
                                            label="Категория",
                                            slug_field="title",)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "goal")


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_goal(self, goal):
        if goal.is_deleted:
            raise serializers.ValidationError("not allowed in deleted goal")
        if goal.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of goal")
        return goal

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

