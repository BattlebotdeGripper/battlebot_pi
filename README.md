# Project Battlebot - Raspberry Pi 5

## Notities

- **Met deze code kan de Fly-Sky FS-iA10B Receiver uitgelezen worden en via CAN-bus verzonden worden naar een Raspberry Pi Pico 2.**

## Benodigheden
- **Raspberry Pi 5**
- **MCP2515 CAN-module**
- **Fly-Sky FS-iA10B**
- **Jumper wires**

---

## Hardware aansluiten

### **CAN-bus bedrading**
- Zie onderstaande repository voor aansluiting van de MCP2515-module:

```bash
https://github.com/Znooptokkie/mcp2515/
```

### **Fly-Sky FS-iA10B**
- Voordat er een serieel signaal van de receiver ontvangen kkan worden, moet je het volgende eerst doen:

1. Pak een Jumper wire (female|female).

2. Verbind de VCC en de GND met elkaar.

3. Zet de controller aan.

#### Aansluting Fly-Sky FS-iA10B - Raspberry Pi 5

| **Fly-Sky** | **Raspberry Pi 5 (GPIO)** |
|-------------|---------------------------|
| **VCC (i-Bus)** | **5V** |
| **GND (i-Bus)** | **GND** |
| **RX** | **** 
....

