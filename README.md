# 🧪 Thermal Monitoring con AMG8833 e Raspberry Pi

Questo progetto utilizza un sensore termico **AMG8833** per il monitoraggio delle temperature tramite un **Raspberry Pi**.

## 🔧 Funzionamento

- I dati termici vengono letti dal sensore AMG8833.
- I valori sono registrati in un database **Redis TimeSeries**.
- Un server **Flask** espone endpoint API specifici per l'interrogazione remota dei dati.
- Inserito anche un docker per l'uso dei **WebSocket** 

## 📡 Client Plotter

Il file `client_plotter` contiene un esempio di **client** che usa **REST API**:

- Interroga ciclicamente Redis per ottenere i dati termici.
- **Interpola** i dati per migliorare la resa grafica.
- Mostra una visualizzazione a schermo in tempo reale.

## 📡 Client WebSocket

Il file `client_websocket` contiene un esempio di **client** che usa **WebSocket**:

- Interroga ciclicamente Redis per ottenere i dati termici.
- **Interpola** i dati per migliorare la resa grafica.
- Mostra una visualizzazione a schermo in tempo reale.

## 🚀 Tecnologie utilizzate

- Raspberry Pi
- Sensore termico AMG8833
- Python
- REST API
- WebSocket
- RedisTimeSeries
- Flask
- PyGame (per il client plotter)
- Docker

---

> ✅ Questo progetto è utile per applicazioni IoT, rilevamento termico, monitoraggio ambientale e prototipazione hardware.
