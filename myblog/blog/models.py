from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class Post(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Заголовок записи', max_length=256)
    description = models.TextField('Описание', max_length=8000)
    date = models.DateField('', blank=True, null=True)
    img = models.ImageField('Изображение', upload_to='media/image/%Y/%m/%d/')

    def __str__(self):
        return f'{self.title}, {self.users}'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'



class Comments(models.Model):
    users_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, verbose_name='Публикация', on_delete=models.CASCADE)
    text_comments = models.TextField("Комментарий")

    def __str__(self):
        return f'{self.users_comment}, {self.post_id}, {self.text_comments}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Likes(models.Model):
    ip = models.CharField('IP-адрес', max_length=100)
    pos = models.ForeignKey(Post, verbose_name='Публикация', on_delete=models.CASCADE)


