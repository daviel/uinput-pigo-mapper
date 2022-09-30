# uinput-pigo-mapper

## Usage

Call the script like this for keyboard mapping:
sudo python main.py UP=KEY_UP LEFT=KEY_LEFT A=KEY_Z B=KEY_Y

Call the script like this for mouse mapping
sudo python main.py UP=REL_Y=-1 DOWN=REL_Y=1 LEFT=REL_X=1 RIGHT=REL_X=-1 A=BTN_LEFT B=BTN_RIGHT X=BTN_MIDDLE

You can mix buttons and mouse movement but only set one key to one other key.
