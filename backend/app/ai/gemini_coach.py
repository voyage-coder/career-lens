
from google import genai
from app.core.config import settings

def generate_coaching(analysis):
    if not settings.gemini_api_key:
        return None

    try:
        client = genai.Client(api_key=settings.gemini_api_key)

        prompt = f"""
        You are a practical career coach.

        Analyze the following resume analysis and provide:

        1. Three prioritized career improvement steps.
        2. Three suitable project ideas.
        3. Important interview preparation topics.
        4. Skills the candidate should learn next.

        Give specific, actionable recommendations.
        Do not invent candidate experience or skills.

        Resume analysis:
        {analysis}
        """

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response")

        return response.text

    except Exception as e:
        print("Gemini Career Coach Error:", str(e))
        raise
