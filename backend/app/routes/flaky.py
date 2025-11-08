from fastapi import APIRouter, Query
import random
import time

router = APIRouter()


@router.get("/flaky", summary="Flaky endpoint for testing 5xx error alerts")
def flaky_endpoint(
    wait: str = Query("300ms", description="Wait duration like 300ms"),
    errorRate: float = Query(0.8, ge=0.0, le=1.0, description="Probability of returning 500"),
):
    """Artificially slow and error-prone endpoint.
    Waits the specified time then returns either 200 or 500 based on errorRate.
    Returns JSON with outcome and parameters.
    """
    # parse wait string (support ms only for simplicity)
    ms = 0
    if wait.endswith("ms"):
        try:
            ms = int(wait[:-2])
        except ValueError:
            ms = 0
    # sleep
    if ms > 0:
        time.sleep(ms / 1000.0)
    failed = random.random() < errorRate
    if failed:
        from fastapi import HTTPException

        raise HTTPException(status_code=500, detail={"error": "Injected failure", "wait": wait, "errorRate": errorRate})
    return {"status": "ok", "wait": wait, "errorRate": errorRate}
