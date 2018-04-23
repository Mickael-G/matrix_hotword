# Matrix Hotword

This is a small service to control the leds on the Matrix Voice.
When a hotword is detected, the leds go green and then return to blue.

Many thanks to https://github.com/syntithenai/opensnips, I am using the MQTT code they created.

Requires:
  - pip install paho-mqtt

To run as services, you need:
  - cd /usr/lib/python2.7/dist-packages
  - sudo ln -s /home/pi/.local/lib/python2.7/site-packages/paho

This is in no way installable software, but here are some steps:
  - Copy the matrix_hotword folder in your /home/pi
  - Copy matrix_hotword.service file into /lib/systemd/system/
  - Then
      - sudo chmod 644 /lib/systemd/system/matrix_hotword.service
      - chmod +x /home/pi/matrix_hotword/service.py
      - sudo systemctl daemon-reload
      - sudo systemctl enable matrix_hotword.service
      - sudo systemctl start matrix_hotword.service
