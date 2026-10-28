import os
import json
import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(override=True)
client = anthropic.Anthropic()

chaotic_user_input = """
Hoi, de app crasht weer! Als ik op de afrekenen knop klik 
krijg ik een wit scherm. Dit is echt belachelijk, ik gebruik een 
iPhone 15 met iOS 17. Fix dit nu! Groet, Henk.
"""

# 1. Definieer het schema superstrak met Pydantic
class JiraTicket(BaseModel):
    title: str = Field(description="Korte, duidelijke titel van de bug")
    severity: str = Field(description="Kies uit: Low, Medium, High, Critical")
    device: str = Field(description="Het apparaat van de gebruiker")
    os_version: str = Field(description="De besturingssysteem versie")
    description: str = Field(description="Professionele samenvatting van de klacht")    
    

# Pydantic genereert automatisch het complexe JSON schema voor Claude!
ticket_tool = {
    "name": "create_jira_ticket",
    "description": "Zet een klantbericht om in een gestructureerd bug-ticket.",
    "input_schema": JiraTicket.model_json_schema()
}

def extract_structured_data(text: str):
    print("Data verwerken via Pydantic schema...")
    
    # WORKSHOP OPDRACHT: Vul de tools en tool_choice in om de JSON output af te dwingen
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        system="Gebruik altijd de tool create_jira_ticket om het klantbericht om te zetten. Vul ALLE velden in het schema in, inclusief description.",
        messages=[{"role": "user", "content": text}],

        tools=[ticket_tool],
        # claude-sonnet-5-5 ondersteunt geen geforceerde tool_choice ("tool"/"any")
        tool_choice={"type": "auto"}
    )
    
    for block in response.content:
        if block.type == "tool_use":
            # 1. Haal de ruwe JSON uit de Claude response
            raw_json = block.input
            
            print("\nClaude gaf deze JSON terug:")
            print(json.dumps(raw_json, indent=2))
            
            # 2. Ultieme check: Valideer de JSON door het door Pydantic te halen!
            try:
                validated_ticket = JiraTicket(**raw_json)
                print("\nPydantic Validatie Succesvol! Het is nu een veilig Python object:")
                print(f"Titel: {validated_ticket.title} | Severity: {validated_ticket.severity}")
            except Exception as e:
                print("\nPydantic Validatie Gefaald:", e)

extract_structured_data(chaotic_user_input)