# Project Battlebot - Raspberry Pi 5

## Notities

- **Met deze code kan de Fly-Sky FS-iA10B Receiver uitgelezen worden en via CAN-bus verzonden worden naar een Raspberry Pi Pico 2.**

---

## Benodigheden
- **Raspberry Pi 5**
- **MCP2515 CAN-module**
- **Fly-Sky FS-iA10B**
- **Jumper wires**

---

## Hardware aansluiten

### **CAN-bus bedrading**
- Zie onderstaande repository voor aansluiting van de MCP2515-module:

https://github.com/Znooptokkie/mcp2515/


### **Fly-Sky FS-iA10B**
- Voordat er een serieel signaal van de receiver ontvangen kkan worden, moet je het volgende eerst doen:

**Receiver**
1. Pak een Jumper wire (female|female).

2. Verbind de VCC en de B met elkaar. Zorg dat er geen stroom op staat.

3. Weer voeden met stroom.

**Controller**
1. Power knop aandoen en bindknop ingedrukt houden. Gelukt zodra LED op Receiver niet meer knippert.


#### Aansluting Fly-Sky FS-iA10B - Raspberry Pi 5

| **Fly-Sky (IBUS)** | **Raspberry Pi 5 (GPIO)** |
|-------------|---------------------------|
| **VCC** | **5V** |
| **GND** | **GND** |
| **RX** | **GPIO 15** |
| **TX** | **GPIO 14** |

---

## Software instellingen Raspberry Pi 5

### Raspi-config

- **Voer het volgende commando uit in de terminal:**

- Ga naar **Interface options** > **Serial Port**:
    * No 
    * Yes

```bash
sudo raspi-config
```

- **Herstart de Raspberry of ga door naar volgende stap:**

```bash
sudo reboot
```


### Config bestanden aanpassen

- **Open het config bestand:**

```bash
sudo nano /boot/firmware/config.txt
```

- **Voeg de volgende regels toe onderaan het bestand:**

```bash
dtparam=uart=on
enable_uart=1
dtoverlay=uart0
core_freq=250
```

- **Herstart de Raspberry of ga door naar volgende stap**

```bash
sudo reboot
```


### Forceer bij opstarten om juiste proces aan signaal te kopellen

- **Open of maak het volgende bestand:**

```bash
sudo nano /etc/udev/rules.d/99-serial.rules
```

- **Voeg de volgende regel toe aan het bestand:**

```bash
KERNEL=="ttyAMA0", SYMLINK+="serial0"
```

- **Herlaad de regels:**

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

- **Herstart de Rapberry**

```bash
sudo reboot
```


### Check instellingen

- **Met het volgende commando zou "/dev/serial0" verwijzen naar "ttyAMA0":**

```bash
ls -l /dev/serial*
```


### Kijken voor dataverkeer met Minicom

- **Download Minicom:**

```bash
sudo apt install minicom
```

- **Kijk of er seriële data binnenkomt via UART:**

```bash
sudo minicom -b 115200 -o -D /dev/serial0
```

