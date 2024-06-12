# accounts/management/commands/import_users.py

import csv
import os
import requests
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from django.contrib.auth.models import Group
from app.models import CustomUser
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Import users from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to be imported')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        if not os.path.exists(csv_file_path):
            raise CommandError(f"File '{csv_file_path}' does not exist")

        # Ensure groups exist
        staff_group, created = Group.objects.get_or_create(name='Staff')
        student_group, created = Group.objects.get_or_create(name='Student')

        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                profile_picture_url = row.get('Profile Picture URL')
                register_no =row.get('Register No')
                name = row.get('Name')
                email = row.get('Email')
                password = row.get('Random Password')
                role = row.get('Role')
                department = row.get('Department')

                if not email or not name:
                    self.stdout.write(self.style.ERROR(f"Skipping row with missing email or name: {row}"))
                    continue

                user, created = CustomUser.objects.get_or_create(
                    email=email,
                    defaults={
                       'register_no':register_no,
                        'name': name,
                        'role': role,
                        'department': department,
                        'is_staff': True
                    }
                )

                if created:
                    user.set_password(password)

                    if profile_picture_url:
                        try:
                            response = requests.get(profile_picture_url)
                            response.raise_for_status()
                            profile_picture_name = f"{slugify(name)}.jpg"
                            user.profile_picture.save(profile_picture_name, ContentFile(response.content), save=False)
                        except requests.RequestException as e:
                            self.stdout.write(self.style.WARNING(f"Could not download profile picture for {email}: {e}"))

                    user.save()

                    # Assign groups based on role
                    if role.lower() == 'staff':
                        user.groups.add(staff_group)
                    elif role.lower() == 'student':
                        user.groups.add(student_group)

                    self.stdout.write(self.style.SUCCESS(f"Successfully created user {email}"))
                else:
                    self.stdout.write(self.style.WARNING(f"User with email {email} already exists"))
