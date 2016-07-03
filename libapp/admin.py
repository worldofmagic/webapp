from django.contrib import admin
from libapp.models import Book, Dvd, LibUser, LibItem
import datetime


def renew(model_admin, request, queryset):
    update_count = 0
    update_msg = ""
    for obj in queryset:
        if obj.checked_out:
            update_count += 1
            queryset.filter(title=obj.title).filter(user=obj.user)\
                .update(duedate=obj.duedate+datetime.timedelta(days=21))

    if update_count == 1:
        update_msg = "1 record was"
    elif update_count > 1:
        update_msg = "%s records were" % update_count
    model_admin.message_user(request, "%s successfully renewed!" % update_msg)

renew.short_description = "Renew selected item"


class BookInLine(admin.StackedInline):
    model = Book
    fields = [('title', 'author'), 'due_date', 'checked_out']
    extra = 0


class DvdInLine(admin.TabularInline):
    model = Dvd
    fields = [('title', 'maker', 'pub_year'),
              ('user', 'due_date', 'duration', 'num_checkout', 'checked_out', 'item_type')]
    extra = 0


class LibUserAdmin(admin.ModelAdmin):
    fields = ['username', ('first_name', 'last_name'), 'password', ('email', 'phone', 'address', 'city',
                                                                    'province', 'postal_code'), 'image_tag', 'photo']
    inlines = [BookInLine, DvdInLine]
    readonly_fields = ('image_tag',)


class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'author', 'pub_year'), ('checked_out', 'item_type', 'user', 'due_date'), 'category']
    list_display = ('id', 'title', 'borrower', 'checked_out', 'due_date')
    actions = [renew]

    def borrower(obj=None):
        if obj.checked_out:
            # Returns the user who has borrowed this book
            return obj.user
        else:
            return ''

    borrower = staticmethod(borrower)


class DvdAdmin(admin.ModelAdmin):
    fields = [('title', 'maker', 'pub_year'), ('checked_out', 'item_type', 'user', 'due_date'), 'rate']
    list_display = ('title', 'rate', 'borrower', 'checked_out', 'due_date')
    actions = [renew]

    def borrower(obj=None):
        if obj.checked_out:
            # Returns the user who has borrowed this book
            return obj.user
        else:
            return ''

    borrower = staticmethod(borrower)

# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.register(Dvd, DvdAdmin)
admin.site.register(LibUser, LibUserAdmin)
