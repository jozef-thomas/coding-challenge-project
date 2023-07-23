from django import forms

class RegistrationForm(forms.Form):
   prereg_name = forms.CharField(label = 'Name',max_length=50)
   prereg_email = forms.EmailField(label = 'Email',max_length=50)
   prereg_mob = forms.CharField(label = "Mobile No",max_length=10)
   districtd = forms.ChoiceField(label = 'District(Please Select the District of your Institution)',choices=[('1','Kottayam'),('2','Alappuzha')])