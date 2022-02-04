from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    ## uživatel může mít několik tasků, při smazání uživatele (User -> UserTask) se mažou i Tasky
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, null=True, blank=True)
    finished = models.BooleanField(default=False)

    ## případně pro extra časový seřazení
    #created = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True)
    
    ## pevně dané pořadí, jinak by se musel seřadit query set
    class Meta:
        ordering = ['finished'] ## nejdřív nedokončený, obráceně -finished

    def __str__(self):
        return self.name
