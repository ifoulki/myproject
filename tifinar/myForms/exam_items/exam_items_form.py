from django import forms
from tifinar.models import Examitems

class ExamItemForm(forms.ModelForm):
    class Meta:
        model = Examitems
        fields = ['exam_number', 'qst_1st_line', 'the_type', 'mark']
