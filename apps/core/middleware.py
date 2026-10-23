"""
Security and performance middleware for TribeRaised Django CMS.
"""


class SecurityHeadersMiddleware:
    """
    Appends production security headers including Content-Security-Policy (CSP)
    and Permissions-Policy to HTTP responses.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Content-Security-Policy
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "font-src 'self' https://fonts.gstatic.com data:",
            "img-src 'self' data: blob: https://storage.googleapis.com https://*.googleapis.com",
            "connect-src 'self' https://profile.triberaised.com https://forum.triberaised.com",
            "frame-ancestors 'self'",
            "base-uri 'self'",
            "form-action 'self' https://profile.triberaised.com https://forum.triberaised.com",
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)

        # Permissions-Policy
        policy = "camera=(), microphone=(), geolocation=(), payment=()"
        response.headers["Permissions-Policy"] = policy

        # Referrer Policy
        if "Referrer-Policy" not in response.headers:
            response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response
