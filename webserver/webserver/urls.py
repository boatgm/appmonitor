from django.conf.urls import patterns, include, url #, urlpatterns
import settings
urlpatterns = patterns('',
    url(r'^statistic/all/','frontend.views.statistic_all'),
    url(r'^statistic/app/.*/','frontend.views.statistic_app'),
    url(r'^statistic/market/.*/','frontend.views.statistic_market'),
    url(r'^api/all/','api.views.statistic_market'),
    url(r'^api/app/.*/','api.views.statistic_market'),
    url(r'^api/market/.*/','api.views.statistic_market'),
    url(r'^crawler/stats/','crawler.views.spider_stats'),
    url(r'^crawler/log/','crawler.views.spider_log'),

    (r'^styles/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.TEMPLATE_DIRS[0]+'/'}),
    # Examples:
    # url(r'^$', 'webserver.views.home', name='home'),
    # url(r'^webserver/', include('webserver.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
