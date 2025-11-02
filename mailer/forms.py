from django import forms
from .models import Sender, EmailOperations, Attachment
from tinymce.widgets import TinyMCE


class MultipleFileInput(forms.FileInput):
    """Custom FileInput widget that supports multiple file uploads"""
    def __init__(self, attrs=None):
        default_attrs = {}
        if attrs:
            default_attrs.update(attrs)
        # Remove multiple from attrs to avoid Django's validation error
        default_attrs.pop('multiple', None)
        super().__init__(attrs=default_attrs)
    
    def build_attrs(self, base_attrs, extra_attrs=None):
        """Add multiple attribute to the final HTML attributes"""
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs['multiple'] = True
        return attrs


class SenderEmailForm(forms.ModelForm):
    """Form for creating and updating Sender email accounts."""
    
    class Meta:
        model = Sender
        fields = ['name', 'email', 'app_password', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sender name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com'
            }),
            'app_password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter app password (16 characters)'
            })
            
        }
        labels = {
            'name': 'Sender Name',
            'email': 'Email Address',
            'app_password': 'App Password',
            'is_active': 'Active'
        }
        help_texts = {
            'app_password': 'Enter the application-specific password for this email account.',
            'is_active': 'Uncheck to disable this sender account without deleting it.'
        }

class EmailOperationsForm(forms.ModelForm):
    """Form for creating EmailOperations"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update widget classes to match template styling
        # Don't update message field as it uses TinyMCE widget
        self.fields['sender'].widget.attrs.update({'class': 'form-control'})
        self.fields['recipient'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
    
    class Meta:
        model = EmailOperations
        fields = ['sender', 'recipient', 'subject', 'message']
        widgets = {
            'sender': forms.Select(attrs={
                'class': 'form-control',
            }),
            'recipient': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'recipient@example.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email subject'
            }),
            'message': TinyMCE(attrs={
                'cols': 80,
                'rows': 20,
                'class': 'form-control',
            }),
        }
        labels = {
            'sender': 'Select Sender',
            'recipient': 'Recipient Email',
            'subject': 'Subject',
            'message': 'Message',
        }

class AttachmentForm(forms.ModelForm):
    """Form for uploading file attachments"""
    file = forms.FileField(
        widget=MultipleFileInput(attrs={
            'class': 'form-control-file'
        }),
        required=False,
        label="Attach Files"
    )

    class Meta:
        model = Attachment
        fields = ['file']