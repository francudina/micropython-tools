echo "port: $1"
echo "image: $2\n"

esptool.py --port $1 erase_flash
esptool.py --port $1 write_flash -z 0x1000 $2
