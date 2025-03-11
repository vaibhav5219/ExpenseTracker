from django.db import models
import uuid

class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True) # django admin me koi edit na kr payega - 'editable'
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now_add=True)
    

    class Meta:
        abstract = True

    def __str__(self):
        return self.uuid

class Transaction(BaseModel):
    description = models.CharField(max_length=255)
    amount = models.FloatField()

    class Meta:
        ordering = ('amount',)

    def isNegative(self):
        return self.amount < 0
