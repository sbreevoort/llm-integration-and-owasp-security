import os
import anthropic
from dotenv import load_dotenv

load_dotenv(override=True)
client = anthropic.Anthropic()

# Tool 1
def get_location_from_ip():
    print("\n[SYSTEM] Lokale functie 'get_location_from_ip' aangeroepen.")
    return "Amsterdam"

# Tool 2
def get_weather(location: str):
    print(f"\n[SYSTEM] Lokale functie 'get_weather' aangeroepen voor: {location}")
    if "amsterdam" in location.lower():
        return "Het regent, 12 graden."
    return "Zonnig, 22 graden."

tools = [
    {
        "name": "get_location_from_ip",
        "description": "Haal de huidige stad van de gebruiker op basis van hun IP-adres. Heeft geen input nodig.",
        "input_schema": {"type": "object", "properties": {}}
    },
    {
        "name": "get_weather",
        "description": "Haal de huidige weersomstandigheden op voor een specifieke locatie.",
        "input_schema": {
            "type": "object",
            "properties": {"location": {"type": "string", "description": "De stad, bijv. Amsterdam"}},
            "required": ["location"]
        }
    }
]

def run_agentic_loop(user_prompt: str):
    messages = [{"role": "user", "content": user_prompt}]
    print("Vraag aan Claude:", user_prompt)
    
    # Recursieve loop: blijf draaien tot de stop_reason niet meer 'tool_use' is
    while True:
        response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        if response.stop_reason == "tool_use":
            # Voeg het verzoek van Claude toe aan de history
            messages.append({"role": "assistant", "content": response.content})
            
            # Voer alle opgevraagde tools uit (Claude kan er meerdere in 1 beurt vragen)
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    if block.name == "get_location_from_ip":
                        result = get_location_from_ip()
                    elif block.name == "get_weather":
                        result = get_weather(block.input["location"])
                    else:
                        result = "Unknown tool"
                    
                    tool_results.append({
                        "type": "tool_result", 
                        "tool_use_id": block.id, 
                        "content": result
                    })
            
            # Voeg onze resultaten toe en de loop start opnieuw!
            messages.append({"role": "user", "content": tool_results})
            print("\n[SYSTEM] Resultaat naar Claude, wachten op vervolgstap...")
            
        else:
            # We hebben een tekstueel antwoord! De loop stopt.
            # content kan ook andere blokken bevatten (bv. thinking), dus pak alleen de tekstblokken
            print("\nClaude zegt:", "".join(b.text for b in response.content if b.type == "text"))
            break

if __name__ == "__main__":
    run_agentic_loop("Waar ben ik nu en heb ik daar vandaag een paraplu nodig?")
