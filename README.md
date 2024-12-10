# daily-diet-api

Repositório criado para armazenar o código da API de Daily Diet com banco de dados.

## Sobre o Projeto

Este projeto foi desenvolvido com fins de estudo, como parte do aprendizado e prática de desenvolvimento de APIs utilizando Flask, banco de dados MySQL e autenticação de usuários. O foco foi construir uma API simples para gerenciar refeições diárias, com funcionalidades de login, CRUD (Create, Read, Update, Delete) de refeições e autenticação de usuários.

Este projeto não é destinado a uso em produção, mas sim como uma demonstração das habilidades adquiridas no processo de desenvolvimento.

## Tecnologias Utilizadas

- **Flask**: Framework web para Python
- **Flask-Login**: Gerenciamento de sessões de usuários
- **SQLAlchemy**: ORM para interação com banco de dados
- **MySQL**: Banco de dados utilizado
- **bcrypt**: Hashing de senhas
- **PyMySQL**: Driver para MySQL em Python

## EndPoints

- **POST /login**: Realiza o login de um usuário
- **POST /sign-up**: Registra um novo usuário
- **GET /user/meals**: Retorna todas as refeições do usuário
- **POST /user/meals**: Adiciona uma nova refeição
- **GET /user/meal/{id_meal}**: Retorna uma refeição específica
- **PUT /user/meal/{id_meal}**: Atualiza uma refeição existente
- **DELETE /user/meal/{id_meal}**: Exclui uma refeição

Exemplo de requisição de login:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "user", "password": "senha"}' http://127.0.0.1:5000/login
