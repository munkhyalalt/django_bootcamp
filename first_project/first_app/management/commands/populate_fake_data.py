from django.core.management.base import BaseCommand, CommandError
import random

from first_app.models import AccessRecord, Webpage, Topic

from faker import Faker

fakegen = Faker()
topics = ['Search', 'Social', 'Market place', 'News', 'Games']


class Command(BaseCommand):
    help = 'Populates fake data to first_app'

    def add_arguments(self, parser):
        parser.add_argument('topic_count', type=int)

    def handle(self, *args, **options):
        self.stdout.write("clearing data...")

        # clearing data
        AccessRecord.objects.all().delete()
        Webpage.objects.all().delete()

        self.stdout.write("populating script...")
        for entry in range(options['topic_count']):
            # get topic for entry
            topic = Topic.objects.get(pk=random.randrange(1, 5))

            # create a fake data for it
            fake_url = fakegen.url()
            fake_date = fakegen.date()
            fake_name = fakegen.company()

            # create new webpage entry

            webpg = Webpage.objects.get_or_create(topic=topic, url=fake_url, name=fake_name)[0]

            # create fake access record

            AccessRecord.objects.get_or_create(name=webpg, date=fake_date)

        self.stdout.write("fake populate finish...")
