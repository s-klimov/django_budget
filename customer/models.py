from django.contrib.auth.models import User
from timestamps.models import models, Model


class Profile(Model):
    user = models.OneToOneField(User, verbose_name="пользователь", db_index=True, on_delete=models.CASCADE)
    avatar = models.ImageField(verbose_name="аватар", null=True, blank=True)

    def __str__(self):
        return "{}".format(self.user.first_name if self.user.first_name else self.user.email)

    @property
    def name(self):
        return str(self)

    @property
    def surname(self):
        return self.user.last_name

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"


class Household(Model):
    user = models.ForeignKey(User, verbose_name="пользователь", db_index=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(Profile, verbose_name="участники домохозяйства")

    def __str__(self):
        return "Домохозяйтсво {}".format(self.user)

    @property
    def name(self):
        return str(self)

    class Meta:
        verbose_name = "домохозяйство"
        verbose_name_plural = "домохозяйства"