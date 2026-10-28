# LLM integratie & OWASP security

Een hands-on workshop waarin je zelf de engine van een autonome AI-agent bouwt met de [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python), en daarna ontdekt hoe je zo'n agent hackt en beveiligt (OWASP Top 10 voor LLM's).

**Volledige uitleg en opdrachten:** [workshop_handleiding.md](workshop_handleiding.md) (ook beschikbaar als [PDF](workshop_handleiding.pdf))

## Wat ga je leren?

| Onderdeel | Onderwerp |
|---|---|
| **Oefening 1** | Van chaos naar JSON: gestructureerde output afdwingen met Pydantic en tool use |
| **Oefening 2** | De tool use "event loop" sluiten: een lokale functie laten uitvoeren door een LLM |
| **Oefening 3.1** | De hack: prompt injection en path traversal (LLM01 en LLM06) |
| **Oefening 3.2** | De patch: de agent beveiligen in je eigen code, niet in de prompt |
| **Bonus** | DevOps-automatisering, een recursieve agent-loop en een LLM-as-a-Judge guardrail |

## Snel starten

Je hebt Python 3 en een Anthropic API key nodig.

```bash
# 1. Kopieer het voorbeeldbestand en vul je API key in
cp .env.example .env

# 2. Maak een virtual environment en activeer die
python -m venv .venv
source .venv/bin/activate          # Windows (cmd): .venv\Scripts\activate.bat

# 3. Installeer de packages
pip install -r requirements.txt

# 4. Controleer of alles werkt
cd step0_setup
python setup.py
```

Zie de [handleiding](workshop_handleiding.md) voor de exacte stappen per besturingssysteem en voor alle oefeningen.

## Mappenstructuur

```
.
├── step0_setup/            Controleer je installatie en API key
├── step1_basic/            Oefening 1: structured output met Pydantic
├── step2_tool_use/         Oefening 2: de tool use loop
├── step3_hack_and_patch/   Oefening 3: de hack en de patch
├── stepx_solutions/        Oplossingen van alle oefeningen en bonusopdrachten
├── workshop_handleiding.md De handleiding (ook als PDF)
└── requirements.txt
```

## Let op

* **Bewust kwetsbare code.** De agent in `step3_hack_and_patch` is met opzet onveilig geschreven, zodat je er een aanval op kunt uitvoeren. Gebruik deze code nooit in een echte toepassing.
* **API-kosten.** De scripts doen echte API-calls, de kosten lopen via een API key die je apart krijgt.
* **Je `.env` is geheim.** Het bestand staat in `.gitignore`. Commit je API key nooit.
* **Modellen.** De workshop gebruikt `claude-sonnet-5-5` en voor de hack ook het oudere `claude-sonnet-4-5`. Oudere modellen kunnen na verloop van tijd worden uitgefaseerd.
