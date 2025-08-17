from rest_framework import serializers
from .models import comments  # تأكد أن النموذج مستورد بشكل صحيح

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comments
        fields = '__all__'  # أو حدد الحقول يدويًا ['id', 'text', ...]