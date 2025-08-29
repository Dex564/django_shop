from django.shortcuts import get_object_or_404
# Create your views here.
from django.views.generic import TemplateView, DetailView
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import Category, Product, Size
from django.db.models import Q


class IndexView(TemplateView):
    template_name = 'main/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() # выводим все категории которые есть в бд
        context['current_category'] = None
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'): # Если с каталога хотим зайти на home content где лист категорий
            return TemplateResponse(request, 'main/home_context.html', context)
        return TemplateResponse(request, self.template_name, context)
    


class CatalogView(TemplateView):
    template = 'main/base.html'

    FILTER_MAPPING = {
        'color': lambda queryset, value: queryset.filter(color__iexact = value), 
        'min_price': lambda queryset, value: queryset.filter(price_gte = value), 
        'max_price': lambda queryset, value: queryset.filter(price_lte = value), 
        'size': lambda queryset, value: queryset.filter(product_size__size__name = value), 
    } # словарь флагов, которые отвечают за сортировку

    def get_context_data(self, **kwargs): # по сути мы достаём из бд элементы, с которыми мы будем контактировать
        context = super().get_context_data(**kwargs) 
        category_slug = kwargs.get('category_slug')
        categories = Category.objects.all()
        products = Product.objects.all().order_by('-created_at')
        current_category = None

        if category_slug: # типа если чел указал слаг, пытаемся достать товар по слагу
            current_category = get_object_or_404(Category, slug=category_slug)
            products = Product.filter(category=current_category)

        query = self.request.GET.get('q') # q - это что что человек написал типо, я хз
        if query:
            products = products.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        filter_params = {}
        for param, filter_func in self.FILTER_MAPPING.items:
            value = self.request.GET.get(param)
            if value:
                products = filter_func(products, value)
                filter_params[param] = value
            else:
                filter_params[param] = ''
        filter_params['q'] = query or ''
        
        context.update({
            'categories': categories,
            'products': products,
            'current_category': category_slug,
            'filter_params': filter_params,
            'sizes': Size.objects.all(),
            'search_query': query or ''
        })

        if self.request.GET.get('show_search') == 'true':
            context['show_search'] = True
        elif self.request.GET.get('reset_search') == 'true':
            context['reset_search'] = True


        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.headers.get('HX-Request'):
            if context.get('show_search'):
                return TemplateResponse(request, 'main/search_input.html')
            elif context.get('reset_search'):
                return TemplateResponse(request, 'main/search_button.html')
            template = 'main/filter_modal.html' if request.GET.get('show_filters') == True else 'main/catalog.html'
            return TemplateResponse(request, template, context)
        return TemplateResponse(request, self.template_name, context)
    


class ProductDetailView(DetailView):
    model = Product
    template_name = 'main/base.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object() # человек когда делает запрос на сервер для показа дет инфы о продукте, он даёт этот самый продукт
        context['categories'] = Category.objects.all()
        context['related_products'] = Product.objects.filter(category=product.categpry).exclude(id = product.id)[:4]
        context['current_category'] = product.category.slug
        return context
    
    def get(self, request, *args, **kwargs):  #метод для получения шаблона
        self.object = self.get_object()
        context = self.get_context_data9(**kwargs)
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'main/product_detail.html', context) # чисто шаблон нашего товара
        raise TemplateResponse(request, self.template_name, context)