from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /accounts/login/",
        "Allow: /accounts/signup/",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /residents/",
        "Disallow: /careplans/",
        "Disallow: /incidents/",
        "Disallow: /handovers/",
        "Disallow: /audit/",
        "Sitemap: " + request.build_absolute_uri("/sitemap.xml"),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
