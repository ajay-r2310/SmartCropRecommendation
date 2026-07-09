"""Flask application entry point."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template

from config import Config
from routes.main_routes import main_bp
from routes.chat_routes import chat_bp

def create_app() -> Flask:
    """Create and configure the Flask application."""

    app = Flask(__name__)
    app.config.from_object(Config)

    configure_logging(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        app.logger.exception("Unhandled application error: %s", error)
        return render_template("500.html"), 500

    print("\n========== REGISTERED ROUTES ==========")
    for rule in app.url_map.iter_rules():
        print(rule)
    print("=======================================\n")

    app.logger.info("Application Start")
    return app


def configure_logging(app: Flask) -> None:
    """Configure console and rotating file logging."""

    Config.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=Config.DEBUG,
    )
