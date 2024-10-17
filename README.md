# PlatformIO + esp-link + Arduino Mega2560

## Description

Shows usage of the https://github.com/jeelabs/esp-link to flash a ATMega2560 board via a ESP8266 board (such as a NodeMCU) over WiFi.

## Preparation

Obtain latest release of esp-link from https://github.com/jeelabs/esp-link/releases.

Flash the downloaded binaries to your ESP8266 board, e.g. using esptool.py. Adapt Paths to Python and esptool.py as needed, or use a GUI flasher.

```
python C:\Users\Max\.platformio\packages\tool-esptoolpy\esptool.py write_flash -fs detect 0x00000 boot_v1.7.bin 0x1000 user1.bin 0x3FC000 esp_init_data_default.bin 0x3FE000 blank.bin
```

After flashing, the ESP8266 should open its own WiFi access point with "ESP" in the name. Connect to it and use the web interface to connect the ESP to your actual home network. Note down the ESP8266's new IP address in your homework for later.

## Wiring

Note: It is in general advisible to use a level-translator for the UART connection between the ESP8266 (3.3V) and the Mega2560 (5V). 
In my tests I left this out since I trust in [this Hackaday article](https://hackaday.com/2022/05/12/is-esp8266-5-v-tolerant-this-curve-tracer-says-yes/) that says it *can* handle 5V. Try with caution.

* NodeMCU "RX" ↔ "TX0" of Mega2560
* NodeMCU "TX" ↔ "RX0" of Mega2560
* NodeMCU GPIO12 (="D6") ↔ "RESET" of Mega2560
* NodeMCU GND ↔ GND of Mega2560 (can already implicitly exist if both devices are on the same USB hub)

**Note:** All of these pin assignments are changable in the esp-link's web interface. Alternative UART pins and a different reset GPIO pin can be set. In this example, **all defaults** were used.

**Note:** It is very important to connect the ESP8266 to "TX0 / RX0", not any other serial pair. The bootloader only responds to the first serial.

## Configuration

In the `platformio.ini` file, use the IP address of your esp-link device instead in `upload_port` and `monitor_port`.

```ini
upload_port = 192.168.0.240
upload_protocol = custom
upload_command = $PYTHONEXE -u esplink_upload.py -P $UPLOAD_PORT  $SOURCES
monitor_port = socket://192.168.0.240:2323
```

## Expected upload output

```
Looking for upload port...
Using manually specified: 192.168.0.240
Uploading .pio\build\megaatmega2560\firmware.hex
==== ESP-LINK UPLOAD ===
Uploading to http://192.168.0.240
Trying to reset board.
NOT READY
Warning: Retrying to sync to Optiboot.
Trying to reset board.
SYNC at 115200 baud, board 1e.98.01, hardware v15, firmware 2.10
Reset to sync with Optiboot OK.
Uploading firmware .pio\build\megaatmega2560\firmware.hex
Success. 2696 bytes at 115200 baud in 3.3s, 794B/s 6% efficient
Firmware uploaded successfully
=========== [SUCCESS] Took 11.43 seconds ===========
```

## Expected serial output

Since the esp-link is a remote serial bridge, we can as per above have a remote serial monitor by telling miniterm to connect to the ESP8266's port. Every serial monitor opening will cause a reset of the Arduino.

```
Executing task: C:\Users\Max\AppData\Roaming\Python\Python311\Scripts\platformio.exe device monitor --environment megaatmega2560 

--- Terminal on socket://192.168.0.240:2323 | 9600 8-N-1
--- Available filters and text transformations: colorize, debug, default, direct, hexlify, log2file, nocontrol, printable, send_on_enter, time
--- More details at https://bit.ly/pio-monitor-filters
--- Quit: Ctrl+C | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H
Blinky from Mega!
Blinky from Mega!
Blinky from Mega!
Blinky from Mega!
Blinky from Mega!
```

**Note:** If your sketch uses a different baud rate, you can either change the baud rate in the `/console.html` website or by a direct POST request
```bash
curl -X POST "http://192.168.0.240/console/baud?rate=9600"
```