import xadmin
from xadmin import views
from .models import Cards
from yanzheng.models import UserProfile
class BaseSetting(object):
    """
    引入更换主题功能
    """
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    """
    页头和页脚
    """
    site_title = "jonathan net auth"
    site_footer = "jonathan net auth"
    # menu_style = "accordion"#如果加上，后台的菜单会变成下拉式


class CardsAdmin(object):
    list_display = ['user', 'kacode', 'time', 'is_used']
    search_fields = ['user', 'kacode', 'time', 'is_used']
    list_filter = ['user', 'kacode', 'time', 'is_used']


xadmin.site.register(Cards, CardsAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
# xadmin.site.register(UserProfile)
#