from django.shortcuts import render, redirect
from .forms import SenderEmailForm

# Create your views here.
def add_sender_view(request):
    if request.method == "POST":
        form = SenderEmailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sender_success')
    else:
        form = SenderEmailForm()
        
    return render(request, 'mailer/add_sender.html', {'form':form})

def sender_success_view(request):
    return render(request, 'mailer/sender_success.html')
