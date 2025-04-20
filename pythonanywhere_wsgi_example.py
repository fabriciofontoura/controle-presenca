import sys
import os

# Adicione o diretório do seu projeto ao path do Python
path = '/home/fabriciofontoura/controle-presenca'
if path not in sys.path:
    sys.path.append(path)

# Defina a variável de ambiente para o Flask
os.environ['FLASK_APP'] = 'app.py'

# Importe a variável app do seu arquivo app.py
from app import app as application
