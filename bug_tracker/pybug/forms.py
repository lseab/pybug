from django import forms
from .models import Comment, Ticket


class TicketForm(forms.ModelForm):

    title = forms.CharField(label=False, widget=forms.TextInput(
        attrs={
            'rows': 1,
            'style': 'font-size: xx-large; border: none;',            
            }
    ))

    description = forms.CharField(label=False, widget=forms.Textarea(
        attrs={
            'placeholder': 'Add a description...',
            'rows': 4,
            'style': 'border: none;',     
            }
    ))

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'reporter', 'assignee', 'priority']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        return super().save(commit=commit)


class CommentForm(forms.Form):

    comment_content = forms.CharField(label=False, widget=forms.Textarea(
        attrs={
            'placeholder': 'Add a comment...',
            'rows': 1,
            'verbose_name': "",
            }
    ))