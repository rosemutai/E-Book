from django import  forms
from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrower
        exclude = ['issue_date', 'return_date']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'

class RatingForm(forms.ModelForm):
    class Meta:
        model = Reviews
        exclude=['member','book']