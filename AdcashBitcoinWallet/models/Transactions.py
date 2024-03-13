from django.db import models
from django.utils import timezone
import uuid

class Transactions(models.Model):
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=15, decimal_places=8)
    spent = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.transaction_id

    def save(self, *args, **kwargs):
        self.transaction_id = uuid.uuid4().hex
        super(Transactions, self).save(*args, **kwargs)

    class Meta:
        db_table = 'Transactions'