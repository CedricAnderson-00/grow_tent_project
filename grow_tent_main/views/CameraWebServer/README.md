# inland ESP32-Cam

This needs to outline all of the steps to get an inland esp32 cam working

use jumper wire to short ground to IOO port(terminal to the left of ground pin) to enter program mode

load all of the zip files into arduino IDE
    Sketch>Include Library>Add .zip library  # select the location of the zip drives and load each one

from main directory in terminal copy the following:
    <sed -i -e 's/=python /=python3 /g' ~/Library/Arduino15/packages/esp32/hardware/esp32/*/platform.txt>

click "serial monitor" icon in top right and hit the reset button to see ip address of camera

change byte reading to higher frame to interpret values