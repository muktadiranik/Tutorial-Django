from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue, MyClubUser
from .forms import VenueForm, UserForm, EventForm, EventFormAdmin
from django.http import HttpResponse
import csv
from django.contrib.auth.models import User
from django.contrib import messages

# import libraries to generate pdf
from django.http import FileResponse
import reportlab
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# pagination
from django.core.paginator import Paginator


def my_events(request):
    events = Event.objects.filter(attendees=request.user.id)
    # paginator
    paginator = Paginator(events, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    count = "i" * page_obj.paginator.num_pages

    return render(request, "events/my_events.html", {
        "events": events,
        "page_obj": page_obj,
        "count": count,
    })


def venue_pdf(request):
    # create a byte stream buffer
    buffer = io.BytesIO()

    # create a canvas
    c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)

    text_object = c.beginText()
    text_object.setTextOrigin(inch, inch)
    text_object.setFont("Helvetica", 16)

    # lines = ["This is line 1",
    #          "This is line 2",
    #          "This is line 3"]

    # for line in lines:
    #     text_object.textLine(line)

    venues = Venue.objects.all()

    # for venue in venues:
    #     text_object.textLine(venue.name)
    #     text_object.textLine(venue.address)
    #     text_object.textLine(venue.zip_code)
    #     text_object.textLine(venue.phone)
    #     text_object.textLine(venue.website)
    #     text_object.textLine(venue.email_address)
    #     text_object.textLine(" ")

    lines = []
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.website)
        lines.append(venue.email_address)
        lines.append(" ")

    for line in lines:
        text_object.textLine(line)

    c.drawText(text_object)
    c.showPage()
    c.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename="venues.pdf")

# generate a csv file venue


def venue_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["content-Disposition"] = "attachment; filename=venues.csv"

    # instantiate a csv writer
    writer = csv.writer(response)
    writer.writerow(["Name", "Address", "Zip Code",
                    "Phone", "Website", "Email Address"])

    venues = Venue.objects.all()
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code,
                        venue.phone, venue.website, venue.email_address])

    return response

# generate a text file venue


def venue_text(request):
    response = HttpResponse(content_type="text/plain")
    response["content-Disposition"] = "attachment; filename=venues.txt"
    # lines = ["This is line 1\n",
    #          "This is line 2\n",
    #          "This is line 3\n"]
    lines = []
    # designate the model
    venues = Venue.objects.all()
    for venue in venues:
        lines.append(
            f"{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.website}\n{venue.email_address}\n\n")

    # write to a text file
    response.writelines(lines)
    return response

# delete an event


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.manager == request.user:
        event.delete()
        messages.success(request, "Event Deleted!!!")
        return redirect("event_list")
    else:
        messages.success(
            request, "You Are Not Authorized To Delete This Event!!!")
        return redirect("event_list")

# delete a venue


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect("venue_list")

# delete a user


def delete_user(request, user_id):
    user = MyClubUser.objects.get(pk=user_id)
    user.delete()
    return redirect("user_list")


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/add_event?submitted=True")
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                # form.save()
                event.save()
                return HttpResponseRedirect("/add_event?submitted=True")

    else:
        if request.user.is_superuser:
            form = EventFormAdmin()
        else:
            form = EventForm()
        if "submitted" in request.GET:
            submitted = True

        return render(request, "events/add_event.html", {
            "form": form,
            "submitted": submitted,
        })


def update_user(request, user_id):
    user = MyClubUser.objects.get(pk=user_id)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect("user_list")
    return render(request, "events/update_user.html", {
        "user": user,
        "form": form,
    })


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None,
                     request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect("venue_list")

    return render(request, "events/update_venue.html", {
        "venue": venue,
        "form": form,
    })


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect("event_list")
    event = Event.objects.get(pk=event_id)
    return render(request, "events/update_event.html", {
        "event": event,
        "form": form,
    })


