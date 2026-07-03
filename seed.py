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

# Create users - 4 Team Leads with their Developers
users_data = [
    # Admin & HR
    {'username': 'admin', 'email': 'admin@slotflow.com', 'first_name': 'Admin', 'last_name': 'User', 'role': 'admin', 'team': None},
    {'username': 'hruser', 'email': 'hr@slotflow.com', 'first_name': 'HR', 'last_name': 'User', 'role': 'hr', 'team': None},

    # Hardik (Team Lead - Design Team)
    {'username': 'hardik', 'email': 'hardik@slotflow.com', 'first_name': 'Hardik', 'last_name': 'Patel', 'role': 'team_lead', 'team': 'Design Team'},
    {'username': 'rahul', 'email': 'rahul@slotflow.com', 'first_name': 'Rahul', 'last_name': 'Sharma', 'role': 'developer', 'team': 'Design Team'},
    {'username': 'priya', 'email': 'priya@slotflow.com', 'first_name': 'Priya', 'last_name': 'Joshi', 'role': 'developer', 'team': 'Design Team'},
    {'username': 'kartik', 'email': 'kartik@slotflow.com', 'first_name': 'Kartik', 'last_name': 'Reddy', 'role': 'developer', 'team': 'Design Team'},

    # Amit (Team Lead - Development Team)
    {'username': 'amit', 'email': 'amit@slotflow.com', 'first_name': 'Amit', 'last_name': 'Verma', 'role': 'team_lead', 'team': 'Development Team'},
    {'username': 'jay', 'email': 'jay@slotflow.com', 'first_name': 'Jay', 'last_name': 'Mehta', 'role': 'developer', 'team': 'Development Team'},
    {'username': 'ravi', 'email': 'ravi@slotflow.com', 'first_name': 'Ravi', 'last_name': 'Kumar', 'role': 'developer', 'team': 'Development Team'},
    {'username': 'neha', 'email': 'neha@slotflow.com', 'first_name': 'Neha', 'last_name': 'Gupta', 'role': 'developer', 'team': 'Development Team'},

    # Parth (Team Lead - Embroidery Team)
    {'username': 'parth', 'email': 'parth@slotflow.com', 'first_name': 'Parth', 'last_name': 'Mehta', 'role': 'team_lead', 'team': 'Embroidery Team'},
    {'username': 'sneha', 'email': 'sneha@slotflow.com', 'first_name': 'Sneha', 'last_name': 'Patil', 'role': 'developer', 'team': 'Embroidery Team'},
    {'username': 'karan', 'email': 'karan@slotflow.com', 'first_name': 'Karan', 'last_name': 'Singh', 'role': 'developer', 'team': 'Embroidery Team'},
    {'username': 'deepa', 'email': 'deepa@slotflow.com', 'first_name': 'Deepa', 'last_name': 'Nair', 'role': 'developer', 'team': 'Embroidery Team'},

    # Niket (Team Lead - QA Team)
    {'username': 'niket', 'email': 'niket@slotflow.com', 'first_name': 'Niket', 'last_name': 'Shah', 'role': 'team_lead', 'team': 'QA Team'},
    {'username': 'pooja', 'email': 'pooja@slotflow.com', 'first_name': 'Pooja', 'last_name': 'Singh', 'role': 'developer', 'team': 'QA Team'},
    {'username': 'ankit', 'email': 'ankit@slotflow.com', 'first_name': 'Ankit', 'last_name': 'Desai', 'role': 'developer', 'team': 'QA Team'},
    {'username': 'meera', 'email': 'meera@slotflow.com', 'first_name': 'Meera', 'last_name': 'Rao', 'role': 'developer', 'team': 'QA Team'},
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
    print(f"User: {user.get_full_name()} ({user.role}) - {u_data['team'] or 'No Team'}")

# Create sample slots
today = date.today()
slots_data = [
    # Hardik's team slots
    {'title': 'Design Review Meeting', 'description': 'Review new UI mockups for the mobile app redesign.', 'category': 'design', 'team': 'Design Team', 'team_lead': 'hardik', 'developers': ['rahul', 'priya', 'kartik'], 'date': today + timedelta(days=3), 'start_time': time(13, 0), 'end_time': time(15, 0), 'requested_by': 'hardik', 'status': 'pending'},

    # Amit's team slots
    {'title': 'Sprint Planning', 'description': 'Sprint planning for the upcoming release cycle.', 'category': 'development', 'team': 'Development Team', 'team_lead': 'amit', 'developers': ['jay', 'ravi', 'neha'], 'date': today, 'start_time': time(10, 0), 'end_time': time(12, 0), 'requested_by': 'amit', 'status': 'approved', 'approved_by': 'hruser'},
    {'title': 'Code Review Session', 'description': 'Review pull requests and discuss coding standards.', 'category': 'development', 'team': 'Development Team', 'team_lead': 'amit', 'developers': ['jay', 'neha'], 'date': today + timedelta(days=2), 'start_time': time(14, 0), 'end_time': time(16, 0), 'requested_by': 'ravi', 'status': 'pending'},

    # Parth's team slots
    {'title': 'Embroidery Design Review', 'description': 'Review and approve new embroidery patterns for the collection.', 'category': 'embroidery', 'team': 'Embroidery Team', 'team_lead': 'parth', 'developers': ['sneha', 'karan', 'deepa'], 'date': today + timedelta(days=1), 'start_time': time(11, 0), 'end_time': time(13, 0), 'requested_by': 'parth', 'status': 'approved', 'approved_by': 'hruser'},
    {'title': 'Stitching Quality Check', 'description': 'Quality inspection of completed embroidery samples.', 'category': 'embroidery', 'team': 'Embroidery Team', 'team_lead': 'parth', 'developers': ['sneha', 'deepa'], 'date': today - timedelta(days=1), 'start_time': time(9, 0), 'end_time': time(11, 0), 'requested_by': 'karan', 'status': 'rejected', 'rejection_reason': 'Schedule conflict with another team meeting.'},

    # Niket's team slots
    {'title': 'QA Test Planning', 'description': 'Plan test cases for the new feature release.', 'category': 'qa', 'team': 'QA Team', 'team_lead': 'niket', 'developers': ['pooja', 'ankit', 'meera'], 'date': today + timedelta(days=4), 'start_time': time(15, 0), 'end_time': time(17, 0), 'requested_by': 'niket', 'status': 'pending'},
    {'title': 'Bug Triage Meeting', 'description': 'Prioritize and assign reported bugs for the sprint.', 'category': 'qa', 'team': 'QA Team', 'team_lead': 'niket', 'developers': ['pooja', 'ankit'], 'date': today + timedelta(days=1), 'start_time': time(16, 0), 'end_time': time(17, 30), 'requested_by': 'meera', 'status': 'pending'},
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

print("\n" + "=" * 60)
print("Seed data created successfully!")
print("=" * 60)
print("\nDemo accounts (password: password123):")
print("-" * 60)
print(f"  {'Email':<28} {'Role':<12} {'Team'}")
print("-" * 60)
print(f"  {'admin@slotflow.com':<28} {'Admin':<12} All Teams")
print(f"  {'hr@slotflow.com':<28} {'HR':<12} All Teams")
print(f"  {'hardik@slotflow.com':<28} {'Team Lead':<12} Design Team")
print(f"  {'rahul@slotflow.com':<28} {'Developer':<12} Design Team")
print(f"  {'priya@slotflow.com':<28} {'Developer':<12} Design Team")
print(f"  {'kartik@slotflow.com':<28} {'Developer':<12} Design Team")
print(f"  {'amit@slotflow.com':<28} {'Team Lead':<12} Development Team")
print(f"  {'jay@slotflow.com':<28} {'Developer':<12} Development Team")
print(f"  {'ravi@slotflow.com':<28} {'Developer':<12} Development Team")
print(f"  {'neha@slotflow.com':<28} {'Developer':<12} Development Team")
print(f"  {'parth@slotflow.com':<28} {'Team Lead':<12} Embroidery Team")
print(f"  {'sneha@slotflow.com':<28} {'Developer':<12} Embroidery Team")
print(f"  {'karan@slotflow.com':<28} {'Developer':<12} Embroidery Team")
print(f"  {'deepa@slotflow.com':<28} {'Developer':<12} Embroidery Team")
print(f"  {'niket@slotflow.com':<28} {'Team Lead':<12} QA Team")
print(f"  {'pooja@slotflow.com':<28} {'Developer':<12} QA Team")
print(f"  {'ankit@slotflow.com':<28} {'Developer':<12} QA Team")
print(f"  {'meera@slotflow.com':<28} {'Developer':<12} QA Team")
