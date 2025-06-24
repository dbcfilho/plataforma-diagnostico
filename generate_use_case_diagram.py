from graphviz import Digraph
import os

# Diretório de saída para os documentos
docs_dir = '/home/ubuntu/plataforma_diagnostico/docs'
os.makedirs(docs_dir, exist_ok=True)
output_filename = os.path.join(docs_dir, 'diagrama_casos_uso')

# Cria o grafo do diagrama de casos de uso
dot = Digraph(comment='Diagrama de Casos de Uso - Plataforma Diagnóstico Educacional', format='png')
dot.attr(rankdir='LR', label='Diagrama de Casos de Uso - Plataforma Diagnóstico Educacional', fontsize='20')

# Define os atores
with dot.subgraph(name='cluster_actors') as actors:
    actors.attr(label='Atores', style='filled', color='lightgrey')
    actors.node_attr.update(shape='plaintext') # Usar forma de stick figure não é direto, usar texto
    actors.node('admin', 'Administrador')
    actors.node('prof', 'Professor')
    actors.node('user_auth', 'Usuário Autenticado')
    actors.node('sistema', 'Sistema (Automático)')

# Define os casos de uso (elipses)
with dot.subgraph(name='cluster_usecases') as usecases:
    usecases.attr(label='Casos de Uso')
    usecases.node_attr.update(shape='ellipse', style='filled', color='lightblue')
    usecases.node('uc_login', 'Realizar Login')
    usecases.node('uc_gerenciar_usuarios', 'Gerenciar Usuários\n(Professores, Alunos)')
    usecases.node('uc_gerenciar_estrutura', 'Gerenciar Estrutura Escolar\n(Escolas, Turmas)')
    usecases.node('uc_importar_dados', 'Importar Dados Externos\n(SAEB, Censo)')
    usecases.node('uc_registrar_avaliacoes', 'Registrar Avaliações')
    usecases.node('uc_registrar_frequencia', 'Registrar Frequência')
    usecases.node('uc_visualizar_dashboards', 'Visualizar Dashboards')
    usecases.node('uc_consultar_diagnosticos', 'Consultar Diagnósticos')
    usecases.node('uc_exportar_relatorios', 'Exportar Relatórios')
    usecases.node('uc_calcular_indicadores', 'Calcular Indicadores')
    usecases.node('uc_gerar_alertas', 'Gerar Alertas')

# Define as associações entre atores e casos de uso
# Relações de Generalização (se aplicável, ex: Admin e Prof são Usuários Autenticados)
dot.edge('admin', 'user_auth', arrowhead='empty', style='dashed', label='é um')
dot.edge('prof', 'user_auth', arrowhead='empty', style='dashed', label='é um')

# Associações
dot.edge('user_auth', 'uc_login')

dot.edge('admin', 'uc_gerenciar_usuarios')
dot.edge('admin', 'uc_gerenciar_estrutura')
dot.edge('admin', 'uc_importar_dados')
dot.edge('admin', 'uc_visualizar_dashboards')
dot.edge('admin', 'uc_consultar_diagnosticos')
dot.edge('admin', 'uc_exportar_relatorios')

dot.edge('prof', 'uc_registrar_avaliacoes')
dot.edge('prof', 'uc_registrar_frequencia')
dot.edge('prof', 'uc_visualizar_dashboards')
dot.edge('prof', 'uc_consultar_diagnosticos')

dot.edge('sistema', 'uc_calcular_indicadores')
dot.edge('sistema', 'uc_gerar_alertas')

# Relações <<include>> ou <<extend>> (simplificado aqui)
# Exemplo: Visualizar Dashboards pode incluir filtros
# dot.edge('uc_visualizar_dashboards', 'uc_aplicar_filtros', label='<<include>>', style='dashed')

# Renderiza e salva o diagrama
try:
    dot.render(output_filename, view=False, cleanup=True)
    # Tenta gerar PDF também
    dot.format = 'pdf'
    dot.render(output_filename, view=False, cleanup=True)
    print(f"Diagrama de Casos de Uso gerado em {output_filename}.png e {output_filename}.pdf")
except Exception as e:
    print(f"Erro ao gerar o Diagrama de Casos de Uso: {e}")
    print("Verifique se o Graphviz está instalado e no PATH do sistema.")

