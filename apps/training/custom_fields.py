from django import forms

class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass

class MultipleChoiceFieldNoValidation(forms.MultipleChoiceField):
    def validate(self, value):
        pass
