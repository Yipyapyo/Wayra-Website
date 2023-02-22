from django import forms
from django.contrib.auth.models import Group, User, Permission

class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')
    name = forms.CharField(label='Group Name', max_length=100)
    permissions = forms.ModelMultipleChoiceField(
        label='Permissions',
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    # KEEP BELOW FOR NOW IN CASE CODES ABOVE DO NOT WORK
    # name = forms.CharField()
    # CHOICES = [
    #     ("portfolio.add_user", "Create user"),
    #     ("portfolio.change_user", "Edit user"),
    #     ("portfolio.delete_user", "Delete user"),
    #     ("portfolio.view_user", "View user"),
        
    #     ("portfolio.add_company", "Create company"),
    #     ("portfolio.change_company", "Edit company"),
    #     ("portfolio.delete_company", "Delete company"),
    #     ("portfolio.view_", "View company"),
        
    #     ("portfolio.add_individual", "Create individual"),
    #     ("portfolio.change_individual", "Edit individual"),
    #     ("portfolio.delete_individual", "Delete individual"),
    #     ("portfolio.view_individual", "View individual"),
        
    #     ("portfolio.add_residentialaddress", "Create residential address"),
    #     ("portfolio.change_residentialaddress", "Edit residential address"),
    #     ("portfolio.delete_residentialaddress", "Delete residential address"),
    #     ("portfolio.view_residentialaddress", "View residential address")
    # ]
    # permissions = forms.MultipleChoiceField(label = "Permissions", choices = CHOICES, widget=forms.CheckboxSelectMultiple())
    
    # def save(self):
    #     new_group, created = Group.objects.get_or_create(name=self.cleaned_data.get("name"))
        
    