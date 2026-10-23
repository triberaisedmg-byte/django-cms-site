"""
Core views including health checks and system status probes.
"""

import logging
from django.db import connection
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def healthz(request):
    """
    Liveness and readiness probe endpoint.
    Validates database connectivity and returns system status JSON.

    Returns:
        JsonResponse with 200 OK when database is responsive,
        or 503 Service Unavailable when database check fails.
    """
    db_ok = True
    db_error = None

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

    status_code = 200 if db_ok else 503
    payload = {
        "status": "healthy" if db_ok else "unhealthy",
        "database": "connected" if db_ok else "error",
        "service": "triberaised-django-cms",
    }
    if db_error:
        payload["error"] = db_error

    return JsonResponse(payload, status=status_code)
