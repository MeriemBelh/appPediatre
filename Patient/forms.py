from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import NumericPasswordValidator
from django.contrib.auth import get_user_model
User = get_user_model()

class PasswordChangingForm(PasswordChangeForm):
    error_css_class = 'error-field'
    old_password = forms.CharField(label='Ancien mot de passe',
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Ancien mot de passe',
                                              'id': 'old_password_field','data_input': '#old_password_field',})

                                   )
    new_password1 = forms.CharField(label='Nouveau mot de passe',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': 'Nouveau mot de passe',
                                               'id': 'new_password1_field','data_input': '#new_password1_field'})
                                    )
    new_password2 = forms.CharField(label='Confirmer le nouveau mot de passe',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                      'placeholder': 'Confirmer le nouveau mot de passe',
                                                                      'id': 'new_password2_field','data_input': '#new_password2_field'})
                                    )

    # error_messages = {
    #     'password_too_common': _("Ce mot de passe est trop courant."),
    #     'password_incorrect': _('Votre ancien mot de passe a été mal saisi. Veuillez le saisir à nouveau.'),
    #     'password_mismatch': _('Les deux champs du nouveau mot de passe ne correspondent pas.'),
    #     'password_too_short': _('Ce mot de passe est trop court. Il doit contenir au moins 8 caractères.'),
    #     'password_entirely_numeric': _("Ce mot de passe ne peut pas être entièrement numérique."),
    #
    # }

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

    # def __init__(self, *args, **kwargs):
    #     super(PasswordChangeForm, self).__init__(*args, **kwargs)
    #     self.error_messages.update(self.error_messages)
