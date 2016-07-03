from django.db import models
from django.utils import timezone
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


# Create your models here.
TYPE_CHOICES = (
    (1, 'Book'),
    (2, 'DVD'),
    (3, 'Other'),
)


class Suggestion(models.Model):
    title = models.CharField(max_length=100)
    pub_year = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(default=1, choices=TYPE_CHOICES)
    cost = models.IntegerField()
    num_interested = models.IntegerField()
    comments = models.TextField()


class LibUser(User):
    PROVINCE_CHOICES = (
        ('AB', 'Alberta'),  # The first value is actually stored in db, the second is descriptive
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    phone = models.IntegerField(null=True)
    photo = models.ImageField(upload_to='libapp/media/user_imgs', null=True)
    postal_code = models.CharField(max_length=7, null=True, blank=True)

    def image_tag(self):
        if self.photo:
            return u'<img src="%s" />' % self.photo.url

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return self.username


class LibItem(models.Model):

    title = models.CharField(max_length=100)
    item_type = models.CharField(max_length=6, choices=TYPE_CHOICES, default='Book')
    checked_out = models.BooleanField(default=False)
    user = models.ForeignKey(LibUser, default=None, null=True, blank=True)
    due_date = models.DateField(default=None, null=True, blank=True)
    last_checkout = models.DateField(default=None, null=True, blank=True)
    date_acquired = models.DateField(default=timezone.now)
    pub_year = models.IntegerField(validators=[MaxValueValidator(2016), MinValueValidator(1900)])
    num_checkout = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return self.title

    def overdue(self):
        if self.checked_out:
            if timezone.now().date() < self.duedate:
                return "Yes"
            else:
                return "No"


class Book(LibItem):
    CATEGORY_CHOICES = (
        (1, 'Fiction'),
        (2, 'Biography'),
        (3, 'Self Help'),
        (4, 'Education'),
        (5, 'Children'),
        (6, 'Teen'),
        (7, 'Other'),
    )

    author = models.CharField(max_length=100)
    category = models.IntegerField(choices=CATEGORY_CHOICES, default=1)

    def __str__(self):
        return self.title + ' by ' + self.author

    def __init__(self, *args, **kwargs):
        self._meta.get_field('item_type').default = 'Book'
        super(Book, self).__init__(*args, **kwargs)


class Dvd(LibItem):
    RATING_CHOICE = (
        (1, 'G'),
        (2, 'PG'),
        (3, 'PG-13'),
        (4, '14A'),
        (5, 'R'),
        (6, 'NR'),
    )
    maker = models.CharField(max_length=100)
    duration = models.IntegerField()
    rate = models.IntegerField(choices=RATING_CHOICE, default=1)

    def __str__(self):
        return self.title+' by '+self.maker

    def __init__(self, *args, **kwargs):
        self._meta.get_field('item_type').default = 'DVD'
        super(Dvd, self).__init__(*args, **kwargs)
