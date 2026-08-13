import json
from datetime import datetime

from app.database.sqlite import db


class CaseService:

    # =====================================
    # Generate Case ID
    # =====================================

    def generate_case_id(self):

        year = datetime.now().year

        result = db.fetchone(
            "SELECT COUNT(*) AS total FROM legal_cases"
        )

        number = result["total"] + 1

        return f"LRX-{year}-{number:06d}"

    # =====================================
    # Save Case
    # =====================================

    def save_case(self, request):

        case_id = self.generate_case_id()

        report = request.report

        db.execute(
            """
            INSERT INTO legal_cases(

                case_id,

                citizen_name,

                city,

                category,

                applicable_act,

                confidence,

                complaint,

                report_json,

                created_at

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,

            (

                case_id,

                request.citizen_name,

                request.city,

                report["case_analysis"]["category"],

                report["case_analysis"]["applicable_act"],

                report["confidence"],

                report["complaint"],

                json.dumps(report),

                datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                )

            )

        )

        return {

            "message": "Case saved successfully.",

            "case_id": case_id

        }

    # =====================================
    # Get All Cases
    # =====================================

    def get_cases(self):

        return db.fetchall(
            """
            SELECT

                case_id,

                citizen_name,

                city,

                category,

                confidence,

                created_at

            FROM legal_cases

            ORDER BY id DESC
            """
        )

    # =====================================
    # Get Single Case
    # =====================================

    def get_case(self, case_id):

        case = db.fetchone(
            """
            SELECT *

            FROM legal_cases

            WHERE case_id = ?
            """,
            (case_id,)
        )

        if case is None:

            return None

        case["report"] = json.loads(
            case["report_json"]
        )

        return case

    # =====================================
    # Delete Case
    # =====================================

    def delete_case(self, case_id):

        db.execute(
            """
            DELETE FROM legal_cases

            WHERE case_id = ?
            """,
            (case_id,)
        )

        return {

            "message": "Case deleted successfully."

        }


case_service = CaseService()