reservation_schema = {
    "id": int,
    "customer_id": int,
    "net_price": int,
    "start_latitude": float,
    "start_longitude": float,
    "srid": int,
    "location_id": int
}

location_schema = {
    "id": int,
    "wgs84_polygon": str,
    "title": str
}