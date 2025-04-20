# Instruções para Implantação do Sistema de Controle de Presença

Este documento contém instruções detalhadas para implantar o Sistema de Controle de Presença em plataformas gratuitas, garantindo que ele fique disponível durante todo o período da atividade (15 de abril a 30 de junho de 2025).

## Opção 1: Implantação no PythonAnywhere (Recomendado)

O PythonAnywhere oferece hospedagem gratuita para aplicações Flask e é fácil de configurar.

### Passo a Passo:

1. **Criar uma conta no PythonAnywhere**
   - Acesse [www.pythonanywhere.com](https://www.pythonanywhere.com)
   - Clique em "Pricing & Signup" e escolha o plano gratuito "Beginner"
   - Complete o processo de registro

2. **Fazer upload dos arquivos**
   - No dashboard do PythonAnywhere, clique em "Files"
   - Crie uma nova pasta chamada "controle-presenca"
   - Faça upload de todos os arquivos do sistema para esta pasta
   - Você pode fazer upload de um arquivo ZIP contendo todo o projeto e depois descompactá-lo

3. **Configurar um ambiente virtual**
   - No dashboard, clique em "Consoles" e depois em "Bash"
   - Execute os seguintes comandos:
     ```
     cd controle-presenca
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

4. **Configurar a aplicação web**
   - No dashboard, clique em "Web"
   - Clique em "Add a new web app"
   - Escolha "Manual configuration" e depois "Python 3.10"
   - Defina o caminho para o código fonte como `/home/seuusuario/controle-presenca`
   - Defina o caminho para o arquivo WSGI como `/home/seuusuario/controle-presenca/wsgi.py`
   - Edite o arquivo WSGI conforme as instruções na página
   - Defina o caminho para o ambiente virtual como `/home/seuusuario/controle-presenca/venv`
   - Clique em "Reload" para iniciar a aplicação

5. **Acessar a aplicação**
   - Sua aplicação estará disponível em `seuusuario.pythonanywhere.com`

## Opção 2: Implantação no Render

O Render oferece hospedagem gratuita para aplicações web e é fácil de integrar com GitHub.

### Passo a Passo:

1. **Criar uma conta no GitHub**
   - Se ainda não tiver, crie uma conta em [github.com](https://github.com)
   - Crie um novo repositório para o projeto

2. **Fazer upload dos arquivos para o GitHub**
   - Clone o repositório localmente
   - Copie todos os arquivos do sistema para o repositório
   - Faça commit e push para o GitHub

3. **Criar uma conta no Render**
   - Acesse [render.com](https://render.com)
   - Registre-se usando sua conta do GitHub

4. **Criar um novo serviço web**
   - No dashboard do Render, clique em "New" e depois em "Web Service"
   - Conecte sua conta do GitHub e selecione o repositório do projeto
   - Defina um nome para o serviço
   - Escolha "Python 3" como ambiente
   - Defina o comando de build como `pip install -r requirements.txt`
   - Defina o comando de start como `gunicorn wsgi:app`
   - Clique em "Create Web Service"

5. **Acessar a aplicação**
   - Sua aplicação estará disponível em um domínio fornecido pelo Render

## Opção 3: Implantação no Railway

O Railway oferece hospedagem gratuita para aplicações web com um processo de implantação simples.

### Passo a Passo:

1. **Criar uma conta no GitHub**
   - Se ainda não tiver, crie uma conta em [github.com](https://github.com)
   - Crie um novo repositório para o projeto

2. **Fazer upload dos arquivos para o GitHub**
   - Clone o repositório localmente
   - Copie todos os arquivos do sistema para o repositório
   - Faça commit e push para o GitHub

3. **Criar uma conta no Railway**
   - Acesse [railway.app](https://railway.app)
   - Registre-se usando sua conta do GitHub

4. **Criar um novo projeto**
   - No dashboard do Railway, clique em "New Project"
   - Escolha "Deploy from GitHub repo"
   - Selecione o repositório do projeto
   - Railway detectará automaticamente que é uma aplicação Python/Flask
   - Clique em "Deploy"

5. **Configurar variáveis de ambiente (se necessário)**
   - No dashboard do projeto, clique em "Variables"
   - Adicione as variáveis de ambiente necessárias

6. **Acessar a aplicação**
   - No dashboard do projeto, clique em "Settings"
   - Na seção "Domains", você encontrará o URL da sua aplicação

## Manutenção e Monitoramento

- Todas estas plataformas oferecem monitoramento básico do status da aplicação
- Verifique regularmente se a aplicação está funcionando corretamente
- Faça backup do banco de dados periodicamente para evitar perda de dados

## Observações Importantes

- As contas gratuitas nestas plataformas podem ter limitações de recursos e tempo de atividade
- Algumas plataformas podem colocar a aplicação em modo de hibernação após períodos de inatividade
- Para garantir disponibilidade contínua, considere acessar a aplicação regularmente

## Suporte

Se precisar de ajuda com a implantação, entre em contato com o desenvolvedor do sistema.
