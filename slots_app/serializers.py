from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Team, Slot, BlockedDate
from accounts.serializers import UserSerializer

User = get_user_model()


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description']


class SlotListSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    requested_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = ['id', 'request_id', 'title', 'description', 'category', 'category_display',
                  'team', 'team_name', 'team_lead', 'date', 'start_time', 'end_time',
                  'requested_by', 'requested_by_name', 'status', 'status_display',
                  'approved_by', 'approved_at', 'rejection_reason', 'created_at']

    def get_requested_by_name(self, obj):
        return obj.requested_by.get_full_name() or obj.requested_by.username


class SlotDetailSerializer(SlotListSerializer):
    developers = UserSerializer(many=True, read_only=True)
    team_lead_name = serializers.SerializerMethodField()

    class Meta(SlotListSerializer.Meta):
        fields = SlotListSerializer.Meta.fields + ['developers']

    def get_team_lead_name(self, obj):
        if obj.team_lead:
            return obj.team_lead.get_full_name() or obj.team_lead.username
        return None


class SlotCreateSerializer(serializers.ModelSerializer):
    developers = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)

    class Meta:
        model = Slot
        fields = ['title', 'description', 'category', 'team', 'team_lead',
                  'developers', 'date', 'start_time', 'end_time']

    def validate(self, data):
        if data['end_time'] <= data['start_time']:
            raise serializers.ValidationError({'end_time': 'End time must be after start time'})
        if BlockedDate.objects.filter(date=data['date']).exists():
            raise serializers.ValidationError({'date': 'This date is blocked and cannot be booked'})
        return data

    def create(self, validated_data):
        developers = validated_data.pop('developers', [])
        slot = Slot.objects.create(**validated_data)
        slot.developers.set(developers)
        return slot


class SlotActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    comment = serializers.CharField(required=False, allow_blank=True)


class BlockedDateSerializer(serializers.ModelSerializer):
    blocked_by_name = serializers.SerializerMethodField()

    class Meta:
        model = BlockedDate
        fields = ['id', 'date', 'reason', 'blocked_by', 'blocked_by_name', 'created_at']

    def get_blocked_by_name(self, obj):
        if obj.blocked_by:
            return obj.blocked_by.get_full_name() or obj.blocked_by.username
        return None
