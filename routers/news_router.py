from fastapi import APIRouter, HTTPException, Query
from utils import get_latest_news

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/latest")
def latest_news(
    topic: str = Query(..., description="Topic to search for news"),
    num_results: int = Query(5, description="Number of news results to return"),
):
    try:
        news = get_latest_news(topic, num_results)
        return {"news": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
