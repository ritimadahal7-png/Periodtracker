from django.db import models
from django.contrib.auth.models import User

class PeriodEntry(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    last_period_date = models.DateField()
    cycle_length = models.IntegerField(default=28)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.last_period_date}"