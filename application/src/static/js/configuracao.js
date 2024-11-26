document.getElementById('showInputBtn').addEventListener('click', () => {
    const inputContainer = document.getElementById('inputContainer');
    if (inputContainer.style.display === 'none') {
        inputContainer.style.display = 'block'; // Mostra o input
    } else {
        inputContainer.style.display = 'none'; // Esconde o input
    }
});

document.getElementById("saveBioBtn").addEventListener("click", function() {
    const newBio = document.getElementById("bioInput").value.trim();
    
    if (newBio) {
        const userId = document.getElementById("user_id").value; // Pega o ID do usuário do campo hidden
        const apiUrl = `http://localhost:5000/files/username/${userId}/bio`; // URL da API

        // Enviar a requisição PUT para a API
        fetch(apiUrl, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ new_bio: newBio })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "Bio atualizada com sucesso") {
                // Atualiza a bio exibida na página
                document.querySelector(".bio-user").textContent = newBio;
                alert("Bio atualizada com sucesso!");
            } else {
                alert("Erro ao atualizar a bio");
            }
        })
        .catch(error => {
            console.error("Erro:", error);
            alert("Erro na requisição. Tente novamente.");
        });
    } else {
        alert("A bio não pode estar vazia!");
    }
});
