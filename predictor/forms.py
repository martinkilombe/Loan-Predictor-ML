from django import forms

class LoanPredictionForm(forms.Form):
    Gender = forms.ChoiceField(
        choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female')],
        initial='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Married = forms.ChoiceField(
        choices=[('', 'Select Marital Status'), ('Yes', 'Yes'), ('No', 'No')],
        initial='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Dependents = forms.ChoiceField(
        choices=[('', 'Select Number of Dependents'), ('0', '0'), ('1', '1'), ('2', '2'), ('3+', '3 or more')],
        initial='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Education = forms.ChoiceField(
        choices=[('', 'Select Education Level'), ('Graduate', 'Graduate'), ('Not Graduate', 'Not Graduate')],
        initial='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Self_Employed = forms.ChoiceField(
        choices=[('', 'Select Employment Status'), ('Yes', 'Yes'), ('No', 'No')],
        initial='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    ApplicantIncome = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Applicant Income'})
    )
    CoapplicantIncome = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Coapplicant Income'})
    )
    LoanAmount = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Loan Amount'})
    )
    Loan_Amount_Term = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Loan Term in Months'})
    )
    Credit_History = forms.ChoiceField(
        choices=[('', 'Select Credit History'), (1, 'Good'), (0, 'Bad')],
        initial='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    Property_Area = forms.ChoiceField(
        choices=[('', 'Select Property Area'), ('Urban', 'Urban'), ('Semiurban', 'Semiurban'), ('Rural', 'Rural')],
        initial='',
        widget=forms.Select(attrs={'class': 'form-control'})
    )