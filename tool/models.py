from django.db import models
import django.utils.timezone

class server_details(models.Model):
    company_name=models.TextField(max_length=100,null=True,default=None)
    server_name=models.TextField(max_length=100,null=True,default=None)
    api_url=models.TextField(max_length=1000,null=True,default=None)
    server_ip=models.TextField(max_length=100,null=True,default=None)
    server_id=models.TextField(max_length=100,null=True,default=None)
    server_password=models.TextField(max_length=100,null=True,default=None)
    description=models.TextField(max_length=1000,null=True,default=None)
    status=models.BooleanField(null=True,default=True)

    def __str__(self):
        return self.server_name

class master_details(models.Model):
    server=models.ForeignKey(server_details,on_delete=models.CASCADE,null=True)
    mt5_id=models.IntegerField(null=True,default=None)
    name=models.TextField(max_length=100,null=True,default=None)
    password=models.TextField(max_length=100,null=True,default=None)
    commission=models.FloatField(null=True,default=False)
    description=models.TextField(max_length=1000,null=True,default=None)
    set_identical=models.BooleanField(null=True,default=False)
    status=models.BooleanField(null=True,default=True)

    def __str__(self):
        return self.name


class copier_details(models.Model):
    server = models.ForeignKey(server_details, on_delete=models.CASCADE, null=True)
    master = models.ForeignKey(master_details, on_delete=models.CASCADE, null=True)
    mt5_id = models.IntegerField(null=True, default=None)
    name = models.TextField(max_length=100, null=True, default=None)
    password = models.TextField(max_length=100, null=True, default=None)
    commission = models.FloatField(null=True, default=False)
    risk = models.TextField(max_length=100,null=True, default=False)

    stop_loss = models.BooleanField(null=True, default=False)
    take_profit = models.BooleanField(null=True, default=False)
    reverse_trade = models.BooleanField(null=True, default=False)
    status = models.BooleanField(null=True, default=True)

    def __str__(self):
        return self.name

