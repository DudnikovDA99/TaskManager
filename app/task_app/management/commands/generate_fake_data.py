import os
import random
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from faker import Faker

from ...models import Task

load_dotenv()

fake = Faker("ru_RU")
User = get_user_model()
fake.date


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--total_users", type=int)
        parser.add_argument("--total_tasks", type=int)

    def handle(self, *args, **options):
        total_users = options["total_users"]
        total_tasks = options["total_tasks"]
        user = self.create_user()
        self.create_task(user)
        self.create_data(total_users, total_tasks)

    def create_user(self):
        username = fake.unique.user_name()
        email = fake.unique.email()
        now = datetime.now()
        user = User.objects.create_user(
            password=os.getenv("TEST_PASSWORD"),
            last_login=fake.date_time_between(start_date=now.replace(now.year - 2)),
            is_superuser=False,
            username=username,
            last_name=fake.last_name(),
            email=email,
            is_staff=False,
            is_active=random.choice([True, False]),
            date_joined=fake.date_time_between(
                start_date=now.replace(now.year - 4),
                end_date=now.replace(now.year - 2),
            ),
            first_name=fake.first_name(),
        )
        return user

    def create_task(self, user):
        now = datetime.now()
        created_at = fake.date_time_between(start_date=now.replace(now.year - 2))
        task = Task.objects.create(
            name=fake.catch_phrase(),
            description=fake.paragraph(nb_sentences=random.randint(1, 5)),
            created_at=created_at,
            updated_at=fake.date_time_between(
                start_date=created_at, end_date=datetime.now()
            ),
            created_by_id=user.id,
            priority=random.randint(1, 4),
            is_completed=random.choice([True, False]),
            end_date=fake.date_time_between(start_date=created_at),
            start_date=created_at,
        )

    def create_data(self, total_users, total_tasks):
        for i in range(total_users):
            user = self.create_user()
            for j in range(random.randint(1, total_tasks)):
                self.create_task(user)
