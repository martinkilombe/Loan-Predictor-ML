from django.shortcuts import render
from .forms import LoanPredictionForm
from .ml_model import predict_loan

def predict(request):
    if request.method == 'POST':
        form = LoanPredictionForm(request.POST)
        if form.is_valid():
            # Check if any dropdown field is empty
            for field in ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Credit_History', 'Property_Area']:
                if form.cleaned_data[field] == '':
                    form.add_error(field, 'Please select an option')
            
            if not form.errors:
                # Process the form data and make prediction
                features = [
                    form.cleaned_data['ApplicantIncome'],
                    form.cleaned_data['CoapplicantIncome'],
                    form.cleaned_data['LoanAmount'],
                    form.cleaned_data['Loan_Amount_Term'],
                    form.cleaned_data['Credit_History'],
                    form.cleaned_data['Gender'],
                    form.cleaned_data['Married'],
                    form.cleaned_data['Dependents'],
                    form.cleaned_data['Education'],
                    form.cleaned_data['Self_Employed'],
                    form.cleaned_data['Property_Area'],
                ]
                
                try:
                    prediction = predict_loan(features)
                    
                    # Interpret the prediction
                    if prediction == 1:
                        result = "Approved"
                        message = "Congratulations! Your loan is likely to be approved."
                    else:
                        result = "Denied"
                        message = "We're sorry, but your loan is likely to be denied."
                    
                    context = {
                        'result': result,
                        'message': message,
                        'form_data': form.cleaned_data  # Include form data for display
                    }
                    return render(request, 'predictor/result.html', context)
                
                except Exception as e:
                    # Handle any errors during prediction
                    form.add_error(None, f"An error occurred during prediction: {str(e)}")
    else:
        form = LoanPredictionForm()
    
    return render(request, 'predictor/predict.html', {'form': form})