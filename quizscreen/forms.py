from django import forms


class QuizResponseForm(forms.Form):
    def __init__(self, *args, words=None, **kwargs):
        super().__init__(*args, **kwargs)
        if words:
            for index, word in enumerate(words, start=1):
                self.fields[f'responses_{index}'] = forms.CharField(
                    label=f"Response for {word}",
                    required=False,
                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': f'Your answer for "{word}"'})
                )
