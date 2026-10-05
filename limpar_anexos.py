import os
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from certificados.models import Certificado

class Command(BaseCommand):
    help = 'Exclui anexos físicos de certificados com mais de 2 meses de criação'

    def handle(self, *args, **kwargs):
        data_limite = timezone.now() - timedelta(days=1)

        certificados_antigos = Certificado.objects.filter(
            data_cadastro__lte=data_limite
        ).exclude(arquivo='')

        arquivos_apagados = 0

        for certificado in certificados_antigos:
            if certificado.arquivo and os.path.isfile(certificado.arquivo.path):
                os.remove(certificado.arquivo.path)
                
                certificado.arquivo = None 
                certificado.save()
                
                arquivos_apagados += 1

        self.stdout.write(self.style.SUCCESS(f'Rotina finalizada! {arquivos_apagados} anexos apagados.'))