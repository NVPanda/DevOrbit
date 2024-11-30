document.addEventListener('DOMContentLoaded', function () {
  const formElement = document.getElementById('post-form');

  if (formElement) {
    formElement.addEventListener('submit', (event) => {
      event.preventDefault();

      const formData = new FormData(formElement);

      // Verificar se todos os campos necessários estão presentes
      if (!formData.has('user_id') || !formData.has('nome') || !formData.has('titulo') || !formData.has('post')) {
        alert('Por favor, preencha todos os campos obrigatórios!');
        return;
      }

      fetch('https://api-devorbirt.onrender.com/post/', { 
        method: 'POST',
        body: formData, // Envia o FormData diretamente
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.status}`);
          }

          return response.json();
        })
        .then(data => {
          if (data.id) {  // Supondo que um "id" seja retornado como sucesso
            alert('Post criado com sucesso!');
            window.location.href = '/devorbit/feed/'; // Redireciona para a página de feed
          } else {
            alert('Falha ao criar o post.');
          }
        })
        .catch(error => {
          alert('Erro ao enviar o formulário. Tente novamente!');
        });
    });
  }
});






function handleImageClick(element) {
  // Garantir que `element` seja válido e obtenha o atributo src
  const imageUrl = element.getAttribute('src');

  // Criar o modal
  const modal = document.createElement('div');
  modal.style.cssText = `
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.8); display: flex; justify-content: center;
    align-items: center; z-index: 1000;
  `;

  const img = document.createElement('img');
  img.src = imageUrl;
  img.style.cssText = 'max-width: 93%; max-height: 93%; border-radius: 8px;';

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

// função para abri foto de perfil 
function handleImageClick(element) {
    const imageUrl = element.getAttribute('data-image-url');
    
    const modal = document.createElement('div');
    modal.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background-color: rgba(0, 0, 0, 0.8); display: flex; justify-content: center;
      align-items: center; z-index: 1000;
    `;

    const img = document.createElement('img');
    img.src = imageUrl;
    img.style.cssText = 'max-width: 93%; max-height: 93%; border-radius: 8px;';

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
