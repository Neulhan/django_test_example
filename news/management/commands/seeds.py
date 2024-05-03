from django_seed import Seed
from django.core.management.base import BaseCommand
from news.models import News
from faker import Faker


class Command(BaseCommand):
    help = 'This command creates articles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number', default=1, type=int,
            help="How many articles do you want to create?")

    def handle(self, *args, **options):
        number = options.get('number')
        faker = Faker(locale=["ko_KR"])
        for _ in range(number):
            title = faker.bs()
            content = faker.catch_phrase()
            link = faker.uri()
            # Create Article instance with Korean data
            News.objects.create(title=title, content=content, link=link)
        self.stdout.write(self.style.SUCCESS(f'{number} articles created!'))
