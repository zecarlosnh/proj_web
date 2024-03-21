from django.db import models

# Create your models here.

class Caminhos_arquivos(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome = models.TextField(blank=True, null=True)
    assinaturas = models.TextField(blank=True, null=True)
    caminhopadrao = models.TextField(blank=True, null=True)
    caminho_os = models.TextField(blank=True, null=True)
    class Meta:
        db_table = 'caminhos_arquivos'
        
        
class Veiculos(models.Model):
    id = models.AutoField(primary_key=True)
    modelo = models.TextField(blank=False)
    placa = models.TextField(blank=False)
    
    class Meta:
        db_table = 'veiculos'
        

class Motoristas(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.TextField(blank=False)
   
    
    class Meta:
        db_table = 'motoristas'
        
        
class Ordem_abastecimento(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.IntegerField(blank=False)
    data = models.DateTimeField()
    veiculo = models.TextField(blank=False)
    motorista = models.TextField(blank=False)
    valor = models.TextField(blank=False)
    
    class Meta:
        db_table = 'ordemabastecimento'