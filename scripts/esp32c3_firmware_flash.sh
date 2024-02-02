echo "port: $1"
echo "image: $2\n"

esptool.py --port $1 erase_flash
esptool.py --chip esp32c3 --port $1 --baud 460800 write_flash -z 0x0 $2
