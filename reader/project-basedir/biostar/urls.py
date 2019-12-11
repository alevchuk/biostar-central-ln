from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic import TemplateView
from biostar.server import views, ajax, search, moderate, api
from biostar.apps.posts.views import NewAnswer, NewPost, EditPost
from biostar.apps.users.views import DigestManager, unsubscribe
from biostar.apps.util.views import QRCode

urlpatterns = patterns('',

    # Post listing.
    url(r'^$', views.PostList.as_view(), name="home"),

    # Listing of all tags.
    url(r'^t/$', views.TagList.as_view(), name="tag-list"),

    # Badge view details.
    url(r'^b/(?P<pk>\d+)/$', views.BadgeView.as_view(), name="badge-view"),

    # Badge list details.
    url(r'^b/list/$', views.BadgeList.as_view(), name="badge-list"),

    # Topic listing.
    url(r'^t/(?P<topic>.+)/$', views.PostList.as_view(), name="topic-list"),


    # ==============================
    # LN
    # ==============================

    # QR code image
    url(r'^qr/(?P<pay_req>[\w]+)/qr.svg$', QRCode.as_view(content_type='image/svg+xml'), name="qr-code"),


    # ==============================
    # User
    # ============================== 

    # The list of users.
    url(r'^user/list/$', views.UserList.as_view(), name="user-list"),

    # User details.
    url(r'^u/(?P<pk>\d+)/$', views.UserDetails.as_view(), name="user-details"),

    # User details.
    url(r'^u/edit/(?P<pk>\d+)/$', views.EditUser.as_view(), name="user-edit"),


    # ==============================
    # Post
    # ============================== 

    # Post details.
    url(r'^p/(?P<pk>\d+)/$', views.PostDetails.as_view(), name="post-details"),

    # Post preview edit
    url(r'^p/edit/preview/(?P<memo>[\w\/\+\=]+)/$', views.RateLimitedNewPost.as_view(), name="post-preview-edit"),

    # Post publish
    url(r'^p/publish/preview/(?P<memo>[\w\/\+\=]+)/$', views.PostPublishView.as_view(), name="post-publish"),

    # Post preview
    url(r'^p/new/preview/(?P<memo>[\w\/\+\=]+)/$', views.PostPreviewView.as_view(), name="post-preview"),

    # A separate url for each post type.
    url(r'^p/new/post/$', views.RateLimitedNewPost.as_view(), name="new-post"),

    # A new answer
    url(r'^p/new/answer/(?P<pid>\d+)/$', views.RateLimitedNewAnswer.as_view(post_type="answer"), name="new-answer"),
    
    # A new comment
    url(r'^p/new/comment/(?P<pid>\d+)/$', views.RateLimitedNewAnswer.as_view(post_type="comment"), name="new-comment"),

    # Edit an existing post.
    url(r'^p/edit/(?P<pk>\d+)/$', EditPost.as_view(), name="post-edit"),


    # ==============================
    # Moderator
    # ==============================

    # Produces the moderator panel.
    url(r'^local/moderate/post/(?P<pk>\d+)/$', moderate.PostModeration.as_view(), name="post-moderation"),

    # Produces the moderator panel.
    url(r'^local/moderate/user/(?P<pk>\d+)/$', moderate.UserModeration.as_view(), name="user-moderation"),


    # ==============================
    # Search, Vote
    # ==============================

    # Search the body.
    url(r'^local/search/page/', search.Search.as_view(), name="search-page"),

    # Search the titles.
    url(r'^local/search/title/', search.search_title, name="search-title"),

     # Returns suggested tags
    url(r'^local/search/tags/', search.suggest_tags, name="suggest-tags"),

    # Vote submission.
    url(r'^x/vote/$', ajax.vote_handler, name="vote-submit"),

    # Local robots.txt.
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain'), name='robots'),

)

# Adding the sitemap.
urlpatterns += patterns('',
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': search.sitemaps})
)

from biostar.server.feeds import LatestFeed, TagFeed, UserFeed, PostFeed, PostTypeFeed

# Adding the RSS related urls.
urlpatterns += patterns('',

    # RSS info page.
    url(r'^info/rss/$', views.RSS.as_view(), name='rss'),

    # RSS feeds
    url(r'^feeds/latest/$', LatestFeed(), name='latest-feed'),

    url(r'^feeds/tag/(?P<text>[\w\-_\+!]+)/$', TagFeed(), name='tag-feed'),
    url(r'^feeds/user/(?P<text>[\w\-_\+!]+)/$', UserFeed(), name='user-feed'),
    url(r'^feeds/post/(?P<text>[\w\-_\+!]+)/$', PostFeed(), name='post-feed' ),
    url(r'^feeds/type/(?P<text>[\w\-_\+!]+)/$', PostTypeFeed(), name='post-type'),
)

urlpatterns += patterns('',
    url(r'^info/(?P<slug>\w+)/$', views.FlatPageView.as_view(), name='flatpage'),
    url(r'^info/update/(?P<pk>\d+)/$', views.FlatPageUpdate.as_view(), name='flatpage-update'),
)

# This is used only for the debug toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )