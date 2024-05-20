from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
import uvicorn
from ikeatypes import *
import webscraper

def get_enum_query(enum: Enum, default_value: Enum = None) -> Query:
    return Query(default_value.name if default_value is not None else None, enum=[elem.name for elem in enum])


app = FastAPI()


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse("/docs")

@app.get("/searchProducts")
def search_products(
        query: str,
        locale: str = get_enum_query(Locale, Locale.EN_US),
        color: str = get_enum_query(Color),
        sort: str = get_enum_query(SortType, SortType.RELEVANCE),
        includeFeatured: bool = False
    ):
    return webscraper.search_request(
        query,
        Locale[locale],
        Color[color] if color else None,
        SortType[sort],
        includeFeatured=includeFeatured
    )

def main():
    try:
        uvicorn.run(app, host='0.0.0.0', port=8000)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
