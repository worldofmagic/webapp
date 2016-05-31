from django.contrib import admin
from libapp.models import Book, Dvd, Libuser, Libitem
import datetime

def renew(modeladmin, request, queryset):
    update_count = 0
    update_msg = ""
    for obj in queryset:
        if obj.checked_out == True:
            update_count += 1
            queryset.filter(title=obj.title).filter(user=obj.user)\
                .update(duedate=obj.duedate+datetime.timedelta(days=21))

    if update_count == 1:
        update_msg = "1 record was"
    elif update_count > 1:
        update_msg = "%s records were" % update_count
    modeladmin.message_user(request, "%s successfully renewed!" % update_msg)

renew.short_description = "Renew selected item"


class BookInLine(admin.StackedInline):
    model = Book
    fields = [('title','author'),'duedate']
    extra = 0

class DvdInLine(admin.TabularInline):
    model = Dvd
    fields = [('title','maker','pubyr'),('user','duedate','num_chkout','checked_out','itemtype')]
    extra = 0

class LibuserAdmin(admin.ModelAdmin):
    fields = [('username'), ('first_name', 'last_name')]
    inlines = [BookInLine,DvdInLine]

class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'author', 'pubyr'), ('checked_out', 'itemtype', 'user', 'duedate'),'category']
    list_display = ('title', 'borrower')
    actions = [renew]

    def borrower(self, obj=None):
        if obj.checked_out == True:
            return obj.user     #Returns the user who has borrowed this book
        else:
            return ''


class DvdAdmin(admin.ModelAdmin):
    fields = [('title', 'maker', 'pubyr'), ('checked_out', 'itemtype', 'user', 'duedate'),'rate']
    list_display = ('title','rate', 'borrower')
    actions = [renew]

    def borrower(self, obj=None):
        if obj.checked_out == True:
            return obj.user     #Returns the user who has borrowed this book
        else:
            return ''





# Register your models here.
admin.site.register(Book,BookAdmin)
admin.site.register(Dvd,DvdAdmin)
admin.site.register(Libuser,LibuserAdmin)
