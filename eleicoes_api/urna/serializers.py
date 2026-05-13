from rest_framework import serializers
from .models import (Eleitor, Eleicao, Candidato, AptidaoEleitor, RegistroVotacao, Voto)

class EleitorSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()

    class Meta:
        model = Eleitor
        fields = '__all__'

    def valida_cpf(self, value):
        regex_cpf = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
        if not re.match(regex_cpf, value):
            raise serializers.ValidationError(
                "formato == 000.000.000-00."
            )
        return value


class EleicaoSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_candidatos = serializers.SerializerMethodField()
    total_aptos = serializers.SerializerMethodField()

    class Meta:
        model = Eleicao
        fields = [
            'titulo',
            'tipo',
            'status', 
        ]

    def total_candidatos(self, obj):
        return obj.Candidato.count()

    def total_aptos(self, obj):
        return obj.aptos.count()


class CandidatoSerializer(serializers.ModelSerializer):
    eleicao_titulo = serializers.CharField(source='eleicao.titulo', read_only=True)


    class Meta:
        model = Candidato
        fields = '__all__'

    def verifica_numero(self):
        if self.Candidato.numero <= 0:
            raise serializers.ValidationError(
                "0 é para voto em branco"
            )

class AptidaoEleitorSerializer(serializers.ModelSerializer):
    eleitor_nome = serializers.CharField(source='eleitor.nome', read_only=True)
    eleicao_titulo = serializers.CharField(source='eleicao.titulo', read_only=True)


class RegistroVotacaoSerializer(serializers.ModelSerializer):
    eleitor_nome = serializers.CharField(source='eleitor.nome', read_only=True)
    eleicao_titulo = serializers.CharField(source='eleicao.titulo', read_only=True)

    class Meta:
        model = Voto
        fields = [
            'eleicao', 
            'data_hora',
        ]
        read_only_fields = fields 

class VotoSerializer(serializers.ModelSerializer):
    candidato_nome_urna = serializers.CharField(source='candidato.nome_urna', read_only=True, allow_null=True)
    em_branco_display = serializers.CharField(SerializerMethodField que retorna 'BRANCO' se em_branco=True, senão None)
    
    class Meta:
        model = Voto
        fields = [
            'eleicao', 
            'data_hora',
            'candidato',
            'em_branco'
        ]


class VotacaoInputSerializer(serializers.ModelSerializer):
    eleitor_id = serializers.IntegerField()
    eleicao_id = serializers.IntegerField(
    candidato_id = serializers.IntegerField(required=False, allow_null=True)
    em_branco = serializers.BooleanField(default=False, required=False)


