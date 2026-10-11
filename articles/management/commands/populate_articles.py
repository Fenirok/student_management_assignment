from django.core.management.base import BaseCommand

from articles.models import Article


class Command(BaseCommand):
    help = "Create sample articles for pagination testing."

    def handle(self, *args, **options):
        articles = []

        for number in range(1, 61):
            articles.append(
                Article(
                    title=f"Sample Article {number}",
                    content=f"This is the content of sample article {number}.",
                    author=f"Author {(number % 5) + 1}",
                    is_published=(number % 4 != 0),
                )
            )

        Article.objects.bulk_create(articles)

        self.stdout.write(
            self.style.SUCCESS(f"Created {len(articles)} articles.")
        )