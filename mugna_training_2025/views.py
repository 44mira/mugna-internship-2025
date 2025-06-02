from functools import reduce
from itertools import product
from django.http import HttpResponse, Http404
import datetime


def index(request):
    return HttpResponse(b"Hello world!")


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
    html = f"<html><body>Offset time is {result}.</body></html>"

    return HttpResponse(html.encode("utf-8"))


def apply_math(*nums):
    add = sum(nums)
    sub = reduce(lambda a, b: a - b, nums)
    prod = reduce(lambda a, b: a * b, nums)

    try:
        quo = reduce(lambda a, b: a / b, nums)
    except:
        quo = "Zero division error."

    return add, sub, prod, quo


def format_result(add, sub, prod, quo):
    return HttpResponse(
        f"""
        <html>
            <body>
                Sum: {add}
                Difference: {sub}
                Product: {prod}
                Quotient: {quo}
            </body>
        </html>
        """.encode()
    )


def add_n(request, nums):
    try:
        path = nums.strip("/").split("/")
        nums = map(int, path)
    except ValueError:
        return Http404

    result = apply_math(*nums)
    return format_result(*result)


def validdate(request, year, month, day):
    try:
        datetime.datetime(year, month, day)
    except:
        return HttpResponse("Invalid format.".encode())

    return HttpResponse("Valid format.".encode())
