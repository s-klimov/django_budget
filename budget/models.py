from taggit.managers import TaggableManager
from timestamps.models import models, Model


class BankAccount(Model):
    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True, unique=True
    )
    incoming_balance = models.DecimalField(verbose_name="входящий остаток", max_digits=10, decimal_places=2)

    @property
    def outcoming_balance(self):
        return self.incoming_balance + \
               sum([key["value"] for key in self.income_set.values("value")]) - \
               sum([key["value"] for key in self.expenditure_set.values("value")])

    class Meta:
        ordering = ("name",)
        verbose_name = "счет"
        verbose_name_plural = "счета"

    def __str__(self):
        return self.name


class CashFlow(Model):
    value = models.DecimalField(verbose_name="сумма", max_digits=10, decimal_places=2)
    bank_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, verbose_name="счет"
    )
    comment = models.CharField(
        max_length=200, verbose_name="комментарий", null=True, blank=True
    )
    tags = TaggableManager()

    class Meta:
        abstract = True

    def __str__(self):
        return "{} {} {}".format(
            self.__class__.__name__, self.tags, self.value
        )


class Income(CashFlow):

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "доход"
        verbose_name_plural = "доходы"


class Expenditure(CashFlow):

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "расход"
        verbose_name_plural = "расходы"
