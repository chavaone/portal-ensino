# profes/views.py
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import FormCreacionProfe, FormDatosProfe, FormEliminarProfe
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.views import generic
from .models import Profe


class ModificarDatosProfe (generic.UpdateView):
    model=Profe
    form_class = FormDatosProfe
    template_name = 'account_edit.html'
    success_url = reverse_lazy('edit_profe_data')

    #get object
    def get_object(self, queryset=None):
        return self.request.user

def eliminar_profe (request):
    if request.method == 'POST':
        form = FormEliminarProfe(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.delete()
            reverse('delete_profe_done')
            return HttpResponseRedirect(reverse('delete_profe_done'))
    else:
        form = FormEliminarProfe()
    return render(request, 'profe_confirm_delete.html', {'form': form})


def signup (request):
    if request.method == 'POST':
        form = FormCreacionProfe(request.POST)
        if form.is_valid():
            #Register user with form data.
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            #Create email and send it.
            email_subject = '' #TODO
            email_message = render_to_string('account_activation_email.html',
                {
                    'user': user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                })
            email_to = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, email_message, to=[email_to])
            email.send()

            #Render response page.
            return render(request, 'account_activation_done.html')
    else:
        form = FormCreacionProfe()
    return render(request, 'signup.html', {'form': form})

def activate (request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Profe.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Profe.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

    return render(request, 'account_activation_complete.html', {'user': user})
