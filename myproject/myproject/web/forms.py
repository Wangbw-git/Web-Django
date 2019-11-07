#encoding: utf-8

from django import forms

class RegisterForm(forms.Form):
    # 1. 定义好以下字段，必须要传递的。这是第一层验证
    username = forms.CharField(max_length=100,min_length=1,required=True)
    name = forms.CharField(max_length=100,min_length=1,required=True)
    password = forms.CharField(max_length=20,min_length=6,required=True)
    repassword = forms.CharField(max_length=20,min_length=6,required=True)
    sex = forms.IntegerField(required=True,max_value=1,min_value=0)

    # 2. 重写clean方法，手动设置一些验证逻辑
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        repassword = cleaned_data.get('repassword')
        if password != repassword:
            # 如果两次密码不相等，那么就要验证失败。抛出异常。
            raise forms.ValidationError("两次密码不一致！")
        # 如果两次密码一致，说明数据正常，直接返回cleaned_data
        return cleaned_data