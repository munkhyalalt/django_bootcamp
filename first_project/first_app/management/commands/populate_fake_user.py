from django.core.management.base import BaseCommand, CommandError

from first_app.models import UserProfileInfo

from faker import Faker

fakegen = Faker()


class Command(BaseCommand):
    help = 'Populates fake data to first_app'

    def add_arguments(self, parser):
        parser.add_argument('user_count', type=int)

    def handle(self, *args, **options):
        self.stdout.write("clearing users....")

        # delete existing users
        UserProfileInfo.objects.all().delete()
        self.stdout.write("populating script...")
        for entry in range(options['user_count']):
            # create a fake data for it
            fakename = fakegen.name()
            first_name = fakename.split()[0]
            last_name = fakename.split()[1]
            email = fakegen.email()

            # create new webpage entry
            UserProfileInfo.objects.get_or_create(first_name=first_name, last_name=last_name, email=email)
        self.stdout.write("fake populate finish...")
