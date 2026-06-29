import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slotflow.settings')
django.setup()

from django.contrib.auth import get_user_model
from slots_app.models import Team, Slot
from notifications.models import Notification
from datetime import date, time, timedelta
from django.utils import timezone

User = get_user_model()

# Create teams
teams_data = [
    {'name': 'Design Team', 'description': 'Design department'},
    {'name': 'Development Team', 'description': 'Development department'},
    {'name': 'Embroidery Team', 'description': 'Embroidery department'},
    {'name': 'QA Team', 'description': 'Quality Assurance department'},
]

teams = {}
for t_data in teams_data:
    team, _ = Team.objects.get_or_create(name=t_data['name'], defaults={'description': t_data['description']})
    teams[t_data['name']] = team
    print(f"Team: {team.name}")

# Create users
users_data = [
    {'username': 'hardik', 'email': 'hardik@slotflow.com', 'first_name': 'Hardik', 'last_name': 'Patel', 'role': 'admin', 'team': 'Design Team'},
    {'username': 'rahul', 'email': 'rahul@slotflow.com', 'first_name': 'Rahul', 'last_name': 'Sharma', 'role': 'team_lead', 'team': 'Design Team'},
    {'username': 'amit', 'email': 'amit@slotflow.com', 'first_name': 'Amit', 'last_name': 'Verma', 'role': 'developer', 'team': 'Embroidery Team'},
    {'username': 'jay', 'email': 'jay@slotflow.com', 'first_name': 'Jay', 'last_name': 'Mehta', 'role': 'developer', 'team': 'Development Team'},
    {'username': 'pooja', 'email': 'pooja@slotflow.com', 'first_name': 'Pooja', 'last_name': 'Singh', 'role': 'team_lead', 'team': 'QA Team'},
    {'username': 'hruser', 'email': 'hr@slotflow.com', 'first_name': 'HR', 'last_name': 'User', 'role': 'hr', 'team': None},
    {'username': 'ravi', 'email': 'ravi@slotflow.com', 'first_name': 'Ravi', 'last_name': 'Kumar', 'role': 'developer', 'team': 'Development Team'},
    {'username': 'admin', 'email': 'admin@slotflow.com', 'first_name': 'Admin', 'last_name': 'User', 'role': 'admin', 'team': None},
]

users = {}
for u_data in users_data:
    team = teams.get(u_data['team']) if u_data['team'] else None
    user, created = User.objects.get_or_create(
        username=u_data['username'],
        defaults={
            'email': u_data['email'],
            'first_name': u_data['first_name'],
            'last_name': u_data['last_name'],
            'role': u_data['role'],
            'team': team,
        }
    )
    if created:
        user.set_password('password123')
        user.save()
    users[u_data['username']] = user
    print(f"User: {user.get_full_name()} ({user.role})")

# Create sample slots
today = date.today()
slots_data = [
    {'title': 'Design Review Meeting', 'description': 'Discuss new design requirements and feedback.', 'category': 'design', 'team': 'Design Team', 'team_lead': 'rahul', 'developers': ['hardik', 'amit', 'jay'], 'date': today + timedelta(days=3), 'start_time': time(13, 0), 'end_time': time(15, 0), 'requested_by': 'hardik', 'status': 'pending'},
    {'title': 'Embroidery Review', 'description': 'Review embroidery samples and approve designs.', 'category': 'embroidery', 'team': 'Embroidery Team', 'team_lead': 'rahul', 'developers': ['amit', 'jay'], 'date': today + timedelta(days=1), 'start_time': time(11, 30), 'end_time': time(13, 0), 'requested_by': 'amit', 'status': 'approved', 'approved_by': 'hruser'},
    {'title': 'Development Review', 'description': 'Development review and planning.', 'category': 'development', 'team': 'Development Team', 'team_lead': 'amit', 'developers': ['pooja', 'ravi'], 'date': today, 'start_time': time(14, 0), 'end_time': time(16, 0), 'requested_by': 'jay', 'status': 'rejected', 'rejection_reason': 'Time slot already booked for another meeting.', 'approved_by': 'hruser'},
    {'title': 'QA Sync', 'description': 'QA sync and testing updates.', 'category': 'qa', 'team': 'QA Team', 'team_lead': 'pooja', 'developers': ['hardik', 'jay'], 'date': today - timedelta(days=1), 'start_time': time(10, 0), 'end_time': time(11, 30), 'requested_by': 'pooja', 'status': 'approved', 'approved_by': 'hruser'},
    {'title': 'Sprint Planning', 'description': 'Sprint planning for next release.', 'category': 'development', 'team': 'Development Team', 'team_lead': 'amit', 'developers': ['ravi', 'jay'], 'date': today - timedelta(days=2), 'start_time': time(9, 0), 'end_time': time(10, 30), 'requested_by': 'ravi', 'status': 'approved', 'approved_by': 'hruser'},
]

for s_data in slots_data:
    team = teams[s_data['team']]
    team_lead = users.get(s_data['team_lead'])
    requested_by = users[s_data['requested_by']]
    approved_by = users.get(s_data.get('approved_by')) if s_data.get('approved_by') else None

    slot, created = Slot.objects.get_or_create(
        title=s_data['title'],
        defaults={
            'description': s_data['description'],
            'category': s_data['category'],
            'team': team,
            'team_lead': team_lead,
            'requested_by': requested_by,
            'date': s_data['date'],
            'start_time': s_data['start_time'],
            'end_time': s_data['end_time'],
            'status': s_data['status'],
            'approved_by': approved_by,
            'approved_at': timezone.now() if s_data['status'] == 'approved' else None,
            'rejection_reason': s_data.get('rejection_reason', ''),
        }
    )
    if created:
        if s_data.get('developers'):
            devs = [users[d] for d in s_data['developers'] if d in users]
            slot.developers.set(devs)
        slot.save()
    print(f"Slot: {slot.request_id} - {slot.title} ({slot.status})")

    # Create notifications
    if created:
        notif_type_map = {'approved': 'approved', 'rejected': 'rejected', 'pending': 'new_slot'}
        Notification.objects.get_or_create(
            user=requested_by,
            slot=slot,
            type=notif_type_map.get(slot.status, 'new_slot'),
            defaults={
                'title': f"Slot {slot.status.title()}",
                'message': f'Your slot "{slot.title}" ({slot.request_id}) has been {slot.status}.',
                'is_read': slot.status != 'pending',
            }
        )

print("\nSeed data created successfully!")
print("\nDemo accounts:")
print("  admin@slotflow.com / password123  -> Admin")
print("  hr@slotflow.com / password123     -> HR")
