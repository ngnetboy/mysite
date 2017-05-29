# -*- coding: utf-8 -*-
from django import forms
from models import Comment



class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)  #默认的 HTML 代码为 <input type="text">
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea) #每一个field都有一个默认的widget，可以使用widget重新定义

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email', 'body')
