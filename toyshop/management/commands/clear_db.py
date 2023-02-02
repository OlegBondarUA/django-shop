from django.core.management.base import BaseCommand, CommandError
from toyshop.clear_db import main


class Command(BaseCommand):
    help = 'cleaning data'

    def handle(self, *args, **options):

        try:
            main()
            print('All tables in my database are empty')
        except Exception as error:
            raise CommandError('Error cleaning %s' % error)

        self.stdout.write(self.style.SUCCESS('Successfully cleaning'))
