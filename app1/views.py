from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from .forms import BookForm
from .models import Book
from django.urls import reverse_lazy
# from django.views.generic import View

# Create your views here.


class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        # print(url)
        # print(uploaded_file.name)
        # print(uploaded_file.size)
    return render(request, 'upload.html', context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book was uploaded successfully..!')
            return redirect('book_list')
        else:
            messages.warning(request, 'Please correctthe error below.')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {'form': form})

def delete(request, pk ):
    if request.method=="POST":
        books = Book.objects.get(pk=pk)
      
        books.delete()
        messages.success(request, ' Book Deleteted successfully..!')
        return redirect("book_list")



# =====================================================================
# class based view
class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'

class UploadBookView(CreateView):
    model = Book
    form_class =BookForm
    success_url = reverse_lazy('class_book_list')
    template_name ='upload_book.html'
    
