# Resolução Desafio Técnico - Otimização de Banco de Dados para Supermarket

## 1. Visão Geral
Este documento descreve as decisões técnicas e estratégias utilizadas para otimizar o desempenho das consultas em um sistema de supermercado. O objetivo é reduzir o tempo de execução das consultas e melhorar a eficiência do banco de dados, utilizando técnicas como **indexação**, **particionamento de tabelas**, **materialized views** e **tabelas de agregação**.

## 2. Estrutura do Projeto 

A seção a seguir apresenta a organização do projeto **API_SUPERMARKET**, abordando as principais ferramentas utilizadas no desenvolvimento e o modelo de entidade-relacionamento (ER) do sistema.

###  2.1. Ferramentas
As ferramentas utilizadas para esse projeto são: 

#### 2.1.1 Docker
O Docker foi utilizado para garantir a portabilidade e reprodutibilidade do ambiente de desenvolvimento e produção. Com ele, foi possível criar containers isolados para o banco de dados PostgreSQL, a API e outras ferramentas auxiliares.

Utilização no projeto:
- Criação de um container PostgreSQL para gerenciamento do banco de dados.
- Uso de um Docker Compose para orquestrar os serviços.
- Facilidade na execução local e implantação em diferentes ambientes.
#### 2.1.2 PgAdmin
O PgAdmin foi utilizado como ferramenta gráfica para gerenciar e visualizar os dados no PostgreSQL. Ele possibilitou:

- Análise de índices e desempenho das queries.
- Execução de consultas SQL para depuração e otimização.
- Monitoramento do banco de dados.

#### 2.1.3 SQLAlchemy
O SQLAlchemy foi escolhido como ORM (Object-Relational Mapping) para facilitar a interação entre a aplicação e o banco de dados. Com ele, conseguimos:

- Criar modelos de dados que refletem a estrutura do banco.
- Executar queries de forma programática sem a necessidade de SQL puro.
- Gerenciar transações e conexões de maneira eficiente.
#### 2.1.4 Alembic
Alembic foi utilizado para versionamento e gerenciamento de migrações do banco de dados. Isso garantiu:

- Controle sobre as mudanças estruturais do banco.
- Criação e aplicação de migrações automáticas.
- Possibilidade de rollback em caso de erros estruturais.
#### 2.1.5 FastAPI
O FastAPI foi utilizado para desenvolver a API do sistema, garantindo alta performance e suporte a validação automática de dados. Suas vantagens incluem:

- Suporte nativo a async e await, melhorando o desempenho.
- Validação automática de entradas usando Pydantic.
- Documentação interativa via Swagger UI e Redoc.

#### 2.1.6 Jmeter
O JMeter foi utilizado para testes de carga e estresse do banco de dados e da API. Com essa ferramenta, conseguimos:

- Simular múltiplas requisições simultâneas para verificar desempenho.
- Identificar gargalos e otimizar queries e endpoints.
- Testar a escalabilidade do sistema.
#### 2.1.7 Faker
O Faker foi utilizado para gerar dados fictícios para testes. Isso permitiu:

- Popular o banco de dados com 1.000.000 de usuários, 1.000 produtos e 50.000.000 vendas fictícias.
- Simular cenários realistas sem depender de dados reais.
- Criar datasets para testes de carga e performance.

#### 2.1.8 PyTest
O PyTest foi usado como framework de testes unitários e de integração. Ele permitiu:

- Garantia de que as funções do sistema funcionam corretamente.
- Testes automatizados para os endpoints da API e interações com o banco.
- Facilidade na execução e geração de relatórios de testes.
#### 2.1.9 Loguru
O Loguru foi utilizado para logging e monitoramento da aplicação. Ele trouxe:

Registros detalhados de requisições e erros da API.
Facilidade na identificação de falhas e otimização da aplicação.
Logs estruturados que auxiliam na análise de performance.







### 2.2 Arquitetura do Sistema

#### 2.2.1 Diagrama de Entidade e Relacionamentos

O diagrama abaixo representa a modelagem das principais entidades do sistema e seus relacionamentos. Ele fornece uma visão clara da estrutura do banco de dados, facilitando a compreensão das interações entre os diferentes componentes.

![Diagrama de Entidade e Relacionamentos](assets/ER-supermarket-api.png)


#### 2.2.1 Estutura de diretórios

Este projeto segue uma organização modular para facilitar a manutenção, escalabilidade e clareza do código. Abaixo uma descrição da responsabilidade de cada diretório.

- **`alembic/`** → Gerenciamento de versões do banco de dados.
- **`app/`** → Contém a lógica central do sistema, dividido por módulos (`controllers`, `models`, `services`, etc.).
- **`assets/`** → Arquivos estáticos, incluindo diagramas.
- **`htmlcov/`** → Relatórios de cobertura de testes gerados automaticamente.
- **`logs/`** → Registros de eventos e logs do sistema.
- **`tests/`** → Scripts de testes automatizados.
- **`venv/`** → Ambiente virtual Python (deve ser ignorado pelo Git).
- **`Dockerfile`** e **`docker-compose.yml`** → Configuração para deploy com Docker.
- **`requirements.txt`** → Lista de dependências do projeto.


## 3. Instruções de Configuração 

Esta seção contém as instruções para configurar e executar o projeto **API_SUPERMARKET** utilizando **Docker e Docker Compose**.

---

### **3.1 Pré-requisitos**
Antes de iniciar, certifique-se de ter os seguintes softwares instalados:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

### **3.2 Configuração do `.env`**
Crie um arquivo `.env` na raiz do projeto e defina as seguintes variáveis de ambiente:

```env
# Configuração do Banco de Dados
DB_HOST=db
CONTAINER_NAME=postgres_container
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=seu_banco
```

### 3.3. Subindo os Containers com Docker Compose
Para iniciar os serviços (backend e db), execute o seguinte comando no terminal:

```sh
docker-compose up --build -d
```

Esse comando irá:
- Construir a imagem do backend a partir do Dockerfile.
- Criar e iniciar os containers para o backend e o banco de dados PostgreSQL.

Para visualizar os logs dos containers em tempo real:

### 3.4 Executando as Migrations
Antes de rodar a aplicação, aplique as migrations do banco de dados:

```sh
alembic upgrade head
```
### 3.5 Testando a Aplicação
Após iniciar os containers, acesse a API em:

🔗 http://localhost:8000/docs (Swagger UI)

Se precisar acessar o banco de dados PostgreSQL:

```sh
docker exec -it postgres_container psql -U seu_usuario -d seu_banco
```
Ou utilizar ferramentas como **pgAdmin**.

## 4. Estratégias de Otimização

### 4.1 Indexação
A indexação foi utilizada para otimizar buscas e reduzir o tempo de resposta de consultas frequentes.

- **Tabelas indexadas:** `sales`, `product_sales`, `product`
- **Principais indexes:**
  - **Composto**: `product_sales (idx_id_sale, idx_id_product)` - Reduziu o tempo da consulta de produto mais vendido de *timeout* para **12 segundos**.
  - **Simples**:
    - `product (idx_category)`: Otimizou a consulta de faturamento por categoria.
    - `sales (idx_datetime, idx_id_user)`: Melhorou consultas por períodos e busca de cliente com mais compras.

| Consulta                        | Tempo Inicial | Tempo com Indexação |
|--------------------------------|--------------|-----------------|
| Produto mais vendido          | Timeout      | 12s             |
| Faturamento por categoria      | Timeout      | Melhorado       |
| Cliente com mais compras       | 11.3s        | 4.6s            |

### 4.2 Particionamento de Tabelas
A tabela `sales` foi particionada por **data (`datetime`)**, o que reduziu significativamente o tempo das consultas.

| Consulta                        | Tempo Inicial | Tempo com Particionamento |
|--------------------------------|--------------|-------------------------|
| Total de vendas em um período | 6.4s        | 1.2s                     |
| Produto mais vendido          | Timeout      | Timeout                  |
| Média de vendas por mês      | 36s         | 9.75s                     |
| Cliente com mais compras      | 11.3s        | 4.6s                      |

### 4.3 Materialized Views
As materialized views foram criadas para armazenar consultas complexas e reduzir o tempo de execução de buscas históricas.
- **Exemplo:** `yearly_total_sales`
  - Criada para armazenar dados de vendas dos últimos anos.
  - Atualizada automaticamente todos os dias às **3h da manhã**.
  - Reduziu o tempo da consulta de **10s para 6s**.

### 4.4 Tabelas de Agregação
Tabelas agregadas foram criadas para otimizar consultas que necessitavam de vários joins. Atualização periódica através de **jobs automáticos**.

