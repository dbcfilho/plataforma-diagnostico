# Wireframes (Descrição Textual)

Este documento descreve a estrutura e os principais elementos das telas da Plataforma Inteligente de Diagnóstico de Defasagens Educacionais.

## 1. Tela de Login

*   **Layout:** Centralizado, simples.
*   **Elementos:**
    *   Logo da Plataforma (Topo)
    *   Título: "Login"
    *   Campo de Entrada: "Email" ou "Usuário"
    *   Campo de Entrada: "Senha" (tipo password)
    *   Checkbox: "Lembrar-me" (Opcional)
    *   Botão: "Entrar"
    *   Link: "Esqueceu sua senha?" (Opcional)

## 2. Painel Administrativo (Visão Geral)

*   **Layout:** Barra lateral de navegação à esquerda, área de conteúdo principal à direita.
*   **Barra Lateral (Menu):**
    *   Dashboard Geral
    *   Gerenciar Escolas
    *   Gerenciar Turmas
    *   Gerenciar Professores
    *   Gerenciar Alunos
    *   Importar Dados
    *   Relatórios
    *   Configurações (Opcional)
    *   Sair
*   **Área de Conteúdo (Exemplo: Dashboard Geral):**
    *   Título: "Dashboard Geral"
    *   Cards de Resumo (KPIs): Número de Escolas, Turmas, Alunos, Professores, Alunos em Risco.
    *   Gráfico 1: Distribuição de Alunos por Nível de Risco (Pizza)
    *   Gráfico 2: Média de Desempenho Geral por Disciplina (Barras)
    *   Tabela: Últimos Alertas Gerados
*   **Área de Conteúdo (Exemplo: Gerenciar Alunos):**
    *   Título: "Gerenciar Alunos"
    *   Botão: "Adicionar Novo Aluno"
    *   Filtros/Busca: Por Nome, Escola, Turma, Risco.
    *   Tabela de Alunos:
        *   Colunas: Nome, Escola, Turma, Série, Risco Atual, Ações (Editar, Ver Detalhes, Excluir).
        *   Paginação.

## 3. Painel do Professor (Visão Geral)

*   **Layout:** Similar ao Admin, com barra lateral e área de conteúdo.
*   **Barra Lateral (Menu):**
    *   Minhas Turmas
    *   Lançar Avaliações
    *   Registrar Frequência
    *   Consultar Diagnósticos
    *   Meu Perfil (Opcional)
    *   Sair
*   **Área de Conteúdo (Exemplo: Minhas Turmas):**
    *   Título: "Minhas Turmas"
    *   Seleção de Turma (Dropdown ou Lista)
    *   Card de Resumo da Turma: Nº Alunos, Média Geral, % Faltas, Alunos em Risco.
    *   Tabela de Alunos da Turma:
        *   Colunas: Nome, Última Média, Faltas Bimestre, Risco, Ações (Ver Diagnóstico).
*   **Área de Conteúdo (Exemplo: Lançar Avaliações):**
    *   Título: "Lançar Avaliações"
    *   Seleção: Turma, Disciplina, Bimestre/Data.
    *   Tabela Editável: Lista de Alunos da Turma com campo para inserir a Nota.
    *   Botão: "Salvar Notas"

## 4. Dashboards de BI (Exemplo - Visão Admin)

*   **Layout:** Área de conteúdo principal, com filtros proeminentes.
*   **Filtros (Topo ou Lateral):**
    *   Período (Ano, Bimestre)
    *   Escola
    *   Turma
    *   Disciplina
    *   Nível de Risco
*   **Área de Conteúdo:**
    *   Título: "Análise de Desempenho e Risco"
    *   Gráfico 1: Evolução da Média de Notas por Disciplina (Linhas)
    *   Gráfico 2: Distribuição de Alunos por Faixa de Risco (Pizza/Donut)
    *   Gráfico 3: Comparativo de Desempenho entre Escolas (Barras)
    *   Mapa (Simulado): Mapa de Duque de Caxias com escolas coloridas por índice de risco.
    *   Heatmap: Desempenho por Turma x Disciplina.
    *   Tabela: Detalhamento de Alunos em Risco Crítico com filtros aplicados.

---
*Observação: Estes são esboços iniciais. O design final incluirá mais detalhes visuais, cores e interatividade.*
