from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from django.db.models import F, Q

from dining.models import Restaurant, Sale


class Command(BaseCommand):
    help = "Demonstrate Q object, text, and regex filters for dining data."

    def handle(self, *args, **options):
        cutoff = timezone.localdate() - timedelta(days=30)

        italian_mexican_q = Q(restaurant_type__in=["Italian", "Mexican"])
        recently_opened_q = Q(date_opened__gte=cutoff)
        not_recently_opened_q = ~recently_opened_q
        name_has_digit_q = Q(name__regex=r"[0-9]+")
        profitable_q = Q(income__gt=F("expenditure"))
        restaurant_name_has_digit_q = Q(restaurant__name__regex=r"[0-9]+")
        profitable_or_named_with_digit_q = profitable_q | restaurant_name_has_digit_q

        self.show("Italian OR Mexican", Restaurant.objects.filter(italian_mexican_q))
        self.show(
            f"NOT opened in the last 30 days (before {cutoff})",
            Restaurant.objects.filter(not_recently_opened_q),
        )
        self.show(
            "Italian/Mexican OR opened in the last 30 days",
            Restaurant.objects.filter(italian_mexican_q | recently_opened_q),
        )
        self.show(
            'Name contains "grill" (case-insensitive)',
            Restaurant.objects.filter(name__icontains="grill"),
        )
        self.show(
            'Name ends with "Cafe"',
            Restaurant.objects.filter(name__endswith="Cafe"),
        )
        self.show(
            "Name contains one or more digits",
            Restaurant.objects.filter(name_has_digit_q),
        )
        self.show(
            "Profitable sale OR restaurant name contains a digit",
            Sale.objects.filter(profitable_or_named_with_digit_q).select_related(
                "restaurant"
            ),
        )

    def show(self, label, queryset):
        self.stdout.write(f"\n=== {label} ===")
        with CaptureQueriesContext(connection) as captured:
            results = list(queryset)
        self.stdout.write(f"Results: {results!r}")
        for query in captured.captured_queries:
            self.stdout.write(f"SQL: {query['sql']}")


