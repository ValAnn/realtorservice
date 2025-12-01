from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Property, Realtor

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