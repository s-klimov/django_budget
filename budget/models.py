import uuid

from django.db.models import Sum, Q, F
from django.utils import timezone
from taggit.managers import TaggableManager
from timestamps.models import models, Model


class BankAccount(Model):
    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True, unique=True
    )
    incoming_balance = models.DecimalField(verbose_name="входящий остаток", max_digits=10, decimal_places=2)
    is_active = models.BooleanField(verbose_name='счет используется', default=True)

    @property
    def outcoming_balance(self):
        incomes = self.income_set.aggregate(Sum("value"))["value__sum"] or 0
        expenditures = self.expenditure_set.aggregate(Sum("value"))["value__sum"] or 0
        transfers_from = self.transfer_set.filter(bank_account=self).aggregate(Sum("value"))["value__sum"] or 0
        transfers_to = self.transfers_to.filter(bank_account_to=self).aggregate(Sum("value"))["value__sum"] or 0
        return self.incoming_balance + incomes + transfers_to - expenditures - transfers_from

    class Meta:
        ordering = ("name",)
        verbose_name = "счет"
        verbose_name_plural = "счета"

    def __str__(self):
        return self.name


class Category(Model):
    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True, unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class IncomeCategory(Category):

    class Meta:
        ordering = ("name",)
        verbose_name = "группа доходов"
        verbose_name_plural = "группы доходов"


class ExpenditureCategory(Category):

    class Meta:
        ordering = ("name",)
        verbose_name = "группа расходов"
        verbose_name_plural = "группы расходов"


class SubCategory(Model):

    name = models.CharField(
        max_length=200, verbose_name="название", db_index=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return "{} -> {}".format(self.category.name, self.name)


class IncomeSubCategory(SubCategory):
    category = models.ForeignKey(
        IncomeCategory, on_delete=models.CASCADE, verbose_name="категория"
    )

    class Meta:
        ordering = ("category__name", "name")
        unique_together = ('name', 'category')
        verbose_name = "подкатегория доходов"
        verbose_name_plural = "подкатегории доходов"


class ExpenditureSubCategory(SubCategory):
    category = models.ForeignKey(
        ExpenditureCategory, on_delete=models.CASCADE, verbose_name="категория"
    )

    class Meta:
        ordering = ("category__name", "name")
        unique_together = ('name', 'category')
        verbose_name = "подкатегория расходов"
        verbose_name_plural = "подкатегории расходов"


class CashFlow(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.DecimalField(verbose_name="сумма", max_digits=10, decimal_places=2)
    bank_account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, verbose_name="счет"
    )
    operation_date = models.DateField(
        default=timezone.now, verbose_name="дата"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return "{} {}".format(
            self.__class__._meta.verbose_name.title(), self.value
        )


class Income(CashFlow):
    sub_category = models.ForeignKey(
        IncomeSubCategory, on_delete=models.CASCADE, verbose_name="категория"
    )

    class Meta:
        ordering = ("-operation_date",)
        verbose_name = "доход"
        verbose_name_plural = "доходы"


class Expenditure(CashFlow):
    sub_category = models.ForeignKey(
        ExpenditureSubCategory, on_delete=models.CASCADE, verbose_name="категория"
    )
    tags = TaggableManager(
        verbose_name="для расширенных отчетов",
        blank=True,
        help_text="введите через запятую названия аналитических групп"
    )

    class Meta:
        ordering = ("-operation_date",)
        verbose_name = "расход"
        verbose_name_plural = "расходы"


class Transfer(CashFlow):
    bank_account_to = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, related_name="transfers_to", verbose_name="на какой счет"
    )

    class Meta:
        ordering = ("-operation_date",)
        constraints = [
            models.CheckConstraint(
                check=~Q(bank_account=F("bank_account_to")),
                name='нельзя переводить деньги между одним и тем же счетом'
            )
        ]
        verbose_name = "перевод между счетами"
        verbose_name_plural = "переводы между счетами"
