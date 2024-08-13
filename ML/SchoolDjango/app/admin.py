from django.contrib import admin
from django.utils.safestring import mark_safe

from app.models import User

admin.site.site_header = '校园大数据分析系统'
admin.site.site_title = '校园大数据分析系统'
admin.site.index_title = '校园大数据分析系统'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    def get_image(self, obj):
        div = f'<img src="{obj.avatar.url}" alt="头像" style="width:100px;height:80px;border-radius: 5px;">'
        return mark_safe(div)

    get_image.short_description = '头像'

    # 搜索字段
    search_fields = ['username', 'city']
    # 分页
    list_per_page = 20
    # 排序规则
    ordering = ['id', ]
    # 显示字段
    list_display = ['username', 'get_image', 'gender', 'city', 'birthday', 'date_joined']


