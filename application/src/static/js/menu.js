document.addEventListener('DOMContentLoaded', function () {
  const formElement = document.getElementById('post-form');

  if (formElement) {
    formElement.addEventListener('submit', (event) => {
      event.preventDefault();

      const formData = new FormData(formElement);

      fetch('http://127.0.0.1:8000/post/', { // Use o endpoint do FastAPI
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
          if (data.success) {
            alert('Post criado com sucesso!');
            window.location.href = '/devorbit/feed/'; // Redireciona para a página de feed
          } else {
            alert('Falha ao criar o post.');
          }
        })
        .catch(error => {
          console.error('Erro ao enviar o formulário:', error);
          window.location.href = '/devorbit/feed/';
        });
    });
  }
});




  // FUNÇÃO PARA EXIBIR O MODAL DE IMAGEM
  function handleImageClick(imageUrl) {
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

