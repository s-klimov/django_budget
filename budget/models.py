from timestamps.models import models, Model


class BankAccount(Model):
    name = models.CharField(max_length=200, verbose_name='название', db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'счет'
        verbose_name_plural = 'счета'

    def __repr__(self):
        return self.name


class IncomeCategory(Model):
    name = models.CharField(max_length=200, verbose_name='название', db_index=True, unique=True)

    def __repr__(self):
        return self.name


class Income(Model):
    value = models.DecimalField(verbose_name='доход', decimal_places=2)
    comment = models.CharField(max_length=200, verbose_name='комментарий', null=True, blank=True)


class ExpenditureCategory(Model):
    name = models.CharField(max_length=200, verbose_name='название', db_index=True, unique=True)

    def __repr__(self):
        return self.name


class Expenditure(Model):
    value = models.DecimalField(verbose_name='расход', decimal_places=2)
    comment = models.CharField(max_length=200, verbose_name='комментарий', null=True, blank=True)
