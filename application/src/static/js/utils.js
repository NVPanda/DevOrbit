

  
  // Função para lidar com o envio do like
document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-button');
    
    likeButtons.forEach(button => {
      button.addEventListener('click', async function () {
        const postId = button.getAttribute('data-id'); // ID do post
        const userId = button.getAttribute('data-user-id'); // ID do usuário
  
        console.log(`Tentando curtir o post ${postId} com o usuário ${userId}`);
  
        try {
          const response = await fetch(`https://api-devorbirt.onrender.com/user/${userId}/likes/${postId}`, { 
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json', // Especifica que o corpo da requisição é JSON
            },
            body: JSON.stringify({
              userId: userId,
              postId: postId,
            }),
          });
      
  
          if (response.ok) {
            const data = await response.json();
            console.log('Like atualizado:', data);
  
            // Atualiza o número de likes na interface
            const likeCountElement = document.getElementById(`like-count-${postId}`);
            if (likeCountElement) {
              likeCountElement.textContent = data.likes;
            } else {
              console.error(`Elemento com id 'like-count-${postId}' não encontrado`);
            }
  
            // Altera a cor do botão de curtir
            button.classList.toggle('text-blue-500');
            button.classList.toggle('text-gray-600');
          } else {
            console.error('Erro ao enviar o like');
          }
        } catch (error) {
          console.error('Erro de conexão com a API:', error);
        }
      });
    });
  });
  
  // Função para lidar com o clique na imagem
  function handleImageClick(imageUrl) {
    // Cria um elemento para o modal
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    modal.style.display = 'flex';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
    modal.style.zIndex = '1000';
  
    // Cria a imagem no modal
    const img = document.createElement('img');
    img.src = imageUrl;
    img.style.maxWidth = '93%';
    img.style.maxHeight = '93%';
    img.style.borderRadius = '8px';
  
    // Botão para fechar o modal
    const closeButton = document.createElement('span');
    closeButton.textContent = 'X';
    closeButton.style.position = 'absolute';
    closeButton.style.top = '20px';
    closeButton.style.right = '20px';
    closeButton.style.color = 'white';
    closeButton.style.fontSize = '24px';
    closeButton.style.cursor = 'pointer';
  
    // Remove o modal ao clicar no botão de fechar
    closeButton.onclick = () => {
      document.body.removeChild(modal);
    };
  
    // Adiciona os elementos ao modal
    modal.appendChild(img);
    modal.appendChild(closeButton);
  
    // Adiciona o modal ao corpo do documento
    document.body.appendChild(modal);
  }
  
  // Função para exibir a barra lateral (não modificada)
function mybar() {
    var x = document.getElementById("cta-button-sidebar");
    if (x.classList.contains("-translate-x-full")) {
      x.classList.remove("-translate-x-full");
    } else {
      x.classList.add("-translate-x-full");
    }
}
  
// Função para mostrar o overlay de carregamento
function showLoading() {
  const loadingOverlay = document.getElementById('loadingOverlay');
  loadingOverlay.style.display = 'flex'; // Exibe o overlay
}

// Função para ocultar o overlay de carregamento
function hideLoading() {
  const loadingOverlay = document.getElementById('loadingOverlay');
  loadingOverlay.style.display = 'none'; // Esconde o overlay
}

// Função genérica para tratar o redirecionamento com efeito de carregamento
function setupProfileRedirect(selector, url) {
  const profileLink = document.querySelector(selector);

  if (profileLink) {
    profileLink.addEventListener('click', function(e) {
      e.preventDefault(); // Previne a navegação imediata
      showLoading(); // Mostra o overlay de carregamento

      // Navega para o link após 2 segundos
      setTimeout(() => {
        window.location.href = url; // Redireciona para o link
      }, 2000); // Tempo do efeito de carregamento
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Configura o redirecionamento para o perfil
  setupProfileRedirect("a[data-url='{{ url_for('perfil.profile_page', usuario=username) }}']", '{{ url_for('perfil.profile_page', usuario=username) }}');
  
  // Configura o redirecionamento para a home
  setupProfileRedirect("a[data-url='{{ url_for('home.home_page', usuario=username) }}']", '{{ url_for('home.home_page', usuario=username) }}');
});

// Exibir ou esconder o formulário de exclusão
function toggleDeleteForm() {
  const deleteForm = document.getElementById('deleteForm');
  deleteForm.style.display = deleteForm.style.display === 'none' || deleteForm.style.display === '' ? 'block' : 'none';
}

// Confirmar exclusão
function confirmDeletion() {
  const reason = document.getElementById('deleteReason').value;
  if (confirm('Tem certeza de que deseja excluir sua conta?')) {
    alert(`Conta excluída.\nMotivo: ${reason || 'Nenhum motivo fornecido'}`);
    // Adicione a lógica para excluir a conta aqui (por exemplo, requisição à API)
  } else {
    alert('Exclusão cancelada.');
  }
}

// Eventos dos botões
document.getElementById('saveBioBtn').addEventListener('click', toggleDeleteForm);
document.getElementById('cancelDeleteBtn').addEventListener('click', toggleDeleteForm);
document.getElementById('confirmDeleteBtn').addEventListener('click', confirmDeletion);
