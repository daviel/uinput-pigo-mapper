#!/usr/bin/env python3

import sys
import libevdev
from libevdev import InputEvent
import RPi.GPIO as GPIO
import time

buttons = [
  {
	 # up BCM: 22
	'bcm': 22,
	'name': 'UP',
	'target_ev': 'KEY_UP',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # down BCM: 4
	'bcm': 4,
	'name': 'DOWN',
	'target_ev': 'KEY_DOWN',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # right BCM: 27
	'bcm': 27,
	'name': 'RIGHT',
	'target_ev': 'KEY_RIGHT',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # left BCM: 17
	'bcm': 17,
	'name': 'LEFT',
	'target_ev': 'KEY_LEFT',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # a BCM: 23
	'bcm': 23,
	'name': 'A',
	'target_ev': 'KEY_Z',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # b BCM: 1
	'bcm': 1,
	'name': 'B',
	'target_ev': 'KEY_B',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # x BCM: 25
	'bcm': 25,
	'name': 'X',
	'target_ev': 'KEY_X',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # y BCM: 12
	'bcm': 12,
	'name': 'Y',
	'target_ev': 'KEY_Y',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # start BCM: 20
	'bcm': 20,
	'name': 'START',
	'target_ev': 'KEY_ENTER',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # select BCM: 26
	'bcm': 26,
	'name': 'SELECT',
	'target_ev': 'KEY_ESC',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # home BCM: 0
	'bcm': 0,
	'name': 'HOME',
	'target_ev': 'KEY_W',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # special BCM: 7
	'bcm': 7,
	'name': 'SPECIAL',
	'target_ev': 'KEY_W',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # SL1 BCM: 15
	'bcm': 15,
	'name': 'SL1',
	'target_ev': 'KEY_W',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # SR1 BCM: 16
	'bcm': 16,
	'name': 'SR1',
	'target_ev': 'KEY_W',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # SL2 BCM: 14
	'bcm': 14,
	'name': 'SL2',
	'target_ev': 'KEY_W',
	'pressed': 0,
	'mouse_move': 0
  },
  {
	 # SR2 BCM: 24
	'bcm': 24,
	'name': 'SR2',
	'target_ev': 'KEY_W',
	'pressed': 0,
	'mouse_move': 0
  }
]

ALL_KEYS = libevdev.EV_KEY.__dict__
ALL_RELS = libevdev.EV_REL.__dict__

def main(args):
	for arg in args:
		arrArg = arg.split("=")
		if len(arrArg) == 2:
			print(arrArg)
			left = arrArg[0].upper()
			right = arrArg[1]

			for button in buttons:
				if button["bcm"] == left or button["name"] == left:
					button["target_ev"] = right
					print(button)
		elif len(arrArg) == 3:
			print(arrArg)
			left = arrArg[0].upper()
			middle = arrArg[1]
			right = arrArg[2]
			for button in buttons:
				if button["bcm"] == left or button["name"] == left:
					button["target_ev"] = middle
					button["mouse_move"] = int(right)

	GPIO.setmode(GPIO.BCM)
	for button in buttons:
		#print(button, button["bcm"])
		GPIO.setup(button["bcm"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	dev = libevdev.Device()
	dev.name = "PiGo device"

	for event in libevdev.EV_KEY.__dict__:
		if event.startswith("KEY_") or event.startswith("BTN_"):
			#print(libevdev.EV_KEY.__getattribute__(event))
			dev.enable(libevdev.EV_KEY.__getattribute__(event))
	for event in libevdev.EV_REL.__dict__:
		if event.startswith("REL_"):
			#print(libevdev.EV_REL.__getattribute__(event))
			dev.enable(libevdev.EV_REL.__getattribute__(event))

	try:
		uinput = dev.create_uinput_device()
		print("New device at {} ({})".format(uinput.devnode, uinput.syspath))

		# Sleep for a bit so udev, libinput, Xorg, Wayland, ... all have had
		# a chance to see the device and initialize it. Otherwise the event
		# will be sent by the kernel but nothing is ready to listen to the
		# device yet.
		time.sleep(1)

		while True:
			for button in buttons:
				events = []

				if GPIO.input(button["bcm"]) == GPIO.HIGH:
					button['pressed'] = True

					if button["target_ev"] in ALL_KEYS:
						events.append(InputEvent(libevdev.EV_KEY.__getattribute__(button["target_ev"]), 1))
					elif button["target_ev"] in ALL_RELS:
						events.append(InputEvent(libevdev.EV_REL.__getattribute__(button["target_ev"]), button["mouse_move"]))
					
				elif button['pressed'] == True and GPIO.input(button["bcm"]) == GPIO.LOW:
					button['pressed'] = False

					if button["target_ev"] in ALL_KEYS:
						events.append(InputEvent(libevdev.EV_KEY.__getattribute__(button["target_ev"]), 0))
					elif button["target_ev"] in ALL_RELS:
						events.append(InputEvent(libevdev.EV_REL.__getattribute__(button["target_ev"]), 0))

				if len(events) > 0:
					events.append(InputEvent(libevdev.EV_SYN.SYN_REPORT, 0))
					uinput.send_events(events)
			time.sleep(1 / 100)
	except OSError as e:
		print(e)


if __name__ == "__main__":
	main(sys.argv)

