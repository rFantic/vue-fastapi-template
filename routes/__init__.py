from fastapi import APIRouter
from fastapi import Query, HTTPException
from typing import Optional
from crossref.restful import Journals

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.get("/journals/{issn}/works")
def journal_works(
    issn: str,
    q: Optional[str] = Query(None, description="Search query for works in the journal"),
    filter_from_year: Optional[int] = Query(None, description="Filter works from this online publication year"),
    sort: Optional[str] = Query(None, description="Sort field, e.g. 'published'"),
    order: Optional[str] = Query(None, description="Sort order: 'asc' or 'desc'"),
    max_items: Optional[int] = Query(20, description="Maximum number of items to return (0 for none)"),
    count: Optional[bool] = Query(False, description="If true, include the number of matching works in the response"),
    mailto: Optional[str] = Query(None, description="Optional mailto email to identify requests to CrossRef"),
):
    """Query CrossRef for works published in a journal identified by ISSN.

    Returns either the constructed query URL and (optionally) the count of matching works,
    or raises an HTTPException on upstream errors.
    """
    # If the user supplied a mailto, pass it to the client to follow CrossRef etiquette
    journals = Journals(mailto=mailto) if mailto else Journals()
    try:
        works_query = journals.works(issn)
        if q:
            works_query = works_query.query(q)
        if filter_from_year:
            works_query = works_query.filter(**{"from-online-pub-date": str(filter_from_year)})
        if sort:
            works_query = works_query.sort(sort)
        if order:
            works_query = works_query.order(order)
        # Collect items up to max_items. journals.works(...) is an iterator.
        items = []
        if max_items and max_items > 0:
            try:
                for idx, item in enumerate(works_query):
                    items.append(item)
                    if idx + 1 >= max_items:
                        break
            except Exception as e:
                raise HTTPException(status_code=502, detail=f"CrossRef iteration error: {e}")

        resp = {"items": items}

        if count:
            try:
                resp["count"] = works_query.count()
            except Exception as e:
                raise HTTPException(status_code=502, detail=f"CrossRef count error: {e}")

        return resp
    except Exception as e:
        # Generic upstream error
        raise HTTPException(status_code=502, detail=f"CrossRef error: {e}")