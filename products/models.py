from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.text import slugify


# class Product(models.Model):
#     title = models.CharField(max_length=200)
#     url = models.URLField()
#     pub_date = models.DateTimeField()
#     votes_total = models.IntegerField(default=1)
#     image = models.ImageField(upload_to='images/')
#     icon = models.ImageField(upload_to='images/')
#     body = models.TextField()
#     hunter = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.title
#
#     def upvote(self):
#         self.votes_total += 1
#         self.save()



class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    category_slug = models.SlugField()

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_name_slug = models.SlugField()
    price = models.PositiveBigIntegerField()
    description = models.TextField()
    features = models.TextField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    users_votes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='products_votes',
                                         blank=True)
    total_votes = models.PositiveIntegerField(db_index=True,
                                              default=0)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):  # new
        if not self.product_name_slug:
            self.product_name_slug = slugify(self.product_name)
        return super().save(*args, **kwargs)

    # def upvote(self):
    #     self.votes_total += 1
    #     self.save()


@receiver(m2m_changed, sender=Product.users_votes.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_votes = instance.users_votes.count()
    instance.save()


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)


class Vote(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return 'Vote for product {} by {}'.format(self.product, self.user)
