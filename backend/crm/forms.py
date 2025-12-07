from django import forms
from .models import Contact, Deal, Interaction


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['company', 'contact_name', 'role', 'email', 'phone', 'source', 
                  'priority', 'status', 'notes']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'contact_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'role': forms.TextInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'source': forms.TextInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'priority': forms.Select(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}, choices=[('Low', 'Low'), ('Med', 'Medium'), ('High', 'High')]),
            'status': forms.Select(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}, choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Archived', 'Archived')]),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500', 'rows': 4}),
        }


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['contact', 'engagement', 'service', 'deal_stage', 'probability_pct',
                  'expected_close_date', 'deal_value_usd', 'retainer_usd', 'billing_frequency',
                  'next_action', 'next_action_due', 'last_contact_date', 'last_action', 'notes']
        widgets = {
            'contact': forms.Select(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'engagement': forms.TextInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'service': forms.TextInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'deal_stage': forms.Select(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}, choices=[
                ('Lead', 'Lead'), ('Qualified', 'Qualified'), ('Proposal', 'Proposal'),
                ('Negotiation', 'Negotiation'), ('Closed Won', 'Closed Won'), ('Closed Lost', 'Closed Lost')
            ]),
            'probability_pct': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500', 'min': 0, 'max': 100}),
            'expected_close_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500', 'type': 'date'}),
            'deal_value_usd': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500', 'step': '0.01'}),
            'retainer_usd': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500', 'step': '0.01'}),
            'billing_frequency': forms.Select(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}, choices=[
                ('', 'Select...'), ('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), 
                ('Annually', 'Annually'), ('One-time', 'One-time')
            ]),
            'next_action': forms.TextInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'next_action_due': forms.DateInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500', 'type': 'date'}),
            'last_contact_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500', 'type': 'date'}),
            'last_action': forms.TextInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500', 'rows': 4}),
        }


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['contact', 'interaction_type', 'direction', 'interaction_date', 'notes', 'outcome']
        widgets = {
            'contact': forms.Select(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
            'interaction_type': forms.Select(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}, choices=[
                ('Email', 'Email'), ('Call', 'Call'), ('Meeting', 'Meeting'),
                ('Demo', 'Demo'), ('Proposal', 'Proposal'), ('Other', 'Other')
            ]),
            'direction': forms.Select(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}, choices=[
                ('', 'Select...'), ('inbound', 'Inbound'), ('outbound', 'Outbound')
            ]),
            'interaction_date': forms.DateTimeInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500', 'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500', 'rows': 4}),
            'outcome': forms.TextInput(attrs={'class': 'w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500'}),
        }

