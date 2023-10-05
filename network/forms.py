from django import forms

class PostForm(forms.Form):
    post_content = forms.CharField(widget=forms.Textarea(attrs={
                                        "rows":"4", "cols":"90", 
                                        'placeholder':'What is in your mind?',
                                        'class':'form-control'}), label="")
