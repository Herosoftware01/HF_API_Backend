from django.contrib import admin
from .models import Unit, Line,Cont_employee

admin.site.register(Unit)
admin.site.register(Line)
# admin.site.register(Cont_employee)
# admin.site.register(Mas_contractor)

from .models import Cont_employee, MasContract

@admin.register(Cont_employee)
class Cont_employeeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'con_id', 'get_contract_name')
    search_fields = ('name', 'code', 'con_id')
    readonly_fields = ('code',)  # Code is auto-generated in save(), so make it read-only in admin

    def get_form(self, request, obj=None, **kwargs):
        """
        Dynamically populate choices for contract_id using MasContract from the 'main' database.
        """
        form = super().get_form(request, obj, **kwargs)
        
        # Fetch all contracts from the 'main' database
        contracts = MasContract.objects.using('main').all().order_by('contract_id')
        
        # Create choices tuple: (contract_id, "ID - Description")
        choices = [('', '---------')] + [
            (c.contract_id, f"{c.contract_id} - {c.contract_des or 'No Description'}") 
            for c in contracts
        ]
        
        # Override the form field widget to be a ChoiceField/Select dropdown
        from django import forms
        form.base_fields['con_id'] = forms.ChoiceField(
            choices=choices,
            required=True,
            label="Contract"
        )
        return form

    @admin.display(description='Contractor Description')
    def get_contract_name(self, obj):
        """
        Fetch and display the contractor description from the 'main' database in the list view.
        """
        if not obj.con_id:
            return "-"
        try:
            contract = MasContract.objects.using('main').get(contract_id=obj.con_id)
            return contract.contract_des
        except MasContract.DoesNotExist:
            return "Unknown Contractor"