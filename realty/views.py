from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Property, Realtor
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ClientSignUpForm, RealtorSignUpForm # Импортируем наши формы

from .forms import ClientSignUpForm, RealtorSignUpForm, PropertyForm # Убедитесь, что PropertyForm импортирована


@login_required # Только для авторизованных пользователей
def realtor_dashboard(request):
    try:
        # Проверяем, является ли пользователь риелтором
        realtor_profile = Realtor.objects.get(user=request.user)
    except ObjectDoesNotExist:
        # Если профиля риелтора нет, перенаправляем на ошибку или главную
        return redirect('home') 

    # Получаем только те объекты, которые связаны с этим риелтором
    my_properties = Property.objects.filter(realtor=realtor_profile).order_by('-created_at')

    context = {
        'realtor': realtor_profile,
        'properties': my_properties,
    }
    return render(request, 'realty/realtor_dashboard.html', context)

def home(request):
    """Главная страница"""
    featured_properties = Property.objects.filter(is_featured=True)[:4]
    realtors = Realtor.objects.all()[:3]
    
    context = {
        'featured_properties': featured_properties,
        'realtors': realtors,
    }
    return render(request, 'realty/home.html', context)

class PropertyListView(ListView):
    """Список всех объектов недвижимости"""
    model = Property
    template_name = 'realty/property_list.html'
    context_object_name = 'properties'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Property.objects.all()
        
        # Фильтрация по типу недвижимости
        property_type = self.request.GET.get('property_type')
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        
        # Фильтрация по статусу
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Сортировка
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_types'] = Property.PROPERTY_TYPES
        context['status_choices'] = Property.STATUS_CHOICES
        return context

class PropertyDetailView(DetailView):
    """Детальная информация об объекте"""
    model = Property
    template_name = 'realty/property_detail.html'
    context_object_name = 'property'


def client_signup(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматический вход после регистрации
            login(request, user) 
            return redirect('home')  # Перенаправляем на главную
    else:
        form = ClientSignUpForm()
        
    return render(request, 'realty/client_signup.html', {'form': form})

def realtor_signup(request):
    if request.method == 'POST':
        form = RealtorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматический вход после регистрации
            login(request, user)
            return redirect('home')
    else:
        form = RealtorSignUpForm()
        
    return render(request, 'realty/realtor_signup.html', {'form': form})

@login_required
def property_add(request): # <--- ЭТА ФУНКЦИЯ ДОЛЖНА СУЩЕСТВОВАТЬ
    try:
        # Убедимся, что добавляет именно риелтор
        realtor_profile = Realtor.objects.get(user=request.user)
    except ObjectDoesNotExist:
        # Если это обычный клиент, он не должен добавлять объекты
        return redirect('home')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES) 
        if form.is_valid():
            new_property = form.save(commit=False)
            new_property.realtor = realtor_profile
            new_property.save()
            
            from django.contrib import messages
            messages.success(request, 'Новый объект успешно добавлен!')
            
            return redirect('realtor_dashboard')
    else:
        form = PropertyForm()
        
    context = {
        'form': form,
        'is_edit': False
    }
    return render(request, 'realty/property_form.html', context)