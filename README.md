# Luizalabs Challenge

Este projeto foi desenvolvido como parte de um desafio da Magalu/Luizalabs. O objetivo principal foi criar uma API para gerenciar clientes e seus produtos favoritos, com alguns diferenciais implementados para melhorar a escalabilidade, performance e usabilidade da solução.

## Tecnologias Utilizadas

- **FASTAPI**: Utilizado devido à sua arquitetura assíncrona, garantindo boa escalabilidade e desempenho diante de um grande volume de requisições.
- **MongoDB com driver Motor**: Escolhido por seu excelente desempenho em conjunto com o ASGI do FASTAPI.
- **Poetry**: Ferramenta utilizada para gerenciar dependências e executar o projeto.
- **Autenticação Bearer Token**: Implementada para garantir a segurança dos endpoints.
- **Flake8 e isort**: Utilizados como ferramentas de linting para manter a qualidade e organização do código.

## Observações sobre a implementação

1. **Geração de IDs**: Não é realizada pela API, ficando sob responsabilidade das partes que irão se integrar.
2. **Endpoints de Produtos**: Devido à indisponibilidade da API de produtos, foi implementado um conjunto de endpoints para gerenciar produtos diretamente nesta solução.
3. **Guidelines**: O desenvolvimento foi realizado seguindo os [guidelines da Luizalabs](https://github.com/luizalabs/dev-guide) e outras dicas publicadas no Medium da empresa, priorizando boas práticas de código e organização do projeto.
4. Por se tratar de uma demonstração, o usuario e a senha de acesso a api estão no arquivo .env

## Como Executar o Projeto

Existem duas abordagens para executar o projeto:

### Com Poetry

1. Certifique-se de que você tem o **Python 3.7+**, **MongoDB** e **Poetry** instalados.
2. Crie um ambiente virtual com o comando:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   poetry install
   ```
4. Copie o arquivo de exemplo de variáveis de ambiente e renomeie-o:
   ```bash
   cp .env.example .env
   ```
5. Execute a aplicação:
   ```bash
   python main.py
   ```
6. Acesse em: http://0.0.0.0:8080/docs

### Com Requirements.txt

1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
2. Instale as dependências manualmente:
   ```bash
   pip install -r requirements.txt
   ```
3. Copie o arquivo de exemplo de variáveis de ambiente e renomeie-o:
   ```bash
   cp .env.example .env
   ```
4. Execute a aplicação:
   ```bash
   python main.py
   ```
51. Acesse em: http://0.0.0.0:8080/docs

## Comandos Adicionais
- **Testes**:
    ```bash
    pytest
   ```
- **Linting do código**:
  ```bash
  poetry run flake8
  ```
- **População do Banco de Dados**:
  ```bash
  python main.py --db_populate
  ```
- **Reset do Banco de Dados**:
  ```bash
  python main.py --db_reset
  ```

## Testando a API

Esta API inclui uma documentação interativa que pode ser acessada em:

```
http://0.0.0.0:8080/docs
```
ou se preferir:
```
http://0.0.0.0:8080/redoc
```

### Autenticação

Para acessar os endpoints, é necessário utilizar autenticação Bearer Token. Clique em "Authorize" no Swagger e insira o token fornecido para ter acesso às funcionalidades da API.

## Contatos

Caso encontre algum bug ou tenha sugestões, fique à vontade para entrar em contato:

- **E-mail**: matheus.muriel@outlook.com
- **LinkedIn**: [Matheus Muriel](https://www.linkedin.com/in/matheusmuriel/)

---

Obrigado por utilizar este projeto! :)

