from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, verbose_name = "Product Price")
    quantity = models.IntegerField(default=0, verbose_name="Product Quantity")
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images")

    def get_photo(self):
        try:
            return self.image.url
        except:
            return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMwAAADACAMAAAB/Pny7AAAAM1BMVEX///+/v7+8vLz8/Pz5+fnt7e3ExMTHx8fPz8/h4eHw8PD29vbY2Njn5+fMzMzU1NS2trYNfAMMAAAEIUlEQVR4nO2c2ZqjIBBGI+573v9pOyZMVHZaC6rn+8/ltAonlFAUmTweAAAAAAAAAFDNPWfqMkZmaEXBF9FVkGEJZLgCGa5AhiuQ4Qpkvjcz4DaZJXeW3PdTc5OMmGJupWE8deiSTNT2gQTISCBDCWQkkKEEMhLIUAIZCWQogYwEMpRARgIZSpLJpFBNIVMOU/F8scxRj48ngcy4yoKWEO1MOkD0MvWyXyWannJwyGWG5lz2pCyvUctU3bkeLUR9T8dNUMv0am1dLL8JtGoIedmoZfSDAjHHtCGZuyHgKmKZUT/0EGtMGx+qrgj5CIhltCh70UZPz+UkxBrQNWKZyXQcFS0zPAvRBsTZX5Apt3ZE778tg0wTK/N+iGhG74XEMrVhAlhi2tieIe/zL1DEMpU+MKKPaeP1CNlKwBRAvc6s+tD4w+XEHqneoaGWGQrFJjY5q9vwO8kTzVnJzZa4gRmX/dbW1ztymW3BO7qEpCUHpuMH4csC6PczZf+NNPGMHJdHfdpANJ6rU2ybx7X5fH9iic0xx/MG4un5KNIUNMa5n6Y5MsLeg3p+4TxTAOtSU61OhZ4pIL9Mbf1m+Lhoi5R7wc0uU3WN5U1Sg2xjcTaSW2ab6yw2daPLNM4sILfM0BY2G9NX89zb1Mwy5SfzMtmYNqmvLMA1O2eW+W4RNBtTkG24poC8MtX3CerYVEthxrURyCtzCCXFxrjf3ppxTQFZZYbj/adIswWZu52sMqcssmh3m7GzuTjLNDll1K3ON9JMy+V+mX0KyCgzqqH0fR/Oib96lb2TGWUmvZ/t26YyFA4O2KeARDKGv82Gd/w9Ns4gc7aUaD/Tawv3aFxINpu9hGGRsWYBaWT6olP/avv429odZIWjFpBE5rX7Fcr+vb7yPzxs5whJZPr3s4//UtpW+CBstYAkBY13WUIcI22+4mKtBaSQkRnY4TTTsCGOwzw0Kb7U8K9eJDrZB9/k68WSBSSQmfeL1o+NPY0MlTHXAuhljiEl3jbl1SCzHdbQy8ynXmyRdu3tlz3NIlMqC8pSja40MhjTFJD6SOMVad4VPgTjFEAu40m0fo2pq9QyN7wfFgwJGrFMeXUStrPq7RHL0A2MqRZALEM3MEWhJ2i0MrPehdswdJZUxlqWvAW9QE0qczWf9DCpvaWUqeylvDvQpwBKGeKB0U8ECGXUL87eznd/lEDGVBi72UaJMzqZy1vjABnlsIZOZlg7cqZUMo8yAecWc5823wpkJJChBDISyFACGQlkKIGM5P+VYfBjbXN/14+1sQMyXIEMVyDDFchwBTJcgQxXIMMVyHAFMlyBDFcgwxXIcAUyXIEMVyDDFchwBTJcgQxXIMMVyHAFMlyBDFcgw5VYma7hTMgPie9UQ82ZoF/fBwAAAAAAAIC/ww/JmYESURpw2wAAAABJRU5ErkJggg=="

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity

    def __str__(self):
        return self.customer.name

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "Order Product"
        verbose_name_plural = "Order Products"

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city
    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"