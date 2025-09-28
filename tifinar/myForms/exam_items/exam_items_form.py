from django import forms
from tifinar.models import Examitems

class ExamItemForm(forms.ModelForm):
    # حقول الخيارات
    choice1_text = forms.CharField(required=False, max_length=500)
    choice1_correct = forms.ChoiceField(
        required=False,
        choices=[('', '----'), ('true', 'صحيح'), ('false', 'خطأ')]
    )
    choice2_text = forms.CharField(required=False, max_length=500)
    choice2_correct = forms.ChoiceField(
        required=False,
        choices=[('', '----'), ('true', 'صحيح'), ('false', 'خطأ')]
    )
    choice3_text = forms.CharField(required=False, max_length=500)
    choice3_correct = forms.ChoiceField(
        required=False,
        choices=[('', '----'), ('true', 'صحيح'), ('false', 'خطأ')]
    )
    
    class Meta:
        model = Examitems
        fields = [
            'exam_number', 'qsts_id', 'dir', 'mark', 'qst_1st_line', 'qsts',
            'the_type', 'correct_answer', 'qst_img', 'if_choising_correct',
            'img_if_right_answer', 'if_its_wrong_answer', 'img_if_wrong_answer'
        ]
        widgets = {
            'dir': forms.Select(choices=[('', 'اختر اللغة'), ('rtl', 'العربية'), ('ltr', 'Français'), ('ltr', 'English')]),
            'mark': forms.Select(),
            'the_type': forms.Select(choices=[
                ('', 'حدد الشكل'),
                ('radio', 'اختيارات (واحد فقط صحيح)'),
                ('checkbox', 'اختيارات (واحد أو أكثر صحيح)'),
                ('text', 'إجابة قصيرة'),
                ('textarea', 'إجابة طويلة')
            ]),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        the_type = cleaned_data.get('the_type')
        
        # التحقق من صحة الخيارات حسب نوع السؤال
        if the_type in ['radio', 'checkbox']:
            choice1_text = cleaned_data.get('choice1_text')
            choice2_text = cleaned_data.get('choice2_text')
            choice3_text = cleaned_data.get('choice3_text')
            
            if not choice1_text or not choice2_text:
                raise forms.ValidationError("يجب ملء الاختيارين الأول والثاني على الأقل")
        
        return cleaned_data