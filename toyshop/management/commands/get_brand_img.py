from django.core.management.base import BaseCommand, CommandError

from toyshop.get_brand_img import main


class Command(BaseCommand):
    help = 'Scrape brand image.'

    def handle(self, *args, **options):
        try:
            main()
        except Exception as error:
            raise CommandError('Error happen while scrapping %s' % error)

        self.stdout.write(self.style.SUCCESS(
            'Successfully parsed brand image.')
        )