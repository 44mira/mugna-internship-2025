from functools import reduce
from django.http import HttpResponse, Http404
from django.shortcuts import render
import datetime


def index(request):
    context = {"request": request}
    return render(request, "index.html", context)


def current_datetime(request):
    now = datetime.datetime.now()
    html = f"<html><body>It is now {now}.</body></html>"

    return HttpResponse(html.encode("utf-8"))


def offset_time(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        return Http404

    now = datetime.datetime.now()
    result = now + datetime.timedelta(hours=offset)

    return render(request, "offset.html", {"output": result})


def apply_math(*nums):
    add = sum(nums)
    sub = reduce(lambda a, b: a - b, nums)
    prod = reduce(lambda a, b: a * b, nums)

    try:
        quo = reduce(lambda a, b: a / b, nums)
    except:
        quo = "Zero division error."

    return add, sub, prod, quo


def add_n(request, nums):
    try:
        path = nums.strip("/").split("/")
        nums = map(int, path)
    except ValueError:
        return Http404

    add, sub, prod, quo = apply_math(*nums)
    return render(
        request, "math.html", {"add": add, "sub": sub, "prod": prod, "quo": quo}
    )


def validdate(request, year, month, day):
    context = {"output": "Valid format"}
    try:
        datetime.datetime(year, month, day)
    except:
        context["output"] = "Invalid format"

    return render(request, "valid_date.html", context)
