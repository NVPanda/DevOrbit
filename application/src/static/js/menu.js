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


document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-button');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.getAttribute('data-id');
            
            fetch(`posts/${postId}/like`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.likes !== undefined) {
                    // Atualizar o número de likes no frontend
                    const likeCountElement = document.getElementById(`like-count-${postId}`);
                    if (likeCountElement) {
                        likeCountElement.textContent = `${data.likes} Likes`;
                    }
                } else {
                    console.error('Erro: o campo "likes" não foi encontrado na resposta:', data);
                }
            })
            .catch(error => console.error('Erro ao curtir o post:', error));
        });
    });
});

const meubtn = document.getElementByid('meubtn')

meubtn.addEventListener('click',function(){
    console.log('BTN foi clicado!');
})

function mybar() {
    var x = document.getElementById("cta-button-sidebar");
    if (x.classList.contains("-translate-x-full")) {
      x.classList.remove("-translate-x-full");
    } else {
      x.classList.add("-translate-x-full");
    }
  }
  