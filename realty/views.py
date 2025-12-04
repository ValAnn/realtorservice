from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Property, Realtor
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ClientSignUpForm, RealtorSignUpForm # Импортируем наши формы

from .forms import ClientSignUpForm, RealtorSignUpForm, PropertyForm # Убедитесь, что PropertyForm импортирована

from django.contrib import messages
from .models import Property, Realtor, Client


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
def property_add(request): 
    try:
        realtor_profile = Realtor.objects.get(user=request.user)
    except ObjectDoesNotExist:
        # Если это обычный клиент, перенаправляем, если им не положено добавлять
        messages.error(request, 'У вас нет прав для добавления объектов.')
        return redirect('home')

    # 1. Получаем/Создаем профиль клиента для текущего пользователя (риелтора)
    # Это решает проблему обязательного поля client в модели Property.
    client_profile, created = Client.objects.get_or_create(
        user=request.user, 
        defaults={
            'phone': realtor_profile.phone,
            'address': 'Не указан',
        }
    )

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES) 
        if form.is_valid():
            new_property = form.save(commit=False)
            
            # Привязка
            new_property.realtor = realtor_profile
            new_property.client = client_profile # Устанавливаем обязательное поле client!
            
            new_property.save()
            
            messages.success(request, 'Новый объект успешно добавлен!')
            
            return redirect('realtor_dashboard')
        else:
            # 🚨 ЭТОТ БЛОК ТЕПЕРЬ ОБЯЗАТЕЛЕН для вывода ошибки
            messages.error(request, 'Ошибка валидации! Объект не сохранен. Проверьте форму.')
            # Если форма недействительна, она будет передана в шаблон с ошибками
    else:
        form = PropertyForm()
        
    context = {
        'form': form,
        'is_edit': False
    }
    return render(request, 'realty/property_form.html', context)

# realty/views.py (Обновленный блок property_edit)

# realty/views.py (Обновленный блок property_edit)

@login_required
def property_edit(request, pk):
    try:
        realtor_profile = Realtor.objects.get(user=request.user)
    except ObjectDoesNotExist:
        messages.error(request, 'У вас нет прав для редактирования объектов.')
        return redirect('home')
    
    property_instance = get_object_or_404(Property, pk=pk)
    
    # 2. Проверяем, принадлежит ли объект текущему риелтору
    if property_instance.realtor != realtor_profile:
        messages.error(request, 'У вас нет прав на редактирование этого объекта.')
        return redirect('realtor_dashboard')

    # 3. 🛠️ ЛОГИКА АВТОМАТИЧЕСКОГО ЗАПОЛНЕНИЯ ОТСУТСТВУЮЩЕГО КЛИЕНТА
    # Если объект был создан до внедрения обязательного поля "client", мы его заполним.
    try:
        current_client = property_instance.client
    except Client.DoesNotExist: # Перехватываем ошибку, если client_id == NULL
        # Если клиент отсутствует (этот объект был создан старым способом), 
        # привязываем его к текущему пользователю-риелтору (как в property_add).
        client_profile, created = Client.objects.get_or_create(
            user=request.user, 
            defaults={
                'phone': realtor_profile.phone,
                'address': 'Не указан',
            }
        )
        property_instance.client = client_profile
        property_instance.save() # Сохраняем, чтобы client_id был заполнен
        current_client = client_profile # Устанавливаем текущего клиента
    # 🛠️ КОНЕЦ ЛОГИКИ АВТОЗАПОЛНЕНИЯ КЛИЕНТА

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            updated_property = form.save(commit=False)
            
            # Теперь updated_property.client гарантированно существует 
            # благодаря блоку try/except выше
            updated_property.realtor = property_instance.realtor 
            updated_property.client = current_client # Используем текущего клиента
            
            updated_property.save() 
            
            messages.success(request, f'Объект "{updated_property.title}" успешно обновлен.')
            return redirect('realtor_dashboard')
        else:
            messages.error(request, 'Ошибка валидации! Объект не обновлен. Проверьте форму.')
            
    else:
        # Загружаем форму с текущими данными объекта
        form = PropertyForm(instance=property_instance)
    
    context = {
        'form': form,
        'is_edit': True,
        'property': property_instance,
    }
    return render(request, 'realty/property_form.html', context)

# --- ФУНКЦИЯ УДАЛЕНИЯ ОБЪЕКТА ---
@login_required
def property_delete(request, pk):
    """
    Позволяет риелтору удалить объект недвижимости (с подтверждением, если POST).
    """
    try:
        realtor_profile = Realtor.objects.get(user=request.user)
    except ObjectDoesNotExist:
        messages.error(request, 'У вас нет прав для удаления объектов.')
        return redirect('home')

    property_instance = get_object_or_404(Property, pk=pk)
    
    # Проверяем права собственности
    if property_instance.realtor != realtor_profile:
        messages.error(request, 'У вас нет прав на удаление этого объекта.')
        return redirect('realtor_dashboard')

    if request.method == 'POST':
        title = property_instance.title # Сохраняем название до удаления
        property_instance.delete()
        messages.success(request, f'Объект "{title}" успешно удален.')
        return redirect('realtor_dashboard')
    
    # Если GET запрос, то просим подтверждение
    context = {
        'property': property_instance
    }
    # Вам потребуется создать шаблон 'realty/property_confirm_delete.html'
    return render(request, 'realty/property_confirm_delete.html', context)