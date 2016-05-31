from libapp.models import Libitem, Libuser, Book, Dvd
print('List all the books in the db:')
books = Book.objects.all()
print(books)

print('List all the Dvds in the db:')
dvds = Dvd.objects.all()
print(dvds)

print('List all the libusers in the db:')
users = Libuser.objects.all()
print(users)

print('List all Libusers whose first name is ‘Anne’:')
anne = Libuser.objects.filter(first_name="Anne")
print(anne)

print('List all Books whose category is ‘Fiction’:')
fiction = Book.objects.filter(category=1)
print(fiction)

print('List all Books whose category is ‘Fiction’ and were published before 2005:')
old_fiction = Book.objects.filter(category=1).filter(pubyr__lte=2005)
print(old_fiction)

print('List all Books with the word ‘Networks’ in its title:')
networks = Book.objects.filter(title__contains="Networks")
print(networks)

print('List the maker of the Dvd with title ‘A New Adventure’:')
ad_dvd = Dvd.objects.filter(title="A New Adventure")
print(ad_dvd.values_list('maker',flat=True))

print('List the Libitems published after 2010:')
new_list = Libitem.objects.filter(pubyr__gte=2010)
print(new_list)

print('List the Dvds with duration less than 2 hours')
old_dvds = Dvd.objects.filter(duration__lte=(2*60))
print(old_dvds)

print('List the Libitems currently checked out:')
chk_item = Libitem.objects.filter(checked_out=True)
print(chk_item)

print('List all Libitems checked out by Libuser with username ‘lisa’:')
chk_lisa = Libitem.objects.filter(checked_out=True).filter(user__first_name__contains='Lisa')
print(chk_lisa)

print('Get the first name of the person who has checked out the Dvd ‘Funny Movie’:')
name_fun = Libuser.objects.filter(libitem__title='Funny Movie').filter(libitem__checked_out=True).values_list('first_name',flat=True).distinct()
print(name_fun)

print('Get the first name of the person who has checked out the Dvd ‘Funny Movie’:')
name_fun = Libuser.objects.filter(libitem__in=Dvd.objects.filter(title='Funny Movie').filter(checked_out=True)).values_list('first_name',flat=True)
print(name_fun)

print('List all Books checked out by Libuser with username ‘lisa’:')
book_lisa = Book.objects.filter(checked_out=True).filter(user__username__contains='lisa')
print(book_lisa)

