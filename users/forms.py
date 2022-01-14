from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model   = CustomUser
        #会員登録時、メールの入力を必須化。
        fields  = [ "username","email" ]

