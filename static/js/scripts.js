document.addEventListener('DOMContentLoaded', function() {
    var cards = document.querySelectorAll('.flip-card');
    
    cards.forEach(function(card) {
        card.addEventListener('click', function() {
            if (!this.classList.contains('flipped')) {
                this.classList.add('flipped');
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var guessInput = document.getElementById('guess-input');
    var suggestionsBox = document.getElementById('suggestions');
    var submitButton = document.getElementById('submit-guess');
    var characterName = document.getElementById('character-name');
    var validNames = []; 

    fetch('/static/data/names_noDupes.txt')
        .then(response => response.text())
        .then(data => {
            validNames = data.split('\n').map(name => name.trim()).filter(name => name !== '-');

            guessInput.addEventListener('input', function() {
                var query = this.value.toLowerCase();
                suggestionsBox.innerHTML = ''; 
                submitButton.disabled = true; 

                if (query) {
                    var filteredNames = validNames.filter(name => name.toLowerCase().includes(query));

                    filteredNames.forEach(function(name) {
                        var suggestionItem = document.createElement('div');
                        suggestionItem.className = 'suggestion-item';
                        suggestionItem.textContent = name;

                        suggestionItem.addEventListener('click', function() {
                            guessInput.value = name;
                            suggestionsBox.innerHTML = ''; 
                            submitButton.disabled = false;  
                        });

                        suggestionsBox.appendChild(suggestionItem);
                    });

                    if (filteredNames.includes(guessInput.value)) {
                        submitButton.disabled = false;
                    }
                }
            });
        });

    submitButton.addEventListener('click', function() {
        if (!this.disabled) {
            fetch('/check_guess', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ guess: guessInput.value, character: characterName })
            })
            .then(response => response.json())
            .then(data => {
                if (data.result === 'correct') {
                    alert('Correct guess!');
                } else {
                    alert('Incorrect guess. Try again!');
                }
            });
        }
    });

    guessInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !submitButton.disabled) {
            submitButton.click();  
        }
    });

    document.addEventListener('click', function(event) {
        if (!suggestionsBox.contains(event.target) && event.target !== guessInput) {
            suggestionsBox.innerHTML = ''; 
        }
    });
});
