from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        ## tabulka models.Task
        model = Task
        ## atributy, který budou ve formuláři
        fields = ['name', 'description', 'finished'] 
        #fields = '__all__'