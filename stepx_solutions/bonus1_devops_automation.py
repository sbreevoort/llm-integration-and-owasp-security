import os
import json
import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv(override=True)
client = anthropic.Anthropic()

class JiraTicket(BaseModel):
    title: str = Field(description="Korte, duidelijke titel van de bug")
    severity: str = Field(description="Kies uit: Low, Medium, High, Critical")
    device: str = Field(description="Het apparaat van de gebruiker")
    os_version: str = Field(description="De besturingssysteem versie")
    description: str = Field(description="Professionele samenvatting van de klacht")

ticket_tool = {
    "name": "create_jira_ticket",
    "description": "Zet een klantbericht om in een gestructureerd bug-ticket.",
    "input_schema": JiraTicket.model_json_schema()
}

# De gesimuleerde DevOps API Integratie
def export_to_mock_api(ticket: JiraTicket):
    filename = "tickets.json"
    print(f"\n[DEVOPS] Ticket exporteren naar database ({filename})...")
    
    tickets = []
    # Lees bestaande tickets als het bestand al bestaat
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                tickets = json.load(f)
        except json.JSONDecodeError:
            pass
            
    # Voeg het nieuwe gevalideerde ticket toe (model_dump() converteert Pydantic object naar dict)
    tickets.append(ticket.model_dump())
    
    # Schrijf alles terug naar disk
    with open(filename, 'w') as f:
        json.dump(tickets, f, indent=2)
        
    print(f"[DEVOPS] Ticket succesvol opgeslagen! Totaal tickets in DB: {len(tickets)}")
    print(f"Laatst toegevoegd: {ticket.title} ({ticket.severity})")

def process_customer_feedback(text: str):
    print("Klantbericht verwerken...")
    
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        system="Gebruik altijd de tool create_jira_ticket om het klantbericht om te zetten. Vul ALLE velden in het schema in, inclusief description.",
        messages=[{"role": "user", "content": text}],
        tools=[ticket_tool],
        # claude-sonnet-5-5 ondersteunt geen geforceerde tool_choice ("tool"/"any")
        tool_choice={"type": "auto"}
    )
    
    if response.stop_reason != "tool_use":
        print(f"\nClaude gebruikte de tool niet. stop_reason: {response.stop_reason}")
        for block in response.content:
            if block.type == "text":
                print(block.text)
        return

    for block in response.content:
        if block.type == "tool_use":
            try:
                # Validatie
                validated_ticket = JiraTicket(**block.input)
                print("\nPydantic Validatie Succesvol!")
                
                # Exporteren naar ons 'DevOps' systeem
                export_to_mock_api(validated_ticket)
                
            except Exception as e:
                print("\nPydantic Validatie Gefaald:", e)

if __name__ == "__main__":
    chaotic_user_input = """
    Hoi, de app crasht weer! Als ik op de afrekenen knop klik 
    krijg ik een wit scherm. Dit is echt belachelijk, ik gebruik een 
    iPhone 15 met iOS 17. Fix dit nu! Groet, Henk.
    """
    process_customer_feedback(chaotic_user_input)
