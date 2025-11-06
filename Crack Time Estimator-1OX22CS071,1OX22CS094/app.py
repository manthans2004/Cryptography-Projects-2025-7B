from __future__ import annotations

from flask import Flask, render_template, request

try:
    # Optional dependency; we handle absence gracefully
    from zxcvbn import zxcvbn  # type: ignore
except Exception:  # pragma: no cover - optional
    zxcvbn = None  # type: ignore


def estimate_entropy_bits(password: str) -> float:
    """Estimate entropy bits assuming independent uniformly random characters.

    Uses detected character set size N and length L: entropy ≈ L * log2(N).
    This is a rough upper bound and does not account for structure or patterns.
    """
    import math

    if not password:
        return 0.0

    has_lower = any("a" <= c <= "z" for c in password)
    has_upper = any("A" <= c <= "Z" for c in password)
    has_digits = any("0" <= c <= "9" for c in password)
    specials = set(" !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    has_symbols = any(c in specials for c in password)

    charset_size = 0
    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digits:
        charset_size += 10
    if has_symbols:
        charset_size += len(specials)

    charset_size = max(charset_size, 1)
    return len(password) * math.log2(charset_size)


def format_seconds(seconds: float) -> str:
    """Convert seconds to a human-friendly duration string."""
    if seconds < 1:
        return "< 1s"
    units = [
        (365 * 24 * 3600, "year"),
        (30 * 24 * 3600, "month"),
        (7 * 24 * 3600, "week"),
        (24 * 3600, "day"),
        (3600, "hour"),
        (60, "minute"),
        (1, "second"),
    ]
    parts: list[str] = []
    remaining = int(seconds)
    for unit_seconds, name in units:
        if remaining >= unit_seconds:
            qty = remaining // unit_seconds
            remaining -= qty * unit_seconds
            parts.append(f"{qty} {name}{'s' if qty != 1 else ''}")
        if len(parts) >= 2:
            break
    return ", ".join(parts) if parts else "< 1s"


def compute_crack_times(entropy_bits: float) -> dict[str, str]:
    """Compute simple crack-time estimates for different attacker models.

    Assumes guesses required ≈ 2^(entropy_bits - 1) on average.
    """
    import math

    guesses_required = 2 ** max(entropy_bits - 1.0, 0.0)
    rates = {
        "online": 1e2,        # 100 guesses/sec
        "offline_cpu": 1e6,  # 1e6 guesses/sec
        "offline_gpu": 1e9,  # 1e9 guesses/sec
    }
    times = {k: guesses_required / v for k, v in rates.items()}
    return {k: format_seconds(t) for k, t in times.items()}


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/analyze")
    def analyze():
        password = request.form.get("password", "")
        if not password:
            return render_template(
                "results.html",
                password_entered=False,
                entropy_bits=0.0,
                zxcvbn_guesses=0.0,
                crack_times={"online": "-", "offline_cpu": "-", "offline_gpu": "-"},
                feedback_warnings=[],
                feedback_suggestions=[],
            )

        entropy_bits = estimate_entropy_bits(password)

        zxcvbn_guesses = 0.0
        feedback_warnings: list[str] = []
        feedback_suggestions: list[str] = []
        if zxcvbn is not None:
            try:
                res = zxcvbn(password)
                zxcvbn_guesses = float(res.get("guesses", 0.0))
                fb = res.get("feedback") or {}
                warning = fb.get("warning")
                suggestions = fb.get("suggestions") or []
                if warning:
                    feedback_warnings.append(str(warning))
                for s in suggestions:
                    feedback_suggestions.append(str(s))
            except Exception:
                # Fallback silently if zxcvbn fails
                pass

        crack_times = compute_crack_times(entropy_bits)

        return render_template(
            "results.html",
            password_entered=True,
            entropy_bits=entropy_bits,
            zxcvbn_guesses=zxcvbn_guesses,
            crack_times=crack_times,
            feedback_warnings=feedback_warnings,
            feedback_suggestions=feedback_suggestions,
        )

    return app


app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



