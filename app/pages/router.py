from datetime import date, datetime, timedelta
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.bookings.router import get_bookings
from app.hotels.rooms.router import get_rooms_by_time
from app.hotels.router import get_all_hotels, get_hotels_by_location, get_hotel_by_id
from app.utils import format_number_thousand_separator, get_month_days

router_frontend = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")


@router_frontend.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router_frontend.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router_frontend.get("/all-hotels", response_class=HTMLResponse)
async def get_all_hotels_page(request: Request, hotels=Depends(get_all_hotels)):
    return templates.TemplateResponse(
        "hotels.html",
        {
            "request": request,
            "hotels": hotels
        }
    )


@router_frontend.get("/bookings", response_class=HTMLResponse)
async def get_bookings_page(request: Request, bookings=Depends(get_bookings)):
    return templates.TemplateResponse(
        "bookings/bookings.html",
        {
            "request": request,
            "bookings": bookings,
            "format_number_thousand_separator": format_number_thousand_separator
        }
    )


@router_frontend.get("/bookings_successful", response_class=HTMLResponse)
async def get_bookings_successful_page(request: Request):
    return templates.TemplateResponse("bookings/bookings_successful.html", {"request": request})


@router_frontend.get("/hotels", response_class=HTMLResponse)
async def get_hotels_search_page(request: Request):
    date_from = datetime.today().date()
    date_to = (datetime.today() + timedelta(days=180)).date()
    dates = get_month_days()

    return templates.TemplateResponse(
        "hotels_and_rooms/hotels.html",
        {
            "request": request,
            "hotels": [],
            "location": "",
            "date_from": date_from,
            "date_to": date_to,
            "dates": dates
        }
    )


@router_frontend.get("/hotels/{location}", response_class=HTMLResponse)
async def get_hotels_search_page(
        request: Request,
        location: str,
        date_from: date,
        date_to: date,
        hotels=Depends(get_hotels_by_location)
):
    dates = get_month_days()

    if date_from > date_to:
        date_to, date_from = date_from, date_to

    date_from = max(datetime.today().date(), date_from)
    date_to = min((datetime.today() + timedelta(days=180)).date(), date_to)

    return templates.TemplateResponse(
        "hotels_and_rooms/hotels.html",
        {
            "request": request,
            "hotels": hotels,
            "location": location,
            "date_from": date_from.strftime("%Y-%m-%d"),
            "date_to": date_to.strftime("%Y-%m-%d"),
            "dates": dates
        }
    )


@router_frontend.get("/hotels/{hotel_id}/rooms", response_class=HTMLResponse)
async def get_rooms_page(
        request: Request,
        date_from: date,
        date_to: date,
        rooms=Depends(get_rooms_by_time),
        hotel=Depends(get_hotel_by_id)
):
    date_from_formatted = date_from.strftime("%d-%m-%Y")
    date_to_formatted = date_from.strftime("%d-%m-%Y")
    booking_length = (date_to - date_from).days

    return templates.TemplateResponse(
        "hotels_and_rooms/rooms.html",
        {
            "request": request,
            "hotel": hotel,
            "rooms": rooms,
            "date_from": date_from,
            "date_to": date_to,
            "booking_length": booking_length,
            "date_from_formatted": date_from_formatted,
            "date_to_formatted": date_to_formatted,
            "format_number_thousand_separator": format_number_thousand_separator
        }
    )
