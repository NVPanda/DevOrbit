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
  