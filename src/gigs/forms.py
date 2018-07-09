from django import forms
from django.utils.timezone import now

from gigs.models import Gig, GigType, GigLocation

class NewGigForm(forms.ModelForm):
    class Meta:
        model = Gig
        fields = ('title','description','tokenvalue')
        exclude = ('poster','is_paid','is_active')

    def __init__(self,poster,*args, **kwargs):
        self.poster = poster
        super(NewGigForm,self).__init__(*args, **kwargs)
        

    def save(self,commit=True):
        gig = super(NewGigForm,self).save(commit=False)
        gig.title = self.cleaned_data['title']
        gig.description = self.cleaned_data['description']
        gig.tokenvalue = self.cleaned_data['tokenvalue']
        gig.date_posted = now()
        gig.is_paid = False
        gig.is_active = True
        gig.poster = self.poster
        if commit:
            gig.save()
        return gig

class NewGigLocationForm(forms.ModelForm):
    
    class Meta:
        model = GigLocation
        fields = ('address1','address2',
                  'city','zipcode',
                  'contact_first_name',
                  'contact_last_name',
                  'contact_phone')
        exclude = ('gig',)

    def __init__(self,gig,*args, **kwargs):
        self.gig = gig
        super(NewGigLocationForm,self).__init__(*args, **kwargs)

    def save(self,commit=True):
        gig_loc = super(NewGigLocationForm,self).save(commit=False)
        gig_loc.address1 = self.cleaned_data['address1']
        gig_loc.address2 = self.cleaned_data['address2']
        gig_loc.city = self.cleaned_data['city']
        gig_loc.zipcode = self.cleaned_data['zipcode']
        gig_loc.contact_first_name = self.cleaned_data['contact_first_name']
        gig_loc.contact_last_name = self.cleaned_data['contact_last_name']
        gig_loc.contact_phone = self.cleaned_data['contact_phone']
        gig_loc.gig = self.gig
        if commit:
            gig_loc.save()
        return gig_loc

class NewGigTypeForm(forms.ModelForm):

    class Meta:
        model = GigType
        fields = '__all__'
        exclude = ('gig',)

    def __init__(self,gig,*args, **kwargs):
        self.gig = gig
        super(NewGigTypeForm,self).__init__(*args, **kwargs)

    def save(self,commit=True):
        gig_type = super(NewGigTypeForm,self).save(commit=False)
        gig_type.gig = self.gig
        gig_type.science = self.cleaned_data['science']
        gig_type.technology = self.cleaned_data['technology']
        gig_type.engineering =  self.cleaned_data['engineering']
        gig_type.arts = self.cleaned_data['arts']
        gig_type.music = self.cleaned_data['music']
        gig_type.business = self.cleaned_data['business']
        gig_type.hospitality = self.cleaned_data['hospitality']
        gig_type.marketing = self.cleaned_data['marketing']

        if commit:
            gig_type.save()
        return gig_type