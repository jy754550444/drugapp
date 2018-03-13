#-*-coding:utf-8-*-
from django import forms

__author__ = 'malxin'


class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u"ԭ����",
        error_messages={'required': u'������ԭ����'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"ԭ����",
                'rows': 1,
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"������",
        error_messages={'required': u'������������'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"������",
                'rows': 1,
            }
        ),
    )

    password1 = forms.CharField(
        required=True,
        label=u"ȷ������",
        error_messages={'required': u'���ٴ�����������'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"ȷ������",
                'rows': 1,
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"�����Ϊ������")
        elif self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError(u"��������������벻һ��")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data