def search(request):
    if request.method == "POST":
        search_keyword = request.POST["search_keyword"]
        venue_list = Venue.objects.filter(name__contains=search_keyword)
        event_list = Event.objects.filter(name__contains=search_keyword)
        user_list_first_name = MyClubUser.objects.filter(
            first_name__contains=search_keyword)
        user_list_last_name = MyClubUser.objects.filter(
            last_name__contains=search_keyword)
        # append two query set
        user_list = user_list_first_name | user_list_last_name

        return render(request, "events/search.html", {
            "search_keyword": search_keyword,
            "venue_list": venue_list,
            "event_list": event_list,
            "user_list": user_list,
        })
    else:
        return render(request, "events/search.html", {})


def search_venue(request):
    if request.method == "POST":

        search_keyword = request.POST["search_keyword"]
        venue_list = Venue.objects.filter(name__contains=search_keyword)

        return render(request, "events/search_venue.html", {
            "venue_list": venue_list,
            "search_keyword": search_keyword,
        })
    else:
        return render(request, "events/search_venue.html", {})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, "events/show_venue.html", {
        "venue": venue,
        "venue_owner": venue_owner,
    })


def show_user(request, user_id):
    user = MyClubUser.objects.get(pk=user_id)
    return render(request, "events/show_user.html", {
        "user": user,
    })


def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, "events/show_event.html", {
        "event": event
    })


def all_users(request):
    user_list = MyClubUser.objects.all().order_by("first_name")

    p = Paginator(MyClubUser.objects.all(), 1)
    page = request.GET.get("page")
    users = p.get_page(page)

    count = "i" * users.paginator.num_pages

    return render(request, "events/user_list.html", {
        "user_list": user_list,
        "users": users,
        "count": count,
    })


def all_venues(request):
    venue_list = Venue.objects.all().order_by("name")

    # set up pagination
    p = Paginator(Venue.objects.all().order_by("name"), 2)
    page = request.GET.get("page")
    venues = p.get_page(page)

    count = "i" * venues.paginator.num_pages

    return render(request, "events/venue_list.html", {
        "venue_list": venue_list,
        "venues": venues,
        "count": count,
    })


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            # form.save()
            return HttpResponseRedirect("/add_venue?submitted=True")
    else:
        form = VenueForm()
        if "submitted" in request.GET:
            submitted = True

    return render(request, "events/add_venue.html", {
        "form": form,
        "submitted": submitted,
    })


def add_user(request):
    submitted = False
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/add_user?submitted=True")
    else:
        form = UserForm()
        if "submitted" in request.GET:
            submitted = True
    return render(request, "events/add_user.html", {
        "form": form,
        "submitted": submitted,
    })


def all_events(request):
    # fetch data from database table Event
    event_list = Event.objects.all().order_by("event_date")

    p = Paginator(Event.objects.all().order_by("event_date"), 1)
    page = request.GET.get("page")
    events = p.get_page(page)

    count = "i" * events.paginator.num_pages

    return render(request, "events/event_list.html", {
        "event_list": event_list,
        "events": events,
        "count": count,
    })


def home(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    name = "Anik"

    # capitalize month name
    month = month.capitalize()

    # convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # get current year
    now = datetime.now()
    current_year = now.year

    # get current month
    current_month = now.month

    # get current date
    current_date = now.day

    # get current time
    time = now.strftime("%H:%M:%S %p")

    # get events of current month
    event_list = Event.objects.filter(
        event_date__year=year,
        event_date__month=month_number
    )

    return render(request, 'events/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "calendar": cal,
        "current_year": current_year,
        "current_month": current_month,
        "current_date": current_date,
        "time": time,
        "event_list": event_list,
    })


def custom_calendar(request):
    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
    year_list = []
    for i in range(2000, 2030):
        year_list.append(i)
    if request.method == "POST":
        return redirect(f"/{request.POST['year']}/{request.POST['month']}/")

    return render(request, "events/custom_calendar.html", {
        "month_list": month_list,
        "year_list": year_list,
    })
