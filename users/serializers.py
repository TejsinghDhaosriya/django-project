from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from .models import User
from django.views.decorators.csrf import csrf_exempt


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
#        field=('email','username','password','is_student','is_teacher')
        fields='__all__'
class CustomRegisterSerializer(RegisterSerializer):
    is_student =serializers.BooleanField()
    is_teacher =serializers.BooleanField()
    class Meta:
        model=User
        field=('email','username','password','is_student','is_teacher')
    
    
    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'is_student': self.validated_data.get('is_student', ''),
            'is_teacher': self.validated_data.get('is_teacher', '')
        }
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.is_student =self.cleaned_data.get('is_student')
        user.is_teacher =self.cleaned_data.get('is_teacher')
        user.save()
        adapter.save_user(request, user, self)
        return user
    
    
 