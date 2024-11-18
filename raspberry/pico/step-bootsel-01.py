# See
# https://github.com/cfreshman/pico-bootsel/tree/master

import bootsel, time, machine

while True:
  if bootsel.pressed():
    print('BOOTSEL pressed')
    while bootsel.pressed():
      time.sleep(.1)
    print('BOOTSEL released')
  time.sleep(.1)
