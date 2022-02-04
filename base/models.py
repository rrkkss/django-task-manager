from django.db import models
from django.contrib.auth.models import User

## extend na integrovanou třídu User, kde přídávám atribut task
#class UserTask(models.Model):
    ## User je 1:1 s UserTask (extendnutej), smazáním Usera se smaže i UserTask
    #user = models.OneToOneField(User, on_delete=models.CASCADE)

    ## Task může mít několik uživatelů, na smazání Tasku dát na null
    #task = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True)

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
