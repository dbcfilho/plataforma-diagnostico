# Documento de Escopo e Requisitos

**Projeto:** Plataforma Inteligente de Diagnóstico de Defasagens Educacionais com Big Data e BI
**Versão:** 1.0
**Data:** 24/05/2025

## 1. Visão Geral e Objetivo do Projeto

Desenvolver uma plataforma web completa, responsiva e funcional para diagnosticar defasagens educacionais (leitura, escrita, matemática) em alunos da rede pública de ensino básico, com foco inicial no contexto de Duque de Caxias, RJ. A plataforma utilizará dados de boletins, frequência, avaliações externas e fatores socioeconômicos para gerar diagnósticos preditivos simples e dashboards interativos de Business Intelligence (BI). O objetivo principal é fornecer uma ferramenta baseada em dados para gestores escolares e professores identificarem lacunas de aprendizagem e tomarem decisões pedagógicas informadas. O sistema servirá como Projeto de Conclusão de Curso (TCC) de Análise e Desenvolvimento de Sistemas, demonstrando a aplicação de tecnologia com impacto social.

## 2. Escopo do Sistema

### 2.1. Funcionalidades Incluídas (MVP):

*   **Gestão de Dados:**
    *   CRUD (Criar, Ler, Atualizar, Deletar) para Escolas, Turmas, Professores e Alunos.
    *   Importação de dados de avaliações e frequência (formato CSV/Excel a ser definido).
    *   Armazenamento de dados socioeconômicos básicos dos alunos.
*   **Autenticação e Autorização:**
    *   Login seguro para Administradores e Professores.
    *   Controle de acesso baseado no perfil do usuário (Admin/Professor).
*   **Processamento e Diagnóstico:**
    *   Cálculo automático de indicadores básicos (média de notas por disciplina, frequência, etc.).
    *   Aplicação de regras de BI simples para classificar alunos em níveis de risco de defasagem (Regular, Atenção, Moderada, Crítica).
    *   Geração de alertas para alunos com risco elevado.
*   **Business Intelligence (BI) e Visualização:**
    *   Dashboards interativos com visualizações de dados educacionais.
    *   Gráficos de desempenho (médias, evolução), frequência e risco.
    *   Filtros dinâmicos nos dashboards (por escola, turma, período, etc.).
    *   Visualização de perfis de aprendizagem simplificados e alertas por aluno.
*   **Relatórios:**
    *   Exportação de dados e relatórios simples em formato CSV.
*   **Interface do Usuário:**
    *   Interface web responsiva (mobile-first).
    *   Painel Administrativo para gestão geral.
    *   Painel do Professor para gestão de turmas e dados pedagógicos.

### 2.2. Funcionalidades Fora do Escopo (Para este MVP):

*   Integração direta e automática com sistemas legados das escolas ou secretarias.
*   Algoritmos complexos de Machine Learning ou IA para predição (foco em regras de BI).
*   Módulo de comunicação direta entre usuários (chat, fórum).
*   Área específica para Alunos ou Responsáveis.
*   Funcionalidades avançadas de gestão de currículo ou plano de aula.
*   Testes automatizados extensivos (foco em testes funcionais manuais para o TCC).
*   Otimizações de performance para altíssima escala (foco na funcionalidade para o volume de dados definido).

## 3. Requisitos Funcionais (RF)

Baseados nos Casos de Uso validados:

*   **RF01:** O sistema deve permitir que Usuários Autenticados realizem login utilizando email/usuário e senha.
*   **RF02:** O sistema deve permitir que Administradores gerenciem (CRUD) os dados de Professores.
*   **RF03:** O sistema deve permitir que Administradores gerenciem (CRUD) os dados de Alunos.
*   **RF04:** O sistema deve permitir que Administradores gerenciem (CRUD) os dados de Escolas.
*   **RF05:** O sistema deve permitir que Administradores gerenciem (CRUD) os dados de Turmas.
*   **RF06:** O sistema deve permitir que Administradores importem dados de avaliações e frequência de fontes externas (ex: planilhas CSV/Excel).
*   **RF07:** O sistema deve permitir que Professores registrem as notas das avaliações de seus alunos por disciplina.
*   **RF08:** O sistema deve permitir que Professores registrem a frequência (faltas) de seus alunos.
*   **RF09:** O sistema deve permitir que Administradores e Professores visualizem dashboards de BI com indicadores educacionais.
*   **RF10:** Os dashboards devem permitir a aplicação de filtros (escola, turma, período, etc.).
*   **RF11:** O sistema deve permitir que Administradores e Professores consultem os diagnósticos individuais dos alunos, incluindo nível de risco e alertas.
*   **RF12:** O sistema deve permitir que Administradores exportem relatórios de dados selecionados em formato CSV.
*   **RF13:** O sistema deve calcular automaticamente indicadores de desempenho (média) e frequência após a inserção/importação de dados.
*   **RF14:** O sistema deve gerar automaticamente diagnósticos e alertas de risco com base em regras predefinidas (limiares de nota e frequência).

## 4. Requisitos Não Funcionais (RNF)

*   **RNF01 (Usabilidade):** A interface do usuário deve ser intuitiva, responsiva e acessível em dispositivos desktop e mobile (mobile-first).
*   **RNF02 (Desempenho):** As consultas aos dashboards e a geração de diagnósticos para o volume de dados definido (1000 alunos) devem ter tempo de resposta aceitável (ex: < 5 segundos para carregamento de dashboards).
*   **RNF03 (Segurança):** O acesso ao sistema deve ser protegido por autenticação. Senhas devem ser armazenadas de forma segura (hashed).
*   **RNF04 (Tecnologia):** O backend será desenvolvido em Python com Django REST Framework. O frontend será desenvolvido em Vue.js (Vue 3 + Composition API). O banco de dados será MySQL.
*   **RNF05 (Manutenibilidade):** O código deve ser bem estruturado, comentado e seguir boas práticas de desenvolvimento para facilitar futuras manutenções ou evoluções.
*   **RNF06 (Documentação):** O projeto deve incluir documentação essencial: README com instruções, Diagramas UML (Casos de Uso, Classes, ER), este Documento de Escopo e Requisitos.
*   **RNF07 (Deploy):** O sistema deve ser configurável para execução local (via Docker Compose) e deve ser possível realizar o deploy em uma plataforma de nuvem gratuita (Render/Railway/Vercel).
*   **RNF08 (Dados):** O sistema utilizará dados sintéticos realistas para demonstração, baseados no contexto educacional de Duque de Caxias e estatísticas públicas.

