# Winterevent 2024 Embedded Talk

## 🔦 Firmware Flash 

- Supported chips: `esp32`, `esp8266`, `esp32s2`

- Images [Micropython source](https://micropython.org/download):
  - `esp32`: [firmware/ESP32_GENERIC-20240105-v1.22.1.bin](firmware/ESP32_GENERIC-20240105-v1.22.1.bin)
  - `esp32s2`: [firmware/LOLIN_S2_MINI-20240105-v1.22.1.bin](firmware/LOLIN_S2_MINI-20240105-v1.22.1.bin)
  - `esp8266`: [firmware/ESP8266_GENERIC-20240105-v1.22.1.bin](firmware/ESP8266_GENERIC-20240105-v1.22.1.bin)

- Steps:
  1. install `esptool` for flashing: `pip install esptool`
  2. find port (macOS): `l /dev/cu.* `
  3. execute (e.g. port: `/dev/cu.usbmodem01`, image: `firmware/ESP32_GENERIC-20240105-v1.22.1.bin`, chip: see supported chips)
        ```
        source scripts/<chip>_firmware_flash.sh <port> <image>
        ```

## ⚙️ Setting Up
1. create `common/secrets.py` file and add Wi-Fi connection details, variables: `SSID`, `PASSWORD` (`.gitignore` ignores file)
2. plug device to PC with cable that supports data transfer (`USB C`, `micro USB`)

## 🏁 Quickstart Guide
1. download [Thonny app](https://thonny.org) on computer
2. right corner or the app, select port for that device (e.g. `ESP32 /dev/cu.usbserial-0001` on Mac/Linux, `COM*` on Windows)
3. if that didn't connect the device (green play button should appear if it's connected/detected):
   1. try clicking on the red stop button in the Thonny
   2. try selecting another device for that same chip (e.g. ESP32 or ESP8266)
   3. sometimes it takes few seconds for computer to detect device (restart from `step 1`)
4. developing your own app
   1. use `main.py` file as entry point for device
   2. use libraries from `src/common` folder to extend your logic
   3. use `src/examples` for examples and quickstart
5. right click on `src` folder in Thonny file explorer > `Upload to /` to upload `src` to device
6. create `main.py` file in the device file explorer as a device starting point when connected with the power cable
7. from this point, two options are available:
   1. restart device with `RST` button on it (runs `main.py` file on the device) - you won't be able to see logs/prints
   2. click green `play` button in Thonny (it runs opened file in Thonny) - you'll be able to see logs/prints 
8. (optional) change `src/common` libraries if needed to fit your design
