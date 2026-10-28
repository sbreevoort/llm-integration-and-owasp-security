import os
import anthropic
from dotenv import load_dotenv

# 1. Laad de variabelen uit het .env bestand
load_dotenv(override=True)

# Sanity check: is de API key aanwezig?
if not os.getenv("ANTHROPIC_API_KEY") or "xXxX" in os.getenv("ANTHROPIC_API_KEY"):
    print("❌ FOUT: Geen geldige ANTHROPIC_API_KEY gevonden!")
    print("Heb je het .env.example bestand gekopieerd naar .env en je key ingevuld?")
    exit(1)

client = anthropic.Anthropic()

print("Een chaotische e-mail die we in Oefening 1 gaan gebruiken:")
chaotic_user_input = """
Hoi, de app crasht weer! Als ik op de afrekenen knop klik 
krijg ik een wit scherm. Dit is echt belachelijk, ik gebruik een 
iPhone 15 met iOS 17. Fix dit nu! Groet, Henk.
"""
print(chaotic_user_input)
print("\nHey Claude, Maak een bug ticket van dit bericht")

prompt = f"Maak een bug ticket van dit bericht:\n\n{chaotic_user_input}"

try:
    print("⏳ Wachten op antwoord van Claude...\n")
    
    # Een standaard, simpele API call (zonder tools of structuur)
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    print("🤖 [ONGESTRUCTUREERDE OUTPUT VAN CLAUDE]:\n")
    # content kan ook andere blokken bevatten (bv. thinking), dus pak alleen de tekstblokken
    for block in response.content:
        if block.type == "text":
            print(block.text)
    
    print("\n" + "="*60)
    print("💡 Zie je hoe 'kletserig' en onvoorspelbaar dit format is?")
    print("   Probeer deze tekst maar eens in een SQL database op te slaan...")
    print("   Tijd voor Oefening 1: Structuur afdwingen met Pydantic!")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"\n❌ FOUT tijdens API call: {e}")