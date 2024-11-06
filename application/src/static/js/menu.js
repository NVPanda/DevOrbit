fetch('/Codechamber/feed/posts', {
    method: 'POST',
    body: formData,
})
.then(response => {
    console.log(response);  // Verifique a resposta da API
    return response.json(); // Aqui tenta-se interpretar a resposta como JSON
})
.then(data => {
    if (data.id) {
        alert('Post criado com sucesso!');
    } else {
        alert('Falha ao criar post.');
    }
})
.catch(error => {
    console.error('Erro na requisição:', error);
    alert('Erro na requisição: ' + error);
});
