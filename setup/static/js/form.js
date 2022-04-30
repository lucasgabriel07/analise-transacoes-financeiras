const input = document.getElementById('upload')
const label = document.getElementById('filename')
const message = document.querySelector('.form-message')

input.oninput = () => {
    const file = input.files[0]

    if (file.name.endsWith('.csv')) {
        label.innerText = file.name
        message.style.color = 'green'
        message.innerText = 'Arquivo carregado.'
        message.style.display = 'block'
    } else {
        input.value = null
        label.innerText = 'Nenhum arquivo escolhido'
        message.style.color = 'red'
        message.innerText = 'Arquivo inválido. O arquivo deve ser do tipo csv.'
        message.style.display = 'block'
    }
}