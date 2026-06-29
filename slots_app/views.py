from django.utils import timezone
from rest_framework import status, permissions, viewsets, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Slot, Team
from .serializers import (
    TeamSerializer, SlotListSerializer, SlotDetailSerializer,
    SlotCreateSerializer
)
from notifications.models import Notification


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


class SlotViewSet(viewsets.ModelViewSet):
    queryset = Slot.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'request_id', 'team__name']
    ordering_fields = ['date', 'created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return SlotCreateSerializer
        elif self.action in ['retrieve', 'approve', 'reject']:
            return SlotDetailSerializer
        return SlotListSerializer

    def get_queryset(self):
        qs = Slot.objects.all()
        status_filter = self.request.query_params.get('status')
        team_filter = self.request.query_params.get('team')
        date_filter = self.request.query_params.get('date')
        if status_filter:
            qs = qs.filter(status=status_filter)
        if team_filter:
            qs = qs.filter(team_id=team_filter)
        if date_filter:
            qs = qs.filter(date=date_filter)
        return qs

    def perform_create(self, serializer):
        slot = serializer.save(requested_by=self.request.user)
        from accounts.models import User
        hr_users = User.objects.filter(role='hr')
        for hr_user in hr_users:
            Notification.objects.create(
                user=hr_user,
                type='new_slot',
                title='New Slot Request',
                message=f'{self.request.user.get_full_name() or self.request.user.username} requested "{slot.title}" ({slot.request_id})',
                slot=slot,
            )

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        slot = self.get_object()
        if slot.status != 'pending':
            return Response({'error': 'Slot is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        slot.status = 'approved'
        slot.approved_by = request.user
        slot.approved_at = timezone.now()
        slot.save()
        Notification.objects.create(
            user=slot.requested_by,
            type='approved',
            title='Slot Approved',
            message=f'Your slot "{slot.title}" ({slot.request_id}) has been approved.',
            slot=slot
        )
        serializer = SlotDetailSerializer(slot)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        slot = self.get_object()
        if slot.status != 'pending':
            return Response({'error': 'Slot is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        reason = request.data.get('reason', '')
        slot.status = 'rejected'
        slot.rejection_reason = reason
        slot.save()
        Notification.objects.create(
            user=slot.requested_by,
            type='rejected',
            title='Slot Rejected',
            message=f'Your slot "{slot.title}" ({slot.request_id}) has been rejected. Reason: {reason or "N/A"}',
            slot=slot
        )
        serializer = SlotDetailSerializer(slot)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total = Slot.objects.count()
        pending = Slot.objects.filter(status='pending').count()
        approved = Slot.objects.filter(status='approved').count()
        rejected = Slot.objects.filter(status='rejected').count()
        return Response({
            'total': total,
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
        })

    @action(detail=False, methods=['get'])
    def calendar(self, request):
        from datetime import date
        month = request.query_params.get('month', date.today().month)
        year = request.query_params.get('year', date.today().year)
        slots = Slot.objects.filter(
            date__year=year,
            date__month=month,
            status__in=['approved', 'pending', 'rejected']
        )
        serializer = SlotListSerializer(slots, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        total = Slot.objects.count()
        pending = Slot.objects.filter(status='pending').count()
        approved = Slot.objects.filter(status='approved').count()
        rejected = Slot.objects.filter(status='rejected').count()

        today_slots = Slot.objects.filter(date=timezone.now().date()).order_by('start_time')[:5]
        recent_notifs = Notification.objects.filter(user=request.user)[:5]

        from accounts.serializers import UserSerializer
        from notifications.serializers import NotificationSerializer

        return Response({
            'stats': {
                'total': total,
                'pending': pending,
                'approved': approved,
                'rejected': rejected,
            },
            'today_schedule': SlotListSerializer(today_slots, many=True).data,
            'recent_notifications': NotificationSerializer(recent_notifs, many=True).data,
        })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def team_list(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)
