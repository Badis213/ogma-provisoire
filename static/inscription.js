const form = document.getElementById('registration-form');
const errorMessage = document.getElementById('error-message');
const popup = document.getElementById('popup');
const closePopupButton = document.getElementById('close-popup');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const data = {
        nom: formData.get('nom'),
        prenom: formData.get('prenom'),
        email: formData.get('email'),
        password: formData.get('password')
    };

    try {
        const response = await fetch('/register', {
            method: 'POST',
            body: new URLSearchParams(data),
        });

        if (response.ok) {
            // Si l'inscription réussie, afficher la boîte modale
            popup.style.display = 'flex'; // Afficher la modale
        } else {
            const result = await response.json();
            errorMessage.textContent = result.message || 'Une erreur est survenue';
        }
    } catch (error) {
        errorMessage.textContent = 'Erreur de connexion au serveur. Veuillez réessayer plus tard.';
    }
});

// Fermer la boîte modale lorsque l'utilisateur clique sur le bouton "Fermer"
closePopupButton.addEventListener('click', () => {
    popup.style.display = 'none'; // Masquer la modale
});
