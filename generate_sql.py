import sys
sys.path.append('/home/ubuntu/plataforma_diagnostico')

from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import mysql

# Import Base and all models from db_model
from db_model import Base, Escola, Turma, Professor, Aluno, Avaliacao, Frequencia, Diagnostico

# Define o dialeto MySQL
mysql_dialect = mysql.dialect()

# Cria um engine dummy (não conecta ao banco, só para gerar DDL)
# Usamos pymysql como driver, conforme instalado
engine = create_engine("mysql+pymysql://user:pass@host/db_name", echo=False)

# Gera o SQL para cada tabela
sql_output = """
-- Scripts SQL para criação das tabelas no MySQL
-- Gerado automaticamente a partir do modelo SQLAlchemy

SET FOREIGN_KEY_CHECKS=0;

"""

for table in Base.metadata.sorted_tables:
    # Usamos CreateTable para gerar a instrução SQL específica para a tabela
    # e compilamos com o dialeto MySQL
    create_sql = CreateTable(table).compile(dialect=mysql_dialect)
    sql_output += "DROP TABLE IF EXISTS `" + table.name + "`;\n"
    sql_output += str(create_sql).strip() + ";\n\n"

sql_output += "SET FOREIGN_KEY_CHECKS=1;\n"

# Salva o SQL em um arquivo
output_file = '/home/ubuntu/plataforma_diagnostico/db_scripts/create_tables.sql'
'/home/ubuntu/plataforma_diagnostico/db_scripts/create_tables.sql'
with open(output_file, 'w') as f:
    f.write(sql_output)

print(f"Script SQL gerado com sucesso em: {output_file}")

