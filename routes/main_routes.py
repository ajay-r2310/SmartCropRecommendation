"""Web and API routes."""

from __future__ import annotations

import csv
import io

from flask import Blueprint, Response, flash, redirect, render_template, request, url_for

from database.mongodb import MongoDB
from services.prediction_service import PredictionService
from utils.constants import CROP_METADATA, SEASONS, SOIL_TYPES, TAMIL_NADU_DISTRICTS
from utils.helpers import format_currency, format_datetime
from utils.validators import normalize_land_area, validate_prediction_payload

main_bp = Blueprint("main", __name__)
prediction_service = PredictionService()
database = MongoDB()


@main_bp.app_template_filter("currency")
def currency_filter(value: float) -> str:
    return format_currency(value)


@main_bp.app_template_filter("datetime")
def datetime_filter(value) -> str:
    return format_datetime(value)


@main_bp.route("/")
def index():
    return render_template(
        "index.html",
        districts=TAMIL_NADU_DISTRICTS,
        soil_types=SOIL_TYPES,
        seasons=SEASONS,
    )


@main_bp.route("/recommend", methods=["POST"])
def recommend():
    is_valid, errors = validate_prediction_payload(request.form)
    if not is_valid:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("main.index"))

    result = prediction_service.recommend(
        location=request.form["location"].strip(),
        soil_type=request.form["soil_type"].strip(),
        season=request.form["season"].strip(),
        land_area=normalize_land_area(request.form["land_area"]),
    )
    document_id = database.insert_prediction(result)
    result["document_id"] = document_id or "Not stored - configure MongoDB Atlas"
    return render_template("result.html", result=result)


@main_bp.route("/history")
def history():
    crop = request.args.get("crop", "").strip()
    season = request.args.get("season", "").strip()
    predictions = database.get_predictions(crop=crop, season=season)
    return render_template(
        "history.html",
        predictions=predictions,
        crops=sorted(CROP_METADATA.keys()),
        seasons=SEASONS,
        selected_crop=crop,
        selected_season=season,
    )


@main_bp.route("/history/export")
def export_history():
    predictions = database.get_predictions(
        crop=request.args.get("crop", "").strip(),
        season=request.args.get("season", "").strip(),
    )
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "Location",
            "Soil Type",
            "Season",
            "Land Area",
            "Temperature",
            "Humidity",
            "Rainfall",
            "Predicted Crop",
            "Expected Yield",
            "Estimated Profit",
            "Sowing Month",
            "Prediction Time",
        ]
    )
    for item in predictions:
        writer.writerow(
            [
                item.get("location"),
                item.get("soil_type"),
                item.get("season"),
                item.get("land_area"),
                item.get("temperature"),
                item.get("humidity"),
                item.get("rainfall"),
                item.get("predicted_crop"),
                item.get("expected_yield"),
                item.get("estimated_profit"),
                item.get("sowing_month"),
                format_datetime(item.get("prediction_time")),
            ]
        )
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=prediction_history.csv"},
    )


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Thank you. The agriculture support team will review your message.", "success")
        return redirect(url_for("main.contact"))
    return render_template("contact.html")

