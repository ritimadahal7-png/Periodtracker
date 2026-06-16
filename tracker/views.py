from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import PeriodEntry
from .forms import RegisterForm


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("home")

    else:
        form = RegisterForm()

    return render(
        request,
        "tracker/register.html",
        {"form": form}
    )


@login_required
def home(request):

    result = None

    if request.method == "POST":

        last_period = request.POST.get("last_period")
        cycle_length = request.POST.get("cycle_length")

        PeriodEntry.objects.create(
            user=request.user,
            last_period_date=last_period,
            cycle_length=cycle_length
        )

        last_period_date = datetime.strptime(
            last_period,
            "%Y-%m-%d"
        )

        next_period = (
            last_period_date
            + timedelta(days=int(cycle_length))
        )

        result = next_period.strftime("%Y-%m-%d")

    entries = PeriodEntry.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "tracker/home.html",
        {
            "result": result,
            "entries": entries
        }
    )