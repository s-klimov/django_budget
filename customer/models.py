from django.contrib.auth.models import User
from timestamps.models import models, Model


class Profile(Model):
    user = models.ForeignKey(User, verbose_name="пользователь", db_index=True, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name="аватар")

    def __str__(self):
        return "{}".format(self.user.first_name if self.user.first_name else self.user.email)


class Household(Model):
    user = models.ForeignKey(User, verbose_name="пользователь", db_index=True, on_delete=models.CASCADE)
    member = models.ManyToManyField(Profile, verbose_name="участники домохозяйства")

    def __str__(self):
        return "Домохозяйтсво {}".format(self.user)
