"""
Core views including health checks and system status probes.
"""

import logging
from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def healthz(request):
    """
    Liveness and readiness probe endpoint.
    Validates database connectivity and cache responsiveness.

    Returns:
        JsonResponse with 200 OK when database and cache are responsive,
        or 503 Service Unavailable when any critical dependency check fails.
    """
    db_ok = True
    db_error = None
    cache_ok = True
    cache_error = None

    # 1. Database Connectivity Probe
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
            if not row or row[0] != 1:
                db_ok = False
                db_error = "Unexpected response from database query."
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Health probe database error: %s", exc)
        db_ok = False
        db_error = str(exc)

    # 2. Cache Responsiveness Probe
    try:
        cache_key = "__healthz_probe__"
        cache.set(cache_key, "ok", timeout=5)
        val = cache.get(cache_key)
        if val != "ok":
            cache_ok = False
            cache_error = "Cache read/write verification failed."
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Health probe cache error: %s", exc)
        cache_ok = False
        cache_error = str(exc)

    all_healthy = db_ok and cache_ok
    status_code = 200 if all_healthy else 503

    payload = {
        "status": "healthy" if all_healthy else "unhealthy",
        "database": "connected" if db_ok else "error",
        "cache": "connected" if cache_ok else "error",
        "service": "triberaised-django-cms",
    }
    if db_error:
        payload["database_error"] = db_error
    if cache_error:
        payload["cache_error"] = cache_error

    return JsonResponse(payload, status=status_code)
