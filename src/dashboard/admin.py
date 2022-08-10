from django.contrib import admin

from dashboard.models import Dashboard, OrganizationalUnit, Cardbox, CardboxType, Level1Link, NotebookPage

admin.site.register(Cardbox)
admin.site.register(CardboxType)
admin.site.register(Dashboard)
admin.site.register(Level1Link)
admin.site.register(NotebookPage)
admin.site.register(OrganizationalUnit)
