
from django import forms


class AnalysisForm(forms.Form):
    data = forms.CharField(label='data', max_length=100)


class TagsForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)

    def __init__(self, *args, **kwargs):

        choices = kwargs.pop('choices')
        choices = [i for i in choices]
        parsed = tuple((data['_id'], data['_id']) for data in choices[0:len(choices)-1])

        super(TagsForm, self).__init__(*args,**kwargs)
        self.fields['collection'] = forms.ChoiceField(choices=parsed)