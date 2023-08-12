from rest_framework import serializers
from django.db import transaction

from core.models import User
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from core.serializers import UserDetailSerializer


class GoalCatCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_board(self, board: Board) -> Board:
        """Проверяет участие и роль пользователя в доске,
        дает право создавать категорию, если он владелец или редактор"""
        allowed_boards = Board.objects.filter(participants__user=self.context["request"].user,
                                              participants__role__in=[BoardParticipant.Role.owner,
                                                                      BoardParticipant.Role.writer]
                                              )
        boards_to_create_cat = {board.title: board.id for board in allowed_boards}
        if board.id not in boards_to_create_cat.values():
            raise serializers.ValidationError("Not allowed")
        return board

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, category: GoalCategory) -> GoalCategory:
        allowed_cat = GoalCategory.objects.filter(
            board__participants__user=self.context["request"].user,
            board__participants__role__in=[BoardParticipant.Role.owner,
                                           BoardParticipant.Role.writer]
        )
        cat_to_create_goal = {cat.title: cat.id for cat in allowed_cat}
        if category.id not in cat_to_create_goal.values():
            raise serializers.ValidationError("Not allowed")
        return category

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    def validate_category(self, category: GoalCategory):
        """Запрещает создавать цель в удаленной доске"""
        if category.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")
        return category

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

    def validate_goal(self, goal: Goal) -> Goal:
        """Запрещает комментировать удаленные цели,
        позволяет комментировать только собственнику и редактору"""
        if goal.is_deleted:
            raise serializers.ValidationError("not allowed in deleted goal")

        if not BoardParticipant.objects.filter(board=goal.category.board,
                                               user=self.context['request'].user,
                                               role__in=[BoardParticipant.Role.owner,
                                                         BoardParticipant.Role.writer]).exists():
            raise serializers.ValidationError("not allowed")
        return goal

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data) -> Board:
        """Автоматически привязывает пользователя
         к создаваемой доске в качестве собственника"""
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(user=user, board=board, role=BoardParticipant.Role.owner)
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                            old_participant.role
                            != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            instance.title = validated_data["title"]
            instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"

        