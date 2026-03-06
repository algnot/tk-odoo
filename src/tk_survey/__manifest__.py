{
    "name": "Tonkla Survey",
    "version": "1.0",
    "depends": ["survey", "website"],
    "data": [
        "reports/certificate_report.xml",
        "reports/certificate_template.xml",
        "reports/paperformat.xml",
        "reports/report.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "tk_survey/static/src/js/survey_certificate.js",
        ],
    },
    "installable": True,
}
