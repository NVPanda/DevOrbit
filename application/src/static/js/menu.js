// document.addEventListener('DOMContentLoaded', () => {
//   const formElement = document.getElementById('post-form');

//   if (formElement) {
//     formElement.addEventListener('submit', (event) => {
//       event.preventDefault();

//       const formData = new FormData(formElement);

//       // Verificar se todos os campos necessários estão presentes
//       if (!formData.has('user_id') || !formData.has('nome') || !formData.has('titulo') || !formData.has('post')) {
//         alert('Por favor, preencha todos os campos obrigatórios!');
//         return;
//       }

//       // Log para verificar os dados do formulário
//       for (let [key, value] of formData.entries()) {
//         console.log(`${key}: ${value}`);
//       }

//       fetch('https://api-devorbirt.onrender.com/post/', {
//         method: 'POST',
//         body: formData,
//         mode: 'cors', // Adicionando 'cors' no fetch
//       })
//       .then(response => {
//         if (!response.ok) {
//           throw new Error(`Erro na requisição: ${response.status}`);
//         }
//         return response.json();
//       })
//       .then(data => {
//         console.log(data);  // Logando os dados da resposta da API
//         if (data.id) {
//           alert('Post criado com sucesso!');
//           window.location.href = '/devorbit/feed/';
//         } else {
//           alert('Falha ao criar o post.');
//         }
//       })
//       .catch(error => {
//         console.error('Erro ao enviar o formulário:', error);
//         alert('Erro ao enviar o formulário. Tente novamente!');
//       });

  





function handleImageClick(element) {
  // Obter o link da imagem a partir do atributo data-src
  const imageUrl = element.getAttribute('data-src');
  
  // Verificar se a URL da imagem é válida
  if (!imageUrl) {
    console.error('A URL da imagem não foi encontrada.');
    return;
  }

  // Criar o modal
  const modal = document.createElement('div');
  modal.style.cssText = `
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.8); display: flex; justify-content: center;
    align-items: center; z-index: 1000;
    borrde-radius: 50% ;
  `;

  // Criar a imagem para o modal
  const img = document.createElement('img');
  img.src = imageUrl;
  img.style.cssText = 'max-width: 93%; max-height: 93%; border-radius: 8px;';
  img.alt = 'Imagem ampliada';  // Adicionar texto alternativo para acessibilidade

  // Criar o botão de fechar
  const closeButton = document.createElement('span');
  closeButton.textContent = 'X';
  closeButton.style.cssText = `
    position: absolute; top: 20px; right: 20px; color: white;
    font-size: 24px; cursor: pointer;
  `;
  closeButton.onclick = () => document.body.removeChild(modal);

  // Adicionar a imagem e o botão de fechar ao modal
  modal.appendChild(img);
  modal.appendChild(closeButton);

  // Adicionar o modal à página
  document.body.appendChild(modal);
}


  // FUNÇÃO PARA EXIBIR A BARRA LATERAL
  function mybar() {
    const sidebar = document.getElementById('cta-button-sidebar');
    if (sidebar) {
      sidebar.classList.toggle('-translate-x-full');
    } else {
      console.error("Elemento com ID 'cta-button-sidebar' não encontrado!");
    }
  }

  // Exemplo de atribuição à barra lateral (adapte conforme necessário)
  const sidebarToggle = document.querySelector('#sidebar-toggle-button');
  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', mybar);
  }

  
// função para abrir foto de perfil 
function handleImageClick(element) {
  Event.preventDefault();
  const imageUrl = element.getAttribute('data-image-url');
  
  const modal = document.createElement('div');
  modal.style.cssText = `
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.8); display: flex; justify-content: center;
    align-items: center; z-index: 1000;
  `;

  const img = document.createElement('img');
  img.src = imageUrl;
  img.style.cssText = 'max-width: 93%; max-height: 93%; border-radius: 50%;'; // Tornando a imagem redonda

  const closeButton = document.createElement('span');
  closeButton.textContent = 'X';
  closeButton.style.cssText = `
    position: absolute; top: 20px; right: 20px; color: white;
    font-size: 24px; cursor: pointer;
  `;
  closeButton.onclick = () => document.body.removeChild(modal);
  
  modal.appendChild(img);
  modal.appendChild(closeButton);
  document.body.appendChild(modal);
}





document.addEventListener('DOMContentLoaded', function () {
  const viewMoreButton = document.getElementById('view-more');
  
  if (viewMoreButton) {
    viewMoreButton.addEventListener('click', function(event) {
      event.preventDefault(); // Impede qualquer ação de navegação
      const fullComment = document.getElementById('full-comment');
      const commentBtn = document.getElementById('comment-btn');
      
      fullComment.style.display = 'block'; // Exibe o comentário completo
      commentBtn.style.display = 'none';   // Remove o botão "Ver mais"
    });
  }
});

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('form[id^="comment-form-"]').forEach((form) => {
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      
      const postId = form.querySelector('input[name="post_id"]').value.trim();
      const userId = form.querySelector('input[name="user_id"]').value.trim();
      const comment = form.querySelector('textarea[name="comment"]').value.trim();

      if (!comment) {
        alert('O comentário não pode estar vazio.');
        return;
      }

      const url = `https://api-devorbirt.onrender.com/post/${postId}/${userId}/comment/`;

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ comment }),
        });

        if (response.ok) {
          form.querySelector('textarea[name="comment"]').value = '';
         
        } else {
          alert(`Erro ao enviar o comentário: ${response.status}`);
          const commentSection = document.querySelector(`#comments-post-${postId}`);
          const newComment = document.createElement('div');
          newComment.textContent = comment; // Adapte para renderizar o HTML completo
          commentSection.appendChild(newComment);
          alert('Comentário enviado com sucesso!');
        }
      } catch (error) {
        alert('Erro ao processar o comentário. Verifique sua conexão.');
      }
    });
  });
});



