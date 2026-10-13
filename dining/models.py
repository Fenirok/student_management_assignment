from django.db import models


class Restaurant(models.Model):
    class RestaurantType(models.TextChoices):
        ITALIAN = "Italian", "Italian"
        MEXICAN = "Mexican", "Mexican"
        OTHER = "Other", "Other"

    name = models.CharField(max_length=200)
    restaurant_type = models.CharField(
        max_length=20,
        choices=RestaurantType.choices,
    )
    date_opened = models.DateField()

    def __str__(self):
        return self.name


class Sale(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="sales",
    )
    income = models.DecimalField(max_digits=10, decimal_places=2)
    expenditure = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.restaurant}: {self.income} income"
