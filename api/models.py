from django.db import models
from uuid import uuid4
from api.services.crypt import cipher_suite

class Connection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=250)
    host = models.CharField(max_length=30)
    port = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        self.password = cipher_suite().encrypt(self.password.encode())
        super(Connection, self).save(*args, **kwargs)
        
        # decode
        # decrypted_password = cipher_suite.decrypt(encrypted_password)
        # print("Decrypted password:", decrypted_password.decode())

    def __str__(self):
        return self.host


class Source(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=30)
    connection  = models.ForeignKey(Connection,on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title