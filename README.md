
# 📦 Sistema de Controle de Estoque

Projeto de sistema web para controle de estoque, desenvolvido com **Flask**, **HTML + Jinja2** e **SQLite**, com ORM usando **SQLAlchemy**. Ideal para gerenciar retiradas, devoluções, extravios e manter um histórico organizado com relatórios e dashboards.

## 💡 Motivação

Elaborei este projeto pensando em uma dificuldade que estava acontecendo no meu serviço:  
**as pessoas pegavam material emprestado e não devolviam**, e não conseguíamos saber **quem tinha retirado o quê**. Isso gerava desorganização, perdas e retrabalho. Com esse sistema, agora é possível registrar todas as movimentações de forma simples e confiável, facilitando o controle e a responsabilização.

## ✨ Funcionalidades

- ✅ Cadastro e visualização de itens em estoque  
- 📥 Registro de **retiradas**, **devoluções** e **extravio** de materiais  
- 📊 Dashboard com visão geral do estoque em tempo real  
- 🧾 Geração de **relatórios** filtráveis  
- 🌐 Interface web responsiva (acessível em celulares)  
- 🗄️ Banco de dados com **SQLite** (leve e portátil)  
- 🔄 Integração com **SQLAlchemy** para manipulação dos dados

## 🛠 Tecnologias utilizadas

- Python 3  
- Flask  
- SQLite  
- SQLAlchemy  
- HTML5 + Jinja2  
- Bootstrap (opcional, se estiver usando para o front-end)

## 🚀 Como rodar o projeto localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS  
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:
   ```bash
   flask run
   ```

5. Acesse no navegador:
   ```
   http://localhost:5000
   ```

## 🌐 Hospedagem

Este projeto pode ser hospedado facilmente no [PythonAnywhere](https://www.pythonanywhere.com/), ideal para aplicações Flask com SQLite.

Usuário de exemplo: `fulano.pythonanywhere.com`

## 📚 Sobre

Este projeto faz parte dos meus estudos em **Engenharia de Software** e **Data Science**, e foi idealizado para facilitar a gestão de materiais em ambientes como almoxarifados, escolas, empresas e obras.

---
