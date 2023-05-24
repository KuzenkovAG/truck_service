import csv

from django.core.management.base import BaseCommand

from loads import models


class Command(BaseCommand):
    help = "Import locations in db."

    def handle(self, *args, **options):

        files = [
            (models.Location, 'static/data/uszips.csv'),
        ]

        for model, file in files:
            object_model = model.objects.all()
            object_model.delete()
            rows_csv = []
            with open(file, encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                i = 0
                for row in reader:
                    i += 1
                    row_csv = model(
                        id=i,
                        city=row['city'],
                        state=row['state_name'],
                        zip=row['zip'],
                        latitude=row['lat'],
                        longitude=row['lng'],
                    )
                    rows_csv.append(row_csv)

            created_objects = model.objects.bulk_create(rows_csv)
            created_count = len(created_objects)
            self.stdout.write(
                self.style.SUCCESS(
                    f'({model}) Создано записей: {created_count}'
                )
            )
