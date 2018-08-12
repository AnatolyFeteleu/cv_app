from django.contrib import admin
from .models import Creator, CurriculumVitae, Company, Education, Language, Other

# Register your models here.
admin.site.register(Creator)
admin.site.register(CurriculumVitae)
admin.site.register(Company)
admin.site.register(Education)
admin.site.register(Other)
admin.site.register(Language)