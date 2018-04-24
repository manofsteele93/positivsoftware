import datetime
import random

from django.contrib.auth import login, authenticate #Signup
from django.contrib.auth import models as auth_models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm #Signup
from django.contrib.auth.models import User #Signup
from django.contrib.sites.shortcuts import get_current_site #Signup
from django.utils.encoding import force_text, force_bytes #Signup
from django.utils.http import urlsafe_base64_encode #Signup
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.http import Http404
from django.template import loader
from django.template.loader import render_to_string #Signup
from django import forms
from django.utils import timezone

from . import models as mods
from .models import Response
from .forms import SignUpForm #Signup
from .tokens import account_activation_token #Signup



@login_required
def index(request):
    try:
        user = auth_models.User.objects.get(username = request.user)
        # recent_products = cmod.Product.objects.all()[:5]
    except (TypeError, ValueError, mods.Response.DoesNotExist):
        return HttpResponseRedirect('/goodday/today/')

    latest_response_list = Response.objects.filter(user=user).order_by('-pub_date')[:5] #.filter(user=request.user)
    template = loader.get_template('goodday/index.html')
    context = {
        'latest_response_list': latest_response_list,
    }
    return HttpResponse(template.render(context, request))

@login_required
def detail(request, response_id):
    try:
        user = auth_models.User.objects.get(username = request.user)
        # response = get_object_or_404(Response, pk=response_id)
        response = Response.objects.get(user=user, id=response_id)
        return render(request, 'goodday/detail.html', {'response': response})
        # recent_products = cmod.Product.objects.all()[:5]
    except (TypeError, ValueError, mods.Response.DoesNotExist):
        return HttpResponseRedirect('/goodday/today/')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/goodday/today/')
    else:
        form = SignUpForm()
    template = loader.get_template('goodday/signup.html')
    return HttpResponse(template.render({'form': form}, request))



@login_required
def today(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewResponseForm(request.POST)



        # check whether it's valid:
        if form.is_valid():

            response = form.save(commit=False)
            response.pub_date = timezone.now()
            response.user = request.user
            response.save()

            # process the data in form.cleaned_data as required
            #r = Response(response_text=request, pub_date = timezone.now())
            #r.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/goodday/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewResponseForm()
    template = loader.get_template('goodday/today.html')
    context = {
        'form': form,
    }
    return HttpResponse(template.render(context, request))

my_list = [
    'I helped someone.',
    'I passed my test!',
    'Mike gave me a compliment',
    'I heard my favorite song on the radio.',
    'We had cookies & ice cream.',
    'The skiing today was phenomenal.',
]







class NewResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ('response_text','public')
        label_suffix = ""
        #Select a random item from my_list above and use that as placeholder text
        secure_random = random.SystemRandom()
        random_placeholder = secure_random.choice(my_list)
        widgets = {
            'response_text': forms.TextInput(attrs={'placeholder': random_placeholder}),
        }

    def __init__(self, *args, **kwargs):
        super(NewResponseForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.label_suffix = "" #removes the : in the form
        self.fields['response_text'].label = "What went well today?"
        self.fields['response_text'].widget.attrs['cols'] = 10
        self.fields['response_text'].widget.attrs['rows'] = 20
        # self.fields['response_text'].initial = "I helped someone..."



def error_404(request):
    context = {}
    return render(request, 'goodday/error_404.html', context)

def error_500(request):
    context = {}
    return render(request, 'goodday/error_500.html', context)
#
#
# # A form for a new response
# class NewResponseForm(forms.Form):
#     response = forms.CharField(initial="I aced the test!", max_length=200,required=True)
#     def commit(self):
#         responses = mods.response()
#         responses.response_text = self.cleaned_data.get('response')
