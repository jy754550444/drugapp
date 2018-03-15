# coding=utf-8
from django import forms
from django.contrib.admin import widgets

__author__ = 'malxin'


class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"原密码",
                'rows': 1,
                'class':'form-control'
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"新密码",
                'rows': 1,
                'class':'form-control'
            }
        ),
    )

    password1 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"确认密码",
                'rows': 1,
                'class':'form-control'
            }
        ),
    )

    # create_at = forms.DateTimeField(widget=widgets.AdminDateWidget(), label=u'时间')
    # create_at = forms.DateField(
    #     widget=forms.DateTimeInput(
    #         attrs={
    #             'type': 'date',
    #             'class':'form-control'
    #         }
    #     ),
    # )

    def clean(self):
        super().clean()
        if not self.is_valid():
            print("form errors")
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['password'] != self.cleaned_data['password1']:
            print("password errors")
            raise forms.ValidationError(u"两次输入的新密码不一样",code="pwd")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data