document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loanForm');
    const result = document.getElementById('result');
    const resultMessage = document.getElementById('resultMessage');
    const applicationDetails = document.getElementById('applicationDetails');
    const newPredictionBtn = document.getElementById('newPrediction');
    const progress = document.querySelector('.progress');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);
        
        fetch('/predict/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            // Update progress bar
            progress.style.width = '100%';

            // Display result
            resultMessage.textContent = data.message;
            resultMessage.style.color = data.result === 'Approved' ? 'green' : 'red';

            // Display application details
            applicationDetails.innerHTML = `
                <h3>Application Details:</h3>
                <ul>
                    ${Object.entries(data.form_data).map(([key, value]) => `<li><strong>${key}:</strong> ${value}</li>`).join('')}
                </ul>
            `;

            form.classList.add('hidden');
            result.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing your request.');
        });
    });

    newPredictionBtn.addEventListener('click', function() {
        form.reset();
        form.classList.remove('hidden');
        result.classList.add('hidden');
        progress.style.width = '0';
    });

    // Update progress bar as user fills out the form
    form.addEventListener('input', function() {
        const inputs = form.querySelectorAll('input, select');
        const filledInputs = Array.from(inputs).filter(input => input.value !== '').length;
        const progressPercentage = (filledInputs / inputs.length) * 100;
        progress.style.width = `${progressPercentage}%`;
    });
});