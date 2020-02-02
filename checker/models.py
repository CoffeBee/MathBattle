from django.db import models
import os

# Create your models here.
class Checker(models.Model):

    class Meta:
        verbose_name = "Проверяющая программа"
        verbose_name_plural = "Проверяющие программы"

    def __str__(self):
        return os.path.basename(self.code.name)

    def checkAns(self, userans, ans) -> bool:
    	codestr = self.code.read()
    	return eval(codestr)

    code = models.FileField(upload_to='uploads/checkers', verbose_name="Файл")
