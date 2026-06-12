"""Service IA — conseiller jardin via Groq."""

import json

from flask import current_app

from app.config import get_groq_api_key, get_groq_model
from app.services.stock_alert_service import StockAlertService


class AIService:
    def __init__(self, stock_alert_service=None):
        self.stock_alert_service = stock_alert_service or StockAlertService()

    def is_configured(self):
        return bool(get_groq_api_key())

    @staticmethod
    def format_api_error(exc):
        message = str(exc).lower()
        if "invalid api key" in message or "incorrect api key" in message:
            return (
                "Clé API refusée par Groq. Vérifiez GROQ_API_KEY dans .env "
                "(https://console.groq.com/keys) puis redémarrez l'application."
            )
        if "model" in message and ("not found" in message or "does not exist" in message):
            return "Modèle IA invalide. Vérifiez GROQ_MODEL dans le fichier .env."
        return f"Erreur lors de l'appel à l'IA : {exc}"

    def recommend_plants(self, garden_description):
        garden_description = garden_description.strip()
        if not garden_description:
            raise ValueError("Décrivez votre jardin ou vos besoins.")

        if not self.is_configured():
            raise ValueError(
                "Clé Groq non configurée. Ajoutez GROQ_API_KEY dans le fichier .env"
            )

        catalog = self.stock_alert_service.get_catalog_for_ai()
        if not catalog:
            raise ValueError("Aucune plante en stock pour faire une recommandation.")

        return self._call_llm_json(garden_description, catalog)

    def generate_description(self, plant_name, species):
        plant_name = plant_name.strip()
        species = species.strip()
        if not plant_name or not species:
            raise ValueError("Le nom et l'espèce sont obligatoires.")

        if not self.is_configured():
            raise ValueError(
                "Clé Groq non configurée. Ajoutez GROQ_API_KEY dans le fichier .env"
            )

        return self._call_llm_description(plant_name, species)

    def advise_stock_management(self, question):
        question = question.strip()
        if not question:
            raise ValueError("Posez une question sur la gestion du stock.")

        if not self.is_configured():
            raise ValueError(
                "Clé Groq non configurée. Ajoutez GROQ_API_KEY dans le fichier .env"
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

        return self._call_llm_stock(question, context)

    def _get_client(self):
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise ValueError("Installez openai : pip install openai") from exc

        api_key = get_groq_api_key()
        if not api_key:
            raise ValueError(
                "Clé Groq non configurée. Ajoutez GROQ_API_KEY dans le fichier .env"
            )

        return OpenAI(
            api_key=api_key,
            base_url=current_app.config["GROQ_API_BASE_URL"],
        )

    def _call_llm_json(self, garden_description, catalog):
        client = self._get_client()
        model = get_groq_model()

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

    def _call_llm_description(self, plant_name, species):
        client = self._get_client()
        model = get_groq_model()

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

    def _call_llm_stock(self, question, context):
        client = self._get_client()
        model = get_groq_model()

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