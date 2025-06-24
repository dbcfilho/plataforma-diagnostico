# Plataforma de Diagnóstico Educacional - TCC

Este projeto consiste em uma plataforma web para diagnóstico educacional, desenvolvida como Trabalho de Conclusão de Curso (TCC). A plataforma visa auxiliar gestores e professores na identificação de alunos com defasagem de aprendizagem e no acompanhamento de indicadores educacionais em Duque de Caxias.

## Visão Geral

A plataforma é composta por:

*   **Backend (Django/DRF):** API RESTful responsável pela lógica de negócio, gerenciamento de dados (escolas, turmas, alunos, professores, avaliações, frequência, diagnósticos), autenticação (JWT), cálculo de indicadores de BI e endpoints para os dashboards.
*   **Frontend (Vue.js/Vite):** Interface web interativa e responsiva para visualização dos dados, dashboards de BI (com gráficos Plotly.js e mapa Leaflet), gerenciamento de entidades (para administradores) e funcionalidades específicas para professores.
*   **Banco de Dados (MySQL - Modelo):** A estrutura do banco de dados foi modelada e um script SQL para criação das tabelas (`db_scripts/create_tables.sql`) foi gerado. A configuração da conexão deve ser feita no `backend/core/settings.py`.
*   **Dados Sintéticos:** Dados de exemplo foram gerados (`data/`) para popular o sistema e demonstrar as funcionalidades.

## Funcionalidades Principais

*   **Autenticação:** Login seguro para Administradores e Professores.
*   **Gerenciamento (Admin):** CRUD para Escolas, Turmas, Alunos, Professores.
*   **Importação de Dados (Admin):** Funcionalidade para importar dados de avaliações/frequência (endpoint `/api/import-data/`).
*   **Registro de Dados (Professor):** Interface para registrar avaliações e frequência (funcionalidade básica implementada).
*   **Dashboards de BI (Admin/Professor):**
    *   Distribuição de Risco (Gráfico de Pizza)
    *   Evolução Temporal de Desempenho (Gráfico de Linha)
    *   Desempenho por Disciplina (Heatmap)
    *   Mapa de Risco das Escolas (Mapa Leaflet)
    *   Indicadores Chave (KPI Cards)
    *   Alertas de Risco (Alert Cards)
    *   Filtros interativos (por escola, turma, etc. - implementação básica).
*   **Exportação de Dados (Admin):** Exportar dados de alunos em formato CSV (endpoint `/api/export-students/`).

## Estrutura do Projeto

```
plataforma_diagnostico/
├── backend/
│   ├── api/            # App Django principal (models, views, serializers, urls)
│   ├── core/           # Configurações do projeto Django (settings, urls)
│   └── manage.py       # Utilitário de gerenciamento Django
├── data/               # Dados sintéticos em CSV
├── db_scripts/         # Scripts SQL (ex: create_tables.sql)
├── docs/               # Documentação (Diagramas ER, Casos de Uso, Classes, Wireframes, Escopo)
├── frontend/
│   └── app/            # Projeto Vue.js (Vite)
│       ├── public/
│       ├── src/
│       │   ├── assets/
│       │   ├── components/ # Componentes Vue (common, layout, bi)
│       │   ├── router/     # Configuração do Vue Router
│       │   ├── stores/     # Stores Pinia (auth)
│       │   ├── views/      # Views/Páginas da aplicação
│       │   ├── App.vue
│       │   ├── index.css   # CSS global (com Tailwind)
│       │   └── main.js     # Ponto de entrada Vue
│       ├── index.html
│       ├── package.json
│       ├── postcss.config.js
│       ├── tailwind.config.js
│       └── vite.config.js
├── .gitignore
└── README.md           # Este arquivo
```

## Como Executar (Desenvolvimento)

**Pré-requisitos:**
*   Python 3.9+
*   Node.js 18+ / npm
*   MySQL (ou outro banco de dados configurado no Django)

**Backend:**
1.  Navegue até a pasta `backend`: `cd plataforma_diagnostico/backend`
2.  Crie e ative um ambiente virtual: `python -m venv venv && source venv/bin/activate` (ou `venv\Scripts\activate` no Windows)
3.  Instale as dependências: `pip install -r requirements.txt` (Nota: `requirements.txt` precisa ser gerado)
4.  Configure a conexão com o banco de dados em `core/settings.py`.
5.  Aplique as migrações (se estiver usando migrações Django): `python manage.py migrate` (Ou execute o script `db_scripts/create_tables.sql` diretamente no seu banco de dados MySQL).
6.  (Opcional) Crie um superusuário: `python manage.py createsuperuser`
7.  Inicie o servidor de desenvolvimento: `python manage.py runserver` (geralmente na porta 8000)

**Frontend:**
1.  Navegue até a pasta `frontend/app`: `cd ../frontend/app` (a partir da pasta backend)
2.  Instale as dependências: `npm install`
3.  Verifique a variável `VITE_API_BASE_URL` no arquivo `.env` (crie-o se não existir) e aponte para a URL do seu backend (ex: `VITE_API_BASE_URL=http://127.0.0.1:8000`)
4.  Inicie o servidor de desenvolvimento Vite: `npm run dev` (geralmente na porta 5173)

**Acesso:**
*   Abra o navegador e acesse a URL do frontend (ex: `http://localhost:5173`).

## Documentação Adicional

Consulte a pasta `docs/` para:
*   Diagrama Entidade-Relacionamento (`diagrama_er.pdf`)
*   Diagrama de Casos de Uso (`diagrama_casos_uso.pdf`)
*   Diagrama de Classes (`classes_PlataformaDiagnostico.png`)
*   Wireframes (`wireframes.md`)
*   Escopo e Requisitos (`escopo_requisitos.md`)

## Próximos Passos / Melhorias

*   Implementação completa dos filtros nos dashboards.
*   Testes unitários e de integração mais abrangentes.
*   Refinamento da interface do usuário e experiência do usuário.
*   Implementação de funcionalidades de edição/deleção nos painéis Admin/Professor.
*   Deploy em ambiente de produção.
*   Melhorias na segurança e tratamento de erros.

