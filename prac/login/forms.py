from django import forms

class AttendForm(forms.Form):
	"""docstring for NameForm"""
	regid = forms.CharField( label="",max_length=10,widget=forms.TextInput(attrs={'class' : 'regid','placeholder':'Enter ERP Registration number', 'label':''}))
	passw = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class' : 'passw', 'placeholder' : 'Enter ERP Password', 'label' : ''}), max_length=64)
	mood_reg = forms.CharField(label="" , max_length=10, widget=forms.TextInput(attrs={'class' : 'moodreg', 'placeholder' : 'Enter Moodle Registration number', 'label':''}))
	mood_passw = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class' : 'moodpassw', 'placeholder' : 'Enter Moodle Password', 'label' : ''}), max_length=64)
