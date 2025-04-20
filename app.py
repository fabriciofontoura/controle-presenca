import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-do-app'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///controle_presenca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelos
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'aluno' ou 'responsavel'
    agendamentos = db.relationship('Agendamento', backref='usuario', lazy=True)
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
        
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    observacoes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pendente')  # 'pendente', 'aprovado', 'rejeitado', 'concluido'
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.tipo == 'aluno':
            return redirect(url_for('dashboard_aluno'))
        else:
            return redirect(url_for('dashboard_responsavel'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            if usuario.tipo == 'aluno':
                return redirect(url_for('dashboard_aluno'))
            else:
                return redirect(url_for('dashboard_responsavel'))
        else:
            flash('Email ou senha inválidos', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')
        
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Email já cadastrado', 'danger')
            return redirect(url_for('cadastro'))
        
        novo_usuario = Usuario(nome=nome, email=email, tipo=tipo)
        novo_usuario.set_senha(senha)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/dashboard/aluno')
@login_required
def dashboard_aluno():
    if current_user.tipo != 'aluno':
        return redirect(url_for('dashboard_responsavel'))
    
    agendamentos = Agendamento.query.filter_by(usuario_id=current_user.id).order_by(Agendamento.data.desc()).all()
    
    # Calcular horas totais
    horas_totais = 0
    for agendamento in agendamentos:
        if agendamento.status == 'concluido':
            inicio = datetime.combine(datetime.today(), agendamento.hora_inicio)
            fim = datetime.combine(datetime.today(), agendamento.hora_fim)
            duracao = (fim - inicio).total_seconds() / 3600
            horas_totais += duracao
    
    return render_template('dashboard_aluno.html', agendamentos=agendamentos, horas_totais=horas_totais)

@app.route('/dashboard/responsavel')
@login_required
def dashboard_responsavel():
    if current_user.tipo != 'responsavel':
        return redirect(url_for('dashboard_aluno'))
    
    agendamentos_pendentes = Agendamento.query.filter_by(status='pendente').order_by(Agendamento.data.asc()).all()
    todos_agendamentos = Agendamento.query.order_by(Agendamento.data.desc()).all()
    alunos = Usuario.query.filter_by(tipo='aluno').all()
    
    # Calcular horas por aluno
    horas_por_aluno = {}
    for aluno in alunos:
        horas_por_aluno[aluno.id] = 0
        agendamentos_aluno = Agendamento.query.filter_by(usuario_id=aluno.id, status='concluido').all()
        for agendamento in agendamentos_aluno:
            inicio = datetime.combine(datetime.today(), agendamento.hora_inicio)
            fim = datetime.combine(datetime.today(), agendamento.hora_fim)
            duracao = (fim - inicio).total_seconds() / 3600
            horas_por_aluno[aluno.id] += duracao
    
    return render_template('dashboard_responsavel.html', 
                          agendamentos_pendentes=agendamentos_pendentes,
                          todos_agendamentos=todos_agendamentos,
                          alunos=alunos,
                          horas_por_aluno=horas_por_aluno)

@app.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar():
    if current_user.tipo != 'aluno':
        return redirect(url_for('dashboard_responsavel'))
    
    if request.method == 'POST':
        data_str = request.form.get('data')
        hora_inicio_str = request.form.get('hora_inicio')
        hora_fim_str = request.form.get('hora_fim')
        observacoes = request.form.get('observacoes')
        
        # Validar data (apenas dias úteis entre 15/04 e 30/06)
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        data_inicio = datetime(2025, 4, 15).date()
        data_fim = datetime(2025, 6, 30).date()
        
        if data < data_inicio or data > data_fim:
            flash('A data deve estar entre 15/04/2025 e 30/06/2025', 'danger')
            return redirect(url_for('agendar'))
        
        if data.weekday() >= 5:  # 5 = Sábado, 6 = Domingo
            flash('Apenas dias úteis (segunda a sexta) são permitidos', 'danger')
            return redirect(url_for('agendar'))
        
        # Validar horário (entre 7h e 19h)
        hora_inicio = datetime.strptime(hora_inicio_str, '%H:%M').time()
        hora_fim = datetime.strptime(hora_fim_str, '%H:%M').time()
        
        hora_min = datetime.strptime('07:00', '%H:%M').time()
        hora_max = datetime.strptime('19:00', '%H:%M').time()
        
        if hora_inicio < hora_min or hora_fim > hora_max:
            flash('O horário deve estar entre 7h e 19h', 'danger')
            return redirect(url_for('agendar'))
        
        if hora_inicio >= hora_fim:
            flash('A hora de início deve ser anterior à hora de término', 'danger')
            return redirect(url_for('agendar'))
        
        # Verificar conflito de horários
        agendamentos_existentes = Agendamento.query.filter_by(data=data).all()
        for agendamento in agendamentos_existentes:
            if (hora_inicio < agendamento.hora_fim and hora_fim > agendamento.hora_inicio):
                flash('Existe um conflito de horário com outro agendamento', 'danger')
                return redirect(url_for('agendar'))
        
        # Criar novo agendamento
        novo_agendamento = Agendamento(
            usuario_id=current_user.id,
            data=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            observacoes=observacoes,
            status='pendente'
        )
        
        db.session.add(novo_agendamento)
        db.session.commit()
        
        flash('Agendamento solicitado com sucesso!', 'success')
        return redirect(url_for('dashboard_aluno'))
    
    return render_template('agendar.html')

@app.route('/agendamento/aprovar/<int:id>')
@login_required
def aprovar_agendamento(id):
    if current_user.tipo != 'responsavel':
        return redirect(url_for('dashboard_aluno'))
    
    agendamento = Agendamento.query.get_or_404(id)
    agendamento.status = 'aprovado'
    db.session.commit()
    
    flash('Agendamento aprovado com sucesso!', 'success')
    return redirect(url_for('dashboard_responsavel'))

@app.route('/agendamento/rejeitar/<int:id>')
@login_required
def rejeitar_agendamento(id):
    if current_user.tipo != 'responsavel':
        return redirect(url_for('dashboard_aluno'))
    
    agendamento = Agendamento.query.get_or_404(id)
    agendamento.status = 'rejeitado'
    db.session.commit()
    
    flash('Agendamento rejeitado com sucesso!', 'success')
    return redirect(url_for('dashboard_responsavel'))

@app.route('/agendamento/concluir/<int:id>')
@login_required
def concluir_agendamento(id):
    if current_user.tipo != 'responsavel':
        return redirect(url_for('dashboard_aluno'))
    
    agendamento = Agendamento.query.get_or_404(id)
    agendamento.status = 'concluido'
    db.session.commit()
    
    flash('Presença registrada com sucesso!', 'success')
    return redirect(url_for('dashboard_responsavel'))

# Inicialização do banco de dados e criação do usuário responsável
def init_db():
    with app.app_context():
        db.create_all()
        
        # Verificar se já existe um responsável
        responsavel = Usuario.query.filter_by(email='responsavel@clinica.com').first()
        if not responsavel:
            responsavel = Usuario(
                nome='Responsável',
                email='responsavel@clinica.com',
                tipo='responsavel'
            )
            responsavel.set_senha('123456')
            db.session.add(responsavel)
            db.session.commit()

# Inicializar o banco de dados
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
