import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv(override=True)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# 1. Onze lokale functie (die de LLM natuurlijk niet zelf kan uitvoeren)
def get_weather(location: str):
    print(f"\n[SYSTEM] Lokale functie 'get_weather' aangeroepen voor: {location}")
    # In het echt doe je hier een API call naar Buienradar/KNMI
    if "amsterdam" in location.lower():
        return "Het regent, 12 graden."
    return "Zonnig, 22 graden."

# 2. De Tool Definitie voor Claude
weather_tool = {
    "name": "get_weather",
    "description": "Haal de huidige weersomstandigheden op voor een specifieke locatie.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "De stad, bijv. Amsterdam"}
        },
        "required": ["location"]
    }
}

def run_agent(user_prompt: str):
    messages = [{"role": "user", "content": user_prompt}]
    
    print("Vraag aan Claude:", user_prompt)
    
    # Eerste call naar Claude
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        tools=[weather_tool],
        messages=messages
    )

    # WORKSHOP OPDRACHT: Vul de logica in als Claude een tool wil gebruiken!
    if response.stop_reason == "tool_use":
        tool_call = next(block for block in response.content if block.type == "tool_use")
        
        # 3. Haal de argumenten uit de response van Claude
        location = tool_call.input["location"]
        
        # 4. Voer ONZE lokale code uit
        local_result = get_weather(location)
        
        # 5. Stuur het resultaat TERUG naar Claude (Dit vullen de devs in tijdens de workshop)
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user", 
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": local_result
            }]
        })
        
        print("\n[SYSTEM] Resultaat teruggestuurd naar Claude, wachten op eindantwoord...")
        
        # Tweede call om het definitieve antwoord te formuleren
        final_response = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            tools=[weather_tool],
            messages=messages
        )
        
        # content kan ook andere blokken bevatten (bv. thinking), dus pak alleen de tekstblokken
        print("\nClaude zegt:", "".join(b.text for b in final_response.content if b.type == "text"))
    else:
        print("\nClaude zegt:", "".join(b.text for b in response.content if b.type == "text"))

# Test de loop!
run_agent("Heb ik een paraplu nodig in Amsterdam vandaag?")