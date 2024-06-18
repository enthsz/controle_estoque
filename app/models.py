from django.db import models


class Product(models.Model):
    nome = models.CharField(max_length=255)
    quantidade_em_estoque = models.IntegerField()
    preco_de_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_de_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_criada = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = 'Product'
        ordering = ['data_criada']

    def __str__(self):
        return self.nome


class Sale(models.Model):
    produto_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    vendidos = models.IntegerField()
    lucro = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_venda = models.DateTimeField(auto_now_add=True)


    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.produto_id.quantidade_em_estoque >= int(self.vendidos):
            super(Sale, self).save(force_insert, force_update, *args, **kwargs)
        return
    

    







