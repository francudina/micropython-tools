echo "port: $1"
echo "image: $2\n"

esptool.py --port $1 erase_flash
esptool.py --port $1 --baud 460800 write_flash --flash_size=detect 0 $2