- **Tabela `product_sales_aggregated`**:
  - Substitui joins entre `sales`, `product_sales` e `product`.
  - Tempo de consulta significativamente reduzido.
  
- **Tabela `category_revenue_aggregated`**:
  - Agrega faturamento por categoria.
  - Evita cruzamento entre `sales`, `product`, `category`, `product_sales`.

  - **Tabela `customer_purchases_aggregated`**:
  - Agrega faturamento por categoria.
  - Facilita o cálculo da **quantidade diária** de produtos comprados por cliente.

## 5. Endpoints e Consultas Otimizadas

| Endpoint | Consulta Otimizada |
|----------|-------------------|
| `/sales/summary?start_date=yyyy/mm/dd&end_date=yyyy/mm/dd` | Consulta `sales`, utilizando index e particionamento. |
| `/sales/top-product?start_date=yyyy/mm/dd&end_date=yyyy/mm/dd` | Utiliza `product_sales_aggregated` para realizar a consulta. |
| `/sales/revenue-by-category?start_date=yyyy/mm/dd&end_date=yyyy/mm/dd` | Usa `category_revenue_aggregated` para realizar a consulta. |
| `/sales/monthly-average` | Usa a MATERIALIZED VIEW `yearly_total_sales` para realizar a consulta. |
| `/sales/top-customer?start_date=yyyy/mm/dd&end_date=yyyy/mm/dd` | Utiliza `customer_purchases_aggregated` para realizar a consulta. |

## 6. Testes

### 6.1 Testes Unitários
Os testes unitários são realizados para validar a correta execução das queries e a consistência dos dados.
- **Verificação de indexes:** Confirma se os indexes estão sendo utilizados.
- **Validação de Materialized Views:** Checa se as views contêm os dados esperados.
- **Verificação de Agregação:** Garante que as tabelas agregadas estão corretas.
- **Validação de datas:** Garante que as datas de início e fim da consulta estão em um intervalo válido e são datas aplicáveis.

### 6.2 Cobertura de testes

### 6.2 Cobertura de Testes  

A cobertura de testes é uma métrica essencial para avaliar a eficácia dos testes automatizados no projeto. Ela mede a quantidade de código executado durante a execução dos testes, garantindo que as funcionalidades críticas sejam verificadas e reduzindo a chance de erros em produção.  

No **API_SUPERMARKET**, a cobertura de testes é monitorada utilizando o **pytest-cov**, que gera relatórios detalhados sobre as áreas do código que foram testadas e aquelas que ainda precisam de validação.  

Os relatórios de cobertura são gerados automaticamente e podem ser visualizados no diretório `htmlcov/`. Para executar os testes e gerar o relatório de cobertura, utilize o seguinte comando:  

```sh
pytest --cov=app --cov-report=html
```

Após a execução, abra o arquivo htmlcov/index.html no navegador para visualizar a cobertura detalhada.


### 6.3 Testes de Carga
Os testes de carga são essenciais para avaliar o desempenho do sistema sob condições de alto volume de acessos simultâneos, garantindo que a aplicação seja capaz de lidar com picos de tráfego sem comprometer a experiência do usuário. Para realizar essa avaliação, utilizamos o JMeter, uma ferramenta robusta e amplamente reconhecida para testes de desempenho.

Resultados Obtidos
Abaixo, você encontrará um relatório agregado gerado pelo JMeter, que resume os principais indicadores de desempenho, como:

Tempo de Resposta Médio: Tempo médio que o sistema leva para processar uma requisição.

Throughput/Vazão: Número de transações por segundo que o sistema consegue suportar.

Taxa de Erros: Porcentagem de requisições que falharam durante o teste.

Desempenho sob Carga: Comportamento do sistema ao aumentar o número de usuários simultâneos.

![Relatório Agregado do JMeter](assets/teste-de-carga.png)

Esses resultados nos permitem identificar possíveis gargalos e otimizar a aplicação para garantir um desempenho consistente, mesmo em cenários de alta demanda.


## 7. Conclusão
As estratégias aplicadas resultaram em uma melhora significativa no desempenho das consultas, tornando o sistema mais eficiente para grandes volumes de dados. O uso de **indexação**, **particionamento**, **materialized views** e **tabelas agregadas** foi essencial para otimizar a performance do banco de dados.