from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from .forms import SenderEmailForm, EmailOperationsForm, AttachmentForm
from .models import Sender, EmailOperations, Attachment

# Create your views here.
def mailer_landing_view(request):
    """Mailer app landing page"""
    return render(request, 'mailer/landing.html')

def add_sender_view(request):
    if request.method == "POST":
        form = SenderEmailForm(request.POST)
        if form.is_valid():
            form.save()
            # If AJAX request or from modal, redirect to single recipient page
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'from_modal' in request.POST:
                messages.success(request, 'Sender added successfully!')
                return redirect('mailer:single_recipient_mailing')
            return redirect('sender_success')
    else:
        form = SenderEmailForm()
        
    return render(request, 'mailer/add_sender.html', {'form':form})

def sender_success_view(request):
    return render(request, 'mailer/sender_success.html')

def single_recipient_mailing_view(request):
    """View for single recipient mailing"""
    senders = Sender.objects.filter(is_active=True)
    
    if request.method == "POST":
        form = EmailOperationsForm(request.POST)
        if form.is_valid():
            email_op = form.save()
            
            # Send the email using sender's credentials
            try:
                sender = email_op.sender
                recipient = email_op.recipient
                subject = email_op.subject
                message_body = email_op.message
                
                # Get decrypted app password from the encrypted field
                app_password = sender.app_password
                
                # Create email message
                msg = MIMEMultipart()
                msg['From'] = sender.email
                msg['To'] = recipient
                msg['Subject'] = subject
                
                # Attach message body as HTML
                msg.attach(MIMEText(message_body, 'html'))
                
                # Handle file attachments
                attachment_files = request.FILES.getlist('file')
                attachment_count = 0
                
                for file in attachment_files:
                    if file:
                        try:
                            # Detect MIME type
                            content_type, encoding = mimetypes.guess_type(file.name)
                            if content_type is None or encoding is not None:
                                content_type = 'application/octet-stream'
                            
                            maintype, subtype = content_type.split('/', 1)
                            
                            # Attach file to email
                            part = MIMEBase(maintype, subtype)
                            part.set_payload(file.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {file.name}'
                            )
                            msg.attach(part)
                            
                            # Reset file pointer for saving to database
                            file.seek(0)
                            
                            # Save attachment to database
                            attachment = Attachment.objects.create(
                                email=email_op,
                                file=file
                            )
                            attachment_count += 1
                        except Exception as e:
                            messages.warning(request, f'Failed to attach file {file.name}: {str(e)}')
                
                # Create SMTP connection with sender's credentials
                connection = None
                try:
                    connection = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
                    connection.starttls()
                    connection.login(sender.email, app_password)
                    
                    # Send email
                    text = msg.as_string()
                    connection.sendmail(sender.email, recipient, text)
                    
                    # Success message
                    if attachment_count > 0:
                        messages.success(request, f'Email with {attachment_count} attachment(s) sent successfully to {recipient}!')
                    else:
                        messages.success(request, f'Email sent successfully to {recipient}!')
                finally:
                    # Always close the connection
                    if connection:
                        try:
                            connection.quit()
                        except:
                            connection.close()
            except smtplib.SMTPAuthenticationError as e:
                messages.error(request, f'Authentication failed. Please check the sender email and app password. Error: {str(e)}')
            except smtplib.SMTPException as e:
                messages.error(request, f'SMTP error occurred: {str(e)}')
            except Exception as e:
                messages.error(request, f'Failed to send email: {str(e)}')
            
            return redirect('mailer:single_recipient_mailing')
        else:
            # Form validation failed - show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = EmailOperationsForm()
    
    # Create attachment form for the template
    attachment_form = AttachmentForm()
    
    # Set sender queryset to only active senders
    if senders.exists():
        form.fields['sender'].queryset = senders
        if not form.is_bound:
            form.initial['sender'] = senders.first()
    
    context = {
        'form': form,
        'attachment_form': attachment_form,
        'senders': senders,
    }
    return render(request, 'mailer/single_recipient_mailing.html', context)

def update_sender_view(request, sender_id):
    """View for updating a sender"""
    sender = get_object_or_404(Sender, id=sender_id)
    if request.method == "POST":
        form = SenderEmailForm(request.POST, instance=sender)
        if form.is_valid():
            # Don't update password if it's empty (keep current encrypted password)
            if not form.cleaned_data.get('app_password'):
                form.instance.app_password = sender.app_password
            form.save()
            messages.success(request, 'Sender updated successfully!')
            return redirect('mailer:single_recipient_mailing')
    else:
        form = SenderEmailForm(instance=sender)
    
    # For AJAX requests, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        from django.http import JsonResponse
        return JsonResponse({
            'name': sender.name,
            'email': sender.email,
            'is_active': sender.is_active
        })
    
    return render(request, 'mailer/update_sender.html', {'form': form, 'sender': sender})

def get_sender_view(request, sender_id):
    """View to get sender data as JSON for modal"""
    from django.http import JsonResponse
    sender = get_object_or_404(Sender, id=sender_id)
    return JsonResponse({
        'name': sender.name,
        'email': sender.email,
        'is_active': sender.is_active
    })

def delete_sender_view(request, sender_id):
    """View for deleting a sender"""
    sender = get_object_or_404(Sender, id=sender_id)
    if request.method == "POST":
        sender.delete()
        messages.success(request, 'Sender deleted successfully!')
        return redirect('mailer:single_recipient_mailing')
    return render(request, 'mailer/delete_sender.html', {'sender': sender})
