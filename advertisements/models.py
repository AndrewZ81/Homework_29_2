from django.db.models import Model, CharField, \
    PositiveIntegerField, BooleanField, ForeignKey, CASCADE, ImageField

from users.models import User


class Category(Model):

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    name = CharField(max_length=200, unique=True)


class Advertisement(Model):

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name

    name = CharField(max_length=200)
    author = ForeignKey(User, on_delete=CASCADE)
    price = PositiveIntegerField()
    description = CharField(max_length=2000)
    is_published = BooleanField()
    image = ImageField(null=True, upload_to="images")
    category = ForeignKey(Category, on_delete=CASCADE)
