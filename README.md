# react-agent-from-scratch

Ein minimaler ReAct-Agent (Reasoning + Acting), gebaut ausschließlich mit rohen Google-Gemini-API-Calls — ganz ohne Agenten-Framework wie LangChain, LangGraph oder CrewAI.

## Worum geht's?

Dieses Projekt ist ein Lernprojekt. Ziel ist es, die Reasoning→Action→Observation-Schleife, die hinter praktisch jedem AI-Agenten steckt, von Grund auf selbst zu verstehen und zu implementieren — bevor High-Level-Frameworks diese Logik abstrahieren.

Der Agent kann:
- über mehrere Schritte selbstständig entscheiden, ob und welches Tool er braucht
- eigene Tools nutzen (u.a. Taschenrechner, Web-Suche, Dateisystem-Zugriff)
- seinen Denk- und Handlungsverlauf transparent im Terminal anzeigen

## Tech-Stack

- Python 3.11+
- [google-genai](https://github.com/googleapis/python-genai) (Gemini API, kostenloser Tier)
- Kein Agenten-Framework — bewusst alles "from scratch"

## 🚧 Status: In aktiver Entwicklung

Dieses Projekt befindet sich noch im Aufbau. Aktuell entstehen nach und nach die einzelnen Bausteine (siehe [Issues](../../issues)):

- [ ] Projekt-Setup
- [ ] Gemini API Client
- [ ] Tools (Taschenrechner, Web-Suche, Dateisystem)
- [ ] ReAct-Loop (Kernlogik)
- [ ] CLI-Interface
- [ ] Error Handling & Safety
- [ ] Tests
- [ ] Vollständige Dokumentation

Eine ausführliche README mit Setup-Anleitung, Architektur-Diagramm und Beispiel-Läufen folgt, sobald der Agent funktionsfähig ist.

## Warum "from scratch"?

Frameworks sind großartig, um produktiv zu sein — aber sie verstecken oft genau die Mechanik, die man verstehen muss, um Agenten wirklich zu begreifen. Dieses Projekt ist der bewusste Umweg: erst das Prinzip verstehen, dann (in späteren Projekten) Frameworks nutzen.

## Lizenz

MIT (folgt)