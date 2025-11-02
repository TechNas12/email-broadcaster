from django import forms
from .models import Sender, EmailOperations


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


class EmailComposeForm(forms.Form):
    """Form for composing and sending emails. Returns data as a list."""
    
    recipient_email = forms.EmailField(
        label='Recipient Email Address',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'recipient@example.com'
        }),
        help_text='Enter the recipient\'s email address.'
    )
    
    subject = forms.CharField(
        label='Subject',
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email subject'
        }),
        help_text='Enter the subject line for your email.'
    )
    
    message = forms.CharField(
        label='Message',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message here...',
            'rows': 10
        }),
        help_text='Enter the email message content.'
    )
    
    def get_email_data_as_list(self):
        """
        Returns the form data as a list in the format:
        [recipient_email_address, subject, message]
        """
        if self.is_valid():
            return [
                self.cleaned_data['recipient_email'],
                self.cleaned_data['subject'],
                self.cleaned_data['message']
            ]
        return None
    
    def clean_recipient_email(self):
        """Validate recipient email address."""
        recipient_email = self.cleaned_data.get('recipient_email')
        if recipient_email:
            recipient_email = recipient_email.strip().lower()
        return recipient_email
    
    def clean_subject(self):
        """Validate and strip subject."""
        subject = self.cleaned_data.get('subject')
        if subject:
            subject = subject.strip()
        return subject


class EmailOperationsForm(forms.ModelForm):
    """Form for creating EmailOperations"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update widget classes to match template styling
        self.fields['sender'].widget.attrs.update({'class': 'form-control'})
        self.fields['recipient'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update({'class': 'form-control'})
    
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
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your message here...',
                'rows': 10
            }),
        }
        labels = {
            'sender': 'Select Sender',
            'recipient': 'Recipient Email',
            'subject': 'Subject',
            'message': 'Message',
        }
