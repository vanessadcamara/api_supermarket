# api_supermarket
# Documentação - Otimização de Banco de Dados para Supermarket

## 1. Visão Geral
Este documento descreve as decisões técnicas e estratégias utilizadas para otimizar o desempenho das consultas em um sistema de supermercado. O objetivo é reduzir o tempo de execução das consultas e melhorar a eficiência do banco de dados, utilizando técnicas como **indexação**, **particionamento de tabelas**, **materialized views** e **tabelas de agregação**.

## 2. Estrutura do Projeto 

## 3. Estratégias de Otimização

### 3.1 Indexação
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

### 3.2 Particionamento de Tabelas
A tabela `sales` foi particionada por **data (`datetime`)**, o que reduziu significativamente o tempo das consultas.

| Consulta                        | Tempo Inicial | Tempo com Particionamento |
|--------------------------------|--------------|-------------------------|
| Total de vendas em um período | 6.4s        | 1.2s                     |
| Produto mais vendido          | Timeout      | Timeout                  |
| Média de vendas por mês      | 36s         | 9.75s                     |
| Cliente com mais compras      | 11.3s        | 4.6s                      |

### 3.3 Materialized Views
As materialized views foram criadas para armazenar consultas complexas e reduzir o tempo de execução de buscas históricas.
- **Exemplo:** `yearly_total_sales`
  - Criada para armazenar dados de vendas dos últimos anos.
  - Atualizada automaticamente todos os dias às **3h da manhã**.
  - Reduziu o tempo da consulta de **10s para 6s**.

### 3.4 Tabelas de Agregação
Tabelas agregadas foram criadas para otimizar consultas que necessitavam de vários joins. Atualização periódica através de **jobs automáticos**.

- **Tabela `product_sales_aggregated`**:
  - Substitui joins entre `sales`, `product_sales` e `product`.
  - Tempo de consulta significativamente reduzido.
  
- **Tabela `category_revenue_aggregated`**:
  - Agrega faturamento por categoria.
  - Evita cruzamento entre `sales`, `product`, `category`, `product_sales`.

## 4. Endpoints e Consultas Otimizadas

| Endpoint | Consulta Otimizada |
|----------|-------------------|
| `/sales/summary?start_date=yyyy/mm/dd&end_date=yyyy/mm/dd` | Consulta `sales`, utilizando index e particionamento. |
| `/sales/top-product?start_date=yyyy/mm/dd&end_date=yyyy/mm/dd` | Utiliza `product_sales_aggregated`. |
| `/sales/revenue-by-category?start_date=yyyy/mm/dd&end_date=yyyy/mm/dd` | Usa `category_revenue_aggregated`. |
| `/sales/monthly-average` | Usa `yearly_total_sales`. |
| `/sales/top-customer?start_date=yyyy/mm/dd&end_date=yyyy/mm/dd` | Consulta `sales` com index em `idx_id_user`. |

## 5. Testes

### 5.1 Testes Unitários
Os testes unitários são realizados para validar a correta execução das queries e a consistência dos dados.
- **Verificação de indexes:** Confirma se os indexes estão sendo utilizados.
- **Validação de Materialized Views:** Checa se as views contêm os dados esperados.
- **Verificação de Agregação:** Garante que as tabelas agregadas estão corretas.
- **Validação de datas:** Garante que as datas de início e fim da consulta estão em um intervalo válido e são datas aplicáveis.

### 5.2 Testes de Carga
Os testes de carga avaliam o desempenho sob condições de alto volume de acessos simultâneos.
- **Teste com 100, 500 e 1000 requisições simultâneas** para os endpoints.
- **Análise de tempo de resposta antes e depois da otimização**.
- **Medição de uso de CPU e Memória** durante as execuções.

## 6. Ferramentas
As ferramentas utilizadas para esse projeto são: 

### 6.1 Docker
O Docker foi utilizado para garantir a portabilidade e reprodutibilidade do ambiente de desenvolvimento e produção. Com ele, foi possível criar containers isolados para o banco de dados PostgreSQL, a API e outras ferramentas auxiliares.

Utilização no projeto:
- Criação de um container PostgreSQL para gerenciamento do banco de dados.
- Uso de um Docker Compose para orquestrar os serviços.
- Facilidade na execução local e implantação em diferentes ambientes.
### 6.2 PgAdmin
O PgAdmin foi utilizado como ferramenta gráfica para gerenciar e visualizar os dados no PostgreSQL. Ele possibilitou:

- Análise de índices e desempenho das queries.
- Execução de consultas SQL para depuração e otimização.
- Monitoramento do banco de dados.

### 6.3 SQLAlchemy
O SQLAlchemy foi escolhido como ORM (Object-Relational Mapping) para facilitar a interação entre a aplicação e o banco de dados. Com ele, conseguimos:

- Criar modelos de dados que refletem a estrutura do banco.
- Executar queries de forma programática sem a necessidade de SQL puro.
- Gerenciar transações e conexões de maneira eficiente.
### 6.4 Alembic
Alembic foi utilizado para versionamento e gerenciamento de migrações do banco de dados. Isso garantiu:

- Controle sobre as mudanças estruturais do banco.
- Criação e aplicação de migrações automáticas.
- Possibilidade de rollback em caso de erros estruturais.
### 6.5 FastAPI
O FastAPI foi utilizado para desenvolver a API do sistema, garantindo alta performance e suporte a validação automática de dados. Suas vantagens incluem:

- Suporte nativo a async e await, melhorando o desempenho.
- Validação automática de entradas usando Pydantic.
- Documentação interativa via Swagger UI e Redoc.

### 6.6 Jmeter
O JMeter foi utilizado para testes de carga e estresse do banco de dados e da API. Com essa ferramenta, conseguimos:

- Simular múltiplas requisições simultâneas para verificar desempenho.
- Identificar gargalos e otimizar queries e endpoints.
- Testar a escalabilidade do sistema.
### 6.7 Faker
O Faker foi utilizado para gerar dados fictícios para testes. Isso permitiu:

- Popular o banco de dados com 1.000.000 de usuários, 1.000 produtos e 50.000.000 vendas fictícias.
- Simular cenários realistas sem depender de dados reais.
- Criar datasets para testes de carga e performance.

### 6.8 PyTest
O PyTest foi usado como framework de testes unitários e de integração. Ele permitiu:

- Garantia de que as funções do sistema funcionam corretamente.
- Testes automatizados para os endpoints da API e interações com o banco.
- Facilidade na execução e geração de relatórios de testes.
### 6.9 Loguru
O Loguru foi utilizado para logging e monitoramento da aplicação. Ele trouxe:

Registros detalhados de requisições e erros da API.
Facilidade na identificação de falhas e otimização da aplicação.
Logs estruturados que auxiliam na análise de performance.

### 6.10 Dotenv
O Dotenv foi utilizado para gerenciamento de variáveis de ambiente de forma segura e organizada. Ele permitiu:

- Armazenamento de credenciais sensíveis, como conexões com o banco de dados e chaves de API, sem expô-las diretamente no código-fonte.
- Facilidade na configuração de diferentes ambientes (desenvolvimento, testes e produção).
- Carregamento automático de variáveis no ambiente Python.

## 7. Instruções de Configuração 

## 8. Conclusão
As estratégias aplicadas resultaram em uma melhora significativa no desempenho das consultas, tornando o sistema mais eficiente para grandes volumes de dados. O uso de **indexação**, **particionamento**, **materialized views** e **tabelas agregadas** foi essencial para otimizar a performance do banco de dados.

