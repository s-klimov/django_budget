from timestamps.models import models, Model


class BankAccount(Model):
    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True, unique=True
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "счет"
        verbose_name_plural = "счета"

    def __repr__(self):
        return self.name


class IncomeGroup(Model):
    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True, unique=True
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "группа доходов"
        verbose_name_plural = "группы доходов"

    def __repr__(self):
        return self.name


class IncomeCategory(Model):
    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True, unique=True
    )
    group = models.ForeignKey(
        IncomeGroup, related_name="categories", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "категория доходов"
        verbose_name_plural = "категории доходов"

    def __repr__(self):
        return self.name


class Income(Model):
    value = models.DecimalField(verbose_name="доход", decimal_places=2)
    bank_account = models.ForeignKey(
        BankAccount, related_name="incomes", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        IncomeCategory, related_name="incomes", on_delete=models.CASCADE
    )
    comment = models.CharField(
        max_length=200, verbose_name="комментарий", null=True, blank=True
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "доход"
        verbose_name_plural = "доходы"

    def __repr__(self):
        return "{} {} {}".format(
            self.__class__.__name__, self.category.name, self.value
        )


class ExpenditureGroup(Model):
    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True, unique=True
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "группа расходов"
        verbose_name_plural = "группы расходов"

    def __repr__(self):
        return self.name


class ExpenditureCategory(Model):
    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True, unique=True
    )
    group = models.ForeignKey(
        IncomeGroup, related_name="categories", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "категория расходов"
        verbose_name_plural = "категории расходов"

    def __repr__(self):
        return self.name


class Expenditure(Model):
    value = models.DecimalField(verbose_name="расход", decimal_places=2)
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
        ordering = ("-created_at",)
        verbose_name = "расход"
        verbose_name_plural = "расходы"

    def __repr__(self):
        return "{} {} {}".format(
            self.__class__.__name__, self.category.name, self.value
        )
