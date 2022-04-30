const removeButtons = document.querySelectorAll('.remove-button')

removeButtons.forEach(button => {
    button.addEventListener('click', () => {
        if (confirm('Tem certeza?')) {
            window.location.href = button.dataset.href
        }
    })
})