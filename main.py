from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import RedirectResponse
import uvicorn
from ikeatypes import *
import webscraper

def get_enum_query(enum: Enum, default_value: Enum = None) -> Query:
    return Query(default_value.name if default_value is not None else None, enum=[elem.name for elem in enum])


app = FastAPI(title="ikea-api", version="1.0.0")


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse("/docs")

@app.get("/searchProducts")
def search_products(
        query: str,
        locale: str = get_enum_query(Locale, Locale.EN_US),
        color: str = get_enum_query(Color),
        sort: str = get_enum_query(SortType, SortType.RELEVANCE),
        includeFeatured: bool = False,
        numProducts: int = 1000,
        numProductsOffset: int = 0
    ) -> list[Product]:
    if locale not in Locale._member_names_:
        raise HTTPException(422, "Invalid locale")
    if color is not None and color not in Color._member_names_:
        raise HTTPException(422, "Invalid color")
    if sort not in SortType._member_names_:
        raise HTTPException(422, "Invalid sort type")
    if numProducts < 1 or numProducts > 1000:
        raise HTTPException(422, "Invalid number of products, must be between 1 and 1000")
    if numProductsOffset < 0:
        raise HTTPException(422, "Invalid number of products offset, must be more or equal to 0")


    startIndex = numProducts*numProductsOffset
    endIndex = numProducts*(numProductsOffset+1)

    return webscraper.search_request(
        query,
        Locale[locale],
        Color[color] if color else None,
        SortType[sort],
        includeFeatured=includeFeatured
    )[startIndex:endIndex]

def main():
    try:
        uvicorn.run(app, host='0.0.0.0', port=8000)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
