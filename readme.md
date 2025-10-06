# Controle Financeiro

Sistema web de controle financeiro com **Python (Flask)**, **Vue.js** e **MySQL**.

---

## Tecnologias
- Python (Flask)
- Vue.js
- MySQL
- Docker + Docker Compose

---

## Estrutura

<img width="315" height="140" alt="image" src="https://github.com/user-attachments/assets/edf8423e-d4c8-4048-9abb-8f49fe674b1d" />


---

## Rodando o projeto

1. Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd controle-financeiro
````
---
```bash
docker-compose up --build
````
### Dados do Conteiner:
API: http://localhost:5000/

Front-end: http://localhost:8080/

MySQL: localhost:3307

```bash
docker-compose down
````
---

## Atualizando Dependências Python

```bash
cd api
pip install <nova_biblioteca>
pip freeze > requirements.txt
docker-compose up --build
````
