from django.core.management.base import BaseCommand, CommandError

from toyshop.get_category_img import main


class Command(BaseCommand):
    help = 'Scrape category image.'

    def handle(self, *args, **options):
        try:
            main()
        except Exception as error:
            raise CommandError('Error happen while scrapping %s' % error)

        self.stdout.write(self.style.SUCCESS(
            'Successfully parsed category image.')
        )