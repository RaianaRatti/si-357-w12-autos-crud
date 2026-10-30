from django.http import HttpRequest, HttpResponse


def myview(request: HttpRequest) -> HttpResponse:
    # Count visits in the session, starting at 1 and resetting after 4
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits
    if num_visits > 4:
        del request.session["num_visits"]

    resp = HttpResponse("view count=" + str(num_visits) + " 05dfff5c")
    resp.set_cookie("dj4e_cookie", "05dfff5c", max_age=1000)
    return resp
