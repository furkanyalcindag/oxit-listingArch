from django.db import models

from listArch.models.Company import Company
from listArch.models.Definition import Definition
from listArch.models.DefinitionDescription import DefinitionDescription


class CompanyDefinition(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ürün')
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name='Açıklama')

    def __str__(self):
        return '%s %s %s' % (self.company.name, '-', self.definition.key)
