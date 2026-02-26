from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.3

    def items(self):
        return [
            "account_login",
            "account_signup",
        ]

    def location(self, item):
        return reverse(item)
