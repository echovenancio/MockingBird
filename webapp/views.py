from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    print(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
    return render(request, "base.html", {})


def health_check(request):
    return HttpResponse("ok")
