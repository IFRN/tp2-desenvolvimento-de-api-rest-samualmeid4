from django.db import models

# Create your models here.

class Eleitor(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome



class Eleicao(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    TIPO_CHOICES = [
        ('Estudantil', 'estudantil'),
        ('Sind', 'sindical'),
        ('Associacao', 'associacao'),
        ('Condominio', 'condominio'),
        ('Conselho', 'conselho'),
        ('Outra', 'outra')
    ]
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    STATUS_CHOICES = [
        ('Rascunho', 'rascunho'),
        ('Aberta', 'aberta'),
        ('Encerrada', 'encerrada'),
        ('Apurada', 'apurada')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')
    permite_branco = models.BooleanField(default=True)
    criada_por = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='eleicoes_criadas')

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.data_hora_fim <= self.data_hora_inicio:
            return {
                'horarios_inválidos': 'horários fora do range.'
            }


class Candidato(models.Model):
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, related_name='candidatos')
    numero = models.PositiveIntegerField() 
    nome = models.CharField(max_length=150)
    nome_urna = models.CharField(max_length=50)
    partido_ou_chapa = models.CharField(max_length=150, blank=True)
    proposta = models.TextField(blank=True)
    foto_url = models.URLField(blank=True)

    def __str__(self):
        return f'{self.nome}, numero: {self.numero}'

    class Meta:
        unique_together = [('eleicao', 'numero')]



class AptidaoEleitor(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='aptidoes')
    eleicao = models.ForeignKey(Eleicao, on_delete=models.CASCADE, related_name='aptos')
    data_inclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.eleitor

    class Meta:
        unique_together = [('eleitor', 'eleicao')]


class RegistroVotacao(models.Model):
    eleitor = models.ForeignKey(Eleitor, on_delete=models.PROTECT, related_name='registros_votacao')
    eleicao = models.ForeignKey(Eleicao, on_delete=models.PROTECT, related_name='registros_votacao')
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.eleitor}, {self.data_hora}'

    class Meta:
        unique_together = [('eleitor', 'eleicao')] 


class Voto(models.Model):
    eleicao = models.ForeignKey(Eleicao, on_delete=models.PROTECT, related_name='votos')
    candidato = models.ForeignKey(Candidato, on_delete=models.PROTECT, related_name='votos', null=True, blank=True) #— nulo quando o voto é em branco
    em_branco = models.BooleanField(default=False)
    data_hora = models.DateTimeField(auto_now_add=True)
    comprovante_hashCharField = models.CharField(max_length=64, unique=True) # — SHA-256 do token entregue ao eleitor

    def __str__(self):
        return self.eleicao

    def clean(self):
        if self.em_branco == True:
            if self.candidato != None:
                return {
                    'votos_inválidos': 'seu voto não pode estar associado a um candidato.'
                }
        if self.em_branco == False:
            if self.candidato is not None:
                return {
                    'votos_inválidos': 'seu voto precisa estar associado a um candidato.'
                }


        # if self.data_hora > self.Eleicao.data_hora_fim or self.data_hora < self.Eleicao.data_hora_inicio:
        #     return {
        #         'votos_inválidos': 'seu voto foi feito fora de horário.'
        #     }


