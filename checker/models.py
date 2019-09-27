from django.db import models
import os

# Create your models here.
class Checker(models.Model):

    class Meta:
        verbose_name = "Checker"
        verbose_name_plural = "Checkers"

    def __str__(self):
        return os.path.basename(self.code.name)

    def checkAns(self, userans, ans) -> bool:
    	codestr = open('../{}'.format(self.code.name)).read()
    	return eval(codestr)

    code = models.FileField(upload_to='uploads/checkers')
