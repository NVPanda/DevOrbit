DevOrbit Community
🌌 Bem-vindo à DevOrbit Community!
A DevOrbit é uma plataforma open source que conecta estudantes, entusiastas de tecnologia e desenvolvedores de todas as áreas. Nosso objetivo é criar um ambiente colaborativo e inspirador, onde todos possam compartilhar conhecimentos, projetos e experiências.

🎯 O que é a DevOrbit Community?
A DevOrbit Community nasceu como um desafio pessoal, um projeto criado para explorar novas habilidades e conectar desenvolvedores apaixonados por tecnologia. É uma rede social que permite:

Interagir: Troque ideias e conhecimentos com outros membros.
Aprender: Participe de discussões, colabore em projetos e expanda suas habilidades.
Compartilhar: Mostre seus projetos, contribua com a comunidade e inspire outras pessoas.
🌟 Nosso diferencial? Um ambiente leve e descontraído, feito para o dia a dia dos desenvolvedores.

🛠️ Funcionalidades
Feed de Projetos: Descubra e compartilhe projetos incríveis de tecnologia.
Sistema de Usuários: Login seguro com Flask-Login e autenticação para proteger a comunidade.
Página de Perfil: Personalize seu perfil e conecte-se com outros membros.
Filtros e Likes: Filtre posts populares e veja o que está em alta na comunidade.
Sistema de Erros: Exibição dinâmica de erros HTTP com redirecionamento automático.
(Mais funcionalidades em breve... 🎉)

🚀 Como começar?
1. Clone o repositório
bash
Copiar
Editar
git clone [https://github.com/Gilderlan0101/CodeChamber]
cd DevOrbit
2. Instale as dependências
Certifique-se de ter Python e Node.js instalados. Então, execute:

bash
Copiar
Editar
# Backend (Python)
python -m venv my_env
source my_env/bin/activate  # Linux/MacOS
my_env\Scripts\activate     # Windows
pip install -r requirements.txt

# Frontend (TailwindCSS)
npm install
3. Configure o ambiente
Crie um arquivo .env na raiz do projeto e adicione as variáveis de ambiente necessárias. Por exemplo:

env
Copiar
Editar

API = 'https://api-devorbirt.onrender.com/posts/'
SECRET_KEY = 'sua_chave_secreta_aqui'
API_NOTICIA = 'sua_chave_da_api_de_noticias_aqui'  # Obtenha sua chave em: https://developer.nytimes.com/

CODECHAMBER = 'DEV ORBIT'
MENSAGEN = 'Fala dev!'
MENSAGEN_POST = 'Os melhores posts vão aparecer aqui! 🌟 Não deixe de comentar e compartilhar suas ideias. Vamos juntos criar uma comunidade incrível!'

## Configuração da Chave de API de Notícias

Para usar a integração com a API de notícias no DevOrbit, você precisa obter uma chave de acesso no site do New York Times:

1. Acesse o site oficial do New York Times para desenvolvedores:  
   [https://developer.nytimes.com/](https://developer.nytimes.com/)

2. Crie uma conta ou faça login.

3. Gere uma chave de API no painel do desenvolvedor.

4. No arquivo `.env ou .env.local`, adicione a chave no campo `API_NOTICIA`:
   ```env
   API_NOTICIA=https://api.nytimes.com/svc/topstories/v2/technology.json?api-key=_chave_da_api_de_noticias

Resultado:

    API = 'https://api-devorbirt.onrender.com/posts/'
    SECRET_KEY = 'sua_chave_secreta_aqui'
    API_NOTICIA = 'sua_chave_da_api_de_noticias_aqui'  # Obtenha sua chave em: https://developer.nytimes.com/
    
    CODECHAMBER = 'DEV ORBIT'
    MENSAGEN = 'Fala dev!'
    MENSAGEN_POST = 'Os melhores posts vão aparecer aqui! 🌟 Não deixe de comentar e compartilhar suas ideias. Vamos juntos criar uma comunidade incrível!'



BANCO_DB='usuarios.db'
4. Rode o projeto
bash
Copiar
Editar
# Compile o CSS com Tailwind
npm run dev

# Inicie o servidor Flask
python3 run.py
O projeto estará disponível em: [http://127.0.0.1:5000/devorbit/feed/]

🤝 Contribuindo
Adoraríamos a sua ajuda! Siga estes passos para contribuir com o projeto:


Faça um fork do repositório.
Crie uma nova branch para sua funcionalidade ou correção.
bash
Copiar
Editar
git checkout -b minha-nova-funcionalidade
Commit suas alterações.
bash
Copiar
Editar
git commit -m "Adiciona nova funcionalidade"
Envie seu código para o fork.
bash
Copiar
Editar
git push origin minha-nova-funcionalidade
Abra um Pull Request e descreva sua contribuição. 🎉

# Novos contribuintes devem acessar o arquivo CONTRIBUTORS.md e adicionar seu nome e e-mail na lista de contribuições.


📜 Licença
Este projeto está licenciado sob a GNU AGPLv3.
Consulte o arquivo LICENSE para mais informações.

🌐 Entre na conversa!
Fique à vontade para se conectar conosco em nossa comunidade no Discord!
Entre no Discord da DevOrbit

✨ Agradecimentos
Um agradecimento especial a todos que contribuem para tornar a DevOrbit Community um lugar incrível para desenvolvedores de todo o mundo. Vamos juntos transformar ideias em realidade! 💡🌍

