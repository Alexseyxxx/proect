from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ClientForm
from .models import Client

@login_required
def profile_view(request):
    client, created = Client.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ClientForm(instance=client)

    return render(request, 'profile.html', {'form': form})


@login_required
def delete_profile(request):
    try:
        client = Client.objects.get(user=request.user)
    except Client.DoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')

    return render(request, 'delete_profile.html', {'client': client})

