from timestamps.models import models, Model


class BankAccount(Model):
    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True, unique=True
    )
    incoming_balance = models.DecimalField(verbose_name="сумма", decimal_places=2)

    class Meta:
        ordering = ("name",)
        verbose_name = "счет"
        verbose_name_plural = "счета"

    def __repr__(self):
        return self.name


class Group(Model):
    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True, unique=True
    )

    class Meta:
        abstract = True

    def __repr__(self):
        return self.name


class IncomeGroup(Group):

    class Meta:
        ordering = ("name",)
        verbose_name = "группа доходов"
        verbose_name_plural = "группы доходов"


class ExpenditureGroup(Group):

    class Meta:
        ordering = ("name",)
        verbose_name = "группа расходов"
        verbose_name_plural = "группы расходов"


class Category(Model):

    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True
    )
    group = models.ForeignKey(
        IncomeGroup, related_name="categories", on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
        unique_together = ('name', 'group')

    def __repr__(self):
        return "{}/{}".format(self.group.name, self.name)


class IncomeCategory(Category):

    class Meta:
        ordering = ("name",)
        verbose_name = "категория доходов"
        verbose_name_plural = "категории доходов"


class ExpenditureCategory(Category):

    class Meta:
        ordering = ("name",)
        verbose_name = "категория расходов"
        verbose_name_plural = "категории расходов"


class CashFlow(Model):
    value = models.DecimalField(verbose_name="сумма", decimal_places=2)
    bank_account = models.ForeignKey(
        BankAccount, related_name="expenditures", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        ExpenditureCategory, related_name="expenditures", on_delete=models.CASCADE
    )
    comment = models.CharField(
        max_length=200, verbose_name="комментарий", null=True, blank=True
    )

    class Meta:
        abstract = True

    def __repr__(self):
        return "{} {} {}".format(
            self.__class__.__name__, self.category.name, self.value
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
