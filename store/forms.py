from django import forms

# Custom Multile File Input Class
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


# Custom Multile File Field Class
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ContactForm(forms.Form):
	fname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
	lname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}), required=False)
	email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
	message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message', 'class': 'form-control', 'rows': 4}))