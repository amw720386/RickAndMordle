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
