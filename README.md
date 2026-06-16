# Golden Raspberry Awards API - Avaliação Back-end

Esta API RESTful foi desenvolvida seguindo rigorosos padrões de engenharia de software para atender aos requisitos da avaliação técnica da **Outsera**. A solução identifica os produtores com o maior e o menor intervalo entre prêmios consecutivos na categoria "Pior Filme" do Golden Raspberry Awards.

## Conformidade com os Requisitos

Abaixo, detalhamos como cada requisito do documento de especificação foi atendido:

### 1. Requisitos do Sistema
- **Carga de Dados**: Ao iniciar, a aplicação lê automaticamente o arquivo `Movielist.csv` e popula o banco de dados em memória. A implementação utiliza o padrão *Startup Event* do FastAPI para garantir que os dados estejam disponíveis antes de qualquer requisição.

### 2. Requisitos da API
- **Cálculo de Intervalos**: Implementamos uma lógica robusta em `AwardService` que processa todos os produtores (mesmo em filmes com múltiplos produtores), identifica vitórias consecutivas e calcula os intervalos. O retorno segue estritamente o formato JSON definido na página 2 do documento.

### 3. Requisitos Não Funcionais
- **Nível de Maturidade de Richardson**: A API foi implementada seguindo o **Nível 2**, utilizando métodos HTTP corretos (`GET`), códigos de status apropriados e recursos bem definidos.
- **Testes de Integração**: Implementados utilizando `pytest` e `httpx`, garantindo que o fluxo completo (desde a carga de dados até o cálculo final) esteja correto e de acordo com a proposta.
- **Banco de Dados em Memória**: Utilizamos **SQLite em memória** (ou arquivo local volátil para persistência durante a sessão), eliminando a necessidade de instalações externas como PostgreSQL ou MySQL.
- **Repositório e Instruções**: O projeto está estruturado para ser facilmente versionado em Git e contém todas as instruções necessárias para execução e teste.

### 4. Quadro de Atenção (Robustez e Lógica)
- **Independência de Dados**: A lógica foi desenhada para ser agnóstica ao conteúdo do CSV. Se o conjunto de dados mudar, o sistema recalculará os intervalos dinamicamente sem necessidade de alteração no código.
- **Qualidade de Código**: Aplicamos princípios **SOLID**, **Clean Code** e padrões de projeto (**Repository/Service**) para demonstrar maturidade técnica e facilitar a manutenção.

## Estrutura do Projeto

```
golden_raspberry_api/
├── app/
│   ├── api/             # Endpoints da API
│   ├── core/            # Configurações e utilitários
│   ├── database/        # Configuração do banco de dados em memória e carga inicial
│   ├── models/          # Modelos de dados (Pydantic e SQLAlchemy)
│   ├── repositories/    # Camada de acesso a dados
│   └── services/        # Lógica de negócio
├── tests/               # Testes de integração
├── .env                 # Variáveis de ambiente (ex: caminho do CSV)
├── main.py              # Ponto de entrada da aplicação FastAPI
└── requirements.txt     # Dependências do projeto
```

## Configuração e Execução

1.  **Clone o repositório** (se aplicável).
2.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure o arquivo `.env`** (exemplo):
    ```
    CSV_FILE_PATH=Movielist.csv
    ```
4.  **Execute a aplicação**:
    ```bash
    uvicorn main:app --reload
    ```

## Endpoints da API

-   `GET /awards/intervals`: Retorna os produtores com o maior e o menor intervalo entre prêmios consecutivos.

## Testes

Para executar os testes de integração:

```bash
pytest
```
