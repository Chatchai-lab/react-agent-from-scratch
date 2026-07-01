# CLAUDE.md
 
Diese Datei gibt Claude (und Claude Code) den Kontext für dieses Projekt.
 
## Projektübersicht
 
**Name:** react-agent-from-scratch
**Ziel:** Ein minimaler ReAct-Agent (Reasoning + Acting), gebaut ausschließlich mit rohen Google-Gemini-API-Calls — ohne Agenten-Framework (kein LangChain, LangGraph, CrewAI etc.).
 
Der Zweck ist ausschließlich **Lernen**: Verstehen, wie die Reasoning→Action→Observation-Schleife technisch funktioniert, bevor High-Level-Frameworks das abstrahieren.
 
## Tech-Stack
 
- Python 3.11+
- `google-genai` (offizielles, aktuelles Google-SDK — **nicht** das veraltete `google-generativeai`)
- Modell: `gemini-2.5-flash` (kostenloser Tier, guter Funktionsumfang für Tool Use)
- Keine Agenten-Frameworks (bewusst!)
- `python-dotenv` für API-Key-Management
- `rich` für farbige Terminal-Ausgabe (optional, aber empfohlen)
- `pytest` für Tests
## Warum Gemini?
 
Google AI Studio bietet einen dauerhaft kostenlosen Tier (kein Trial, keine Kreditkarte nötig) mit Function-Calling-Support — ideal zum Lernen ohne Kostenrisiko. Aktuelle Limits (Stand: Sommer 2026, bitte in Google AI Studio verifizieren, da sich Limits ändern können): ca. 1.500 Requests/Tag auf `gemini-2.5-flash`.
 
## Architektur-Prinzipien
 
1. **Keine Abstraktionen, die das Lernen verschleiern.** Jede Zeile Loop-Logik soll nachvollziehbar sein.
2. **Tools sind einfache Python-Funktionen** mit einem klar definierten JSON-Schema (passend zum Gemini Function-Declaration-Format).
3. **Der Agent-Loop ist explizit**, nicht versteckt in einer Bibliothek: `while`-Schleife mit klaren Schritten (Anfrage senden → Antwort parsen → Function-Call erkennen → Tool ausführen → Function-Response zurückspielen → wiederholen).
4. **Maximale Transparenz im Terminal-Output**: Der Nutzer soll live sehen, was der Agent "denkt" und tut (Thought/Action/Observation).
## Projektstruktur (Zielzustand)
 
```
react-agent-from-scratch/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   ├── agent.py          # Kern: ReAct-Loop
│   ├── client.py         # Gemini API Wrapper
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py       # Tool-Interface/Registry
│   │   ├── calculator.py
│   │   ├── web_search.py
│   │   └── file_system.py
│   └── cli.py            # Terminal-Interface
├── tests/
│   └── test_agent.py
└── examples/
    └── demo_run.md        # Beispiel-Session (Screenshot/Log)
```
 
## Konventionen
 
- Alle Tool-Definitionen folgen dem Gemini Function-Declaration-Schema (`name`, `description`, `parameters` — ein JSON-Schema-Objekt mit `type`, `properties`, `required`).
- Jeder Tool-Call wird geloggt: Tool-Name, Input, Output.
- Maximale Loop-Iterationen sind konfigurierbar (Standard: 10), um Endlosschleifen zu verhindern.
- Keine Secrets im Code — API-Key ausschließlich über `.env` (siehe `.env.example`), Variable heißt `GEMINI_API_KEY`.
- Commits folgen Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
## Kern-API-Muster (Referenz)
 
```python
from google import genai
from google.genai import types
 
client = genai.Client(api_key="...")
 
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=conversation_history,
    config=types.GenerateContentConfig(
        tools=[my_function_declarations],
        system_instruction=SYSTEM_PROMPT,
    ),
)
 
# Antwort prüfen: enthält sie einen function_call-Part?
for part in response.candidates[0].content.parts:
    if part.function_call:
        # Tool ausführen, Ergebnis als function_response-Part zurückgeben
        ...
    elif part.text:
        # finale Antwort
        ...
```
 
## Wie an diesem Projekt gearbeitet wird
 
Die Arbeit ist in GitHub Issues unterteilt (siehe `issues/`), die eine sinnvolle Reihenfolge vorgeben. Jedes Issue hat eine klare Beschreibung und Akzeptanzkriterien. Ein Issue = ein Feature-Branch = ein Pull Request.
 
Reihenfolge:
1. Projekt-Setup & Struktur
2. Gemini API Client Wrapper
3. Tool-Abstraktion + Taschenrechner-Tool
4. Web-Search-Tool
5. Dateisystem-Tool
6. ReAct-Loop (Kernlogik)
7. CLI mit farbiger Ausgabe
8. Error Handling & Safety-Limits
9. Dokumentation (README, Demo)
10. Tests
## Nicht-Ziele
 
- Keine Produktionsreife (kein Deployment, kein Multi-User-Betrieb)
- Kein Framework-Vergleich in diesem Projekt (das kommt in späteren Projekten)
- Keine UI — reines CLI-Tool