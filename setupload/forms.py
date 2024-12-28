from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class CsvUploadForm(forms.Form):
    csv_files = MultipleFileField(label='Vocab Set:')
    number_input = forms.IntegerField(label='Question Quantity')


class CsvPasteForm(forms.Form):
    csv_text = forms.CharField(label='Vocab Set:', widget=forms.Textarea(attrs={"rows": "5"}))
    number_input = forms.IntegerField(label='Question Quantity')
