from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import json

def analyze_website(url):
    chat_model = ChatOpenAI(model="gpt-4-turbo")
    
    system_message = SystemMessage(
        content="Du är en AI-assistent specialiserad på att analysera företagswebbplatser och extrahera nyckelinformation. Returnera all data i JSON-format utan extra kommentarer eller förklaringar."
    )
    
    user_message = HumanMessage(
        content=f"""
        Analysera webbplatsen {url}. Ge följande data i JSON-format exakt:

        {{
            "email": "...",
            "phone": "...",
            "instagram": "...",
            "facebook": "...",
            "linkedin": "...",
            "industry": "...",
            "video_need_assessment": "Kort kommentar om företagets behov av video och digitalt innehåll."
        }}

        Returnera ENDAST JSON. Inget annat. Om data saknas, använd tomma strängar ("").
        """
    )
    
    result = chat_model.invoke([system_message, user_message])

    # Försöker säkra JSON-parsning
    try:
        clean_json = result.content.strip("```json").strip("```").strip()
        parsed_json = json.loads(clean_json)
        return parsed_json
    except json.JSONDecodeError as e:
        print(f"Fel vid JSON-parsning: {e}")
        return {
            "email": "",
            "phone": "",
            "instagram": "",
            "facebook": "",
            "linkedin": "",
            "industry": "",
            "video_need_assessment": ""
        }
