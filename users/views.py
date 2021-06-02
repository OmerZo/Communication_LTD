from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm, CustomerCreateForm
from .models import Profile, Customer


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            phone = profile_form.cleaned_data.get('phone')
            data_plan = profile_form.cleaned_data.get('data_plan')
            profile = Profile.objects.create(user=user, phone=phone, data_plan=data_plan)
            profile.save()

            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('products-home')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def profile(requests):
    return render(requests, 'users/profile.html')


def customer_create_view(request):
    form = CustomerCreateForm()
    if request.method == 'POST':
        form = CustomerCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer')
    context = {
        'form': form
    }
    return render(request, "users/customer_create.html", context)


def customer_detail_view(request):
    obj = Customer.objects.filter().order_by('-id')[0]
    context = {
        'Name': obj.Name,
        'Email': obj.Email
    }
    return render(request, "users/customer_detail.html", context)
