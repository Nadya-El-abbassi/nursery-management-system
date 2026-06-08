"""Service IA — conseiller jardin via OpenAI."""

import json

from flask import current_app

from app.services.stock_alert_service import StockAlertService


class AIService:
    def __init__(self, stock_alert_service=None):
        self.stock_alert_service = stock_alert_service or StockAlertService()

    def is_configured(self):
        return bool(current_app.config.get("OPENAI_API_KEY"))

    def recommend_plants(self, garden_description):
        garden_description = garden_description.strip()
        if not garden_description:
            raise ValueError("Décrivez votre jardin ou vos besoins.")

        if not self.is_configured():
            raise ValueError(
                "Clé OpenAI non configurée. Ajoutez OPENAI_API_KEY dans le fichier .env"
            )

        catalog = self.stock_alert_service.get_catalog_for_ai()
        if not catalog:
            raise ValueError("Aucune plante en stock pour faire une recommandation.")

        return self._call_openai(garden_description, catalog)

    def generate_description(self, plant_name, species):
        plant_name = plant_name.strip()
        species = species.strip()
        if not plant_name or not species:
            raise ValueError("Le nom et l'espèce sont obligatoires.")

        if not self.is_configured():
            raise ValueError(
                "Clé OpenAI non configurée. Ajoutez OPENAI_API_KEY dans le fichier .env"
            )

        return self._call_openai_description(plant_name, species)

    def advise_stock_management(self, question):
        question = question.strip()
        if not question:
            raise ValueError("Posez une question sur la gestion du stock.")

        if not self.is_configured():
            raise ValueError(
                "Clé OpenAI non configurée. Ajoutez OPENAI_API_KEY dans le fichier .env"
            )

        low_stock = self.stock_alert_service.get_low_stock()
        out_of_stock = self.stock_alert_service.get_out_of_stock()
        catalog = self.stock_alert_service.get_catalog_for_ai()

        context = {
            "stock_faible": [
                {"name": p["name"], "quantity": p["quantity"], "seuil": p["alert_threshold"]}
                for p in low_stock
            ],
            "rupture": [{"name": p["name"]} for p in out_of_stock],
            "catalogue": catalog,
        }

        return self._call_openai_stock(question, context)

    def _call_openai(self, garden_description, catalog):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ValueError("Installez openai : pip install openai") from exc

        client = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
        model = current_app.config["OPENAI_MODEL"]

        prompt = f"""Tu es un conseiller expert en pépinière.
Le client décrit son besoin : "{garden_description}"

Voici le catalogue disponible en stock (JSON) :
{json.dumps(catalog, ensure_ascii=False, indent=2)}

Recommande exactement 3 plantes du catalogue (uniquement celles en stock).
Réponds en JSON avec ce format :
{{
  "introduction": "texte court en français",
  "recommendations": [
    {{
      "plant_id": 1,
      "name": "nom",
      "reason": "pourquoi cette plante convient"
    }}
  ],
  "care_tips": "conseils d'entretien généraux"
}}
"""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Tu réponds uniquement en JSON valide, en français.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        content = response.choices[0].message.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        return json.loads(content)

    def _call_openai_description(self, plant_name, species):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ValueError("Installez openai : pip install openai") from exc

        client = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
        model = current_app.config["OPENAI_MODEL"]

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu rédiges des fiches produit pour une pépinière. "
                        "Réponds en français, 3-4 phrases maximum."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Rédige une description commerciale pour : {plant_name} "
                        f"({species}). Mentionne exposition, arrosage et usage."
                    ),
                },
            ],
            temperature=0.6,
        )

        return response.choices[0].message.content.strip()

    def _call_openai_stock(self, question, context):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ValueError("Installez openai : pip install openai") from exc

        client = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
        model = current_app.config["OPENAI_MODEL"]

        prompt = f"""Tu es un assistant IA de gestion de stock pour une pépinière au Maroc.
Question du gérant : "{question}"

État du stock (JSON) :
{json.dumps(context, ensure_ascii=False, indent=2)}

Réponds en français de façon claire et actionnable.
Indique quoi commander, quels produits sont en rupture ou stock faible si pertinent.
"""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu es un expert gestion de stock pépinière."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )

        return response.choices[0].message.content.strip()
