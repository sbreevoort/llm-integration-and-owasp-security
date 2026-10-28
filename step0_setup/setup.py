import os
import anthropic
from dotenv import load_dotenv

# 1. Laad de variabelen uit het .env bestand
load_dotenv(override=True)

# Sanity check: is de API key aanwezig?
if not os.getenv("ANTHROPIC_API_KEY") or "xXxX" in os.getenv("ANTHROPIC_API_KEY"):
    print("FOUT: Geen geldige ANTHROPIC_API_KEY gevonden!")
    print("Heb je het .env.example bestand gekopieerd naar .env en je key ingevuld?")
    exit(1)

print("Setup succesvol! Verbinding maken met Anthropic...")
client = anthropic.Anthropic()

prompt = "Hoi Claude, werkt de setup?"
print(f"Stel een vraag ter controle: {prompt}")

try:
    print("Wachten op antwoord van Claude...\n")
    
    # Een standaard, simpele API call (zonder tools of structuur)
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    # content kan ook andere blokken bevatten (bv. thinking), dus pak alleen de tekstblokken
    for block in response.content:
        if block.type == "text":
            print(block.text)
    
    #print("[ONGESTRUCTUREERDE OUTPUT VAN CLAUDE]:\n")
    #print(response)
    
except Exception as e:
    print(f"\nFOUT tijdens API call: {e}")