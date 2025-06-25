from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Product
from category.models import Category
from django.utils.text import slugify


class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category__name',  # Matches column name in Excel/CSV
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')  # Match by category name
    )

    def before_import_row(self, row, **kwargs):
        """
        Automatically creates category if it doesn't exist before importing a row.
        Ensures no 'null category_id' errors.
        """
        category_name = row.get('category__name')
        if category_name:
            category_name = category_name.strip()
            Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': slugify(category_name)}
            )

    class Meta:
        model = Product
        import_id_fields = ('slug',)
        fields = (
            'name',
            'slug',
            'category__name',
            'description',
            'price',
            'size',
            'stock',
            'image',
        )
        skip_unchanged = True
        report_skipped = True


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'category', 'price', 'size', 'stock', 'created_at')
    list_filter = ('category', 'size')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
