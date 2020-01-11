# lights
Halloween costume lights, stranger things style

In the stranger things TV show there was a wall: https://youtu.be/jIQ9z2bxXyg?t=163
I've decided to create the same thing running on two T-shirts independently: https://photos.app.goo.gl/dhHES4FaSokraK45A (It got better in later versions)

Requirements I've had in mind were:
	Two halves have to work completely independently
	Configuration and message can be changed using my phone
	If it gets unplugged and plugged back in it has to keep working as if nothing happened
	Doesn't need reliable connection

This code is a simple flask server + a controler for WS2811 lights. Each of the T-shirts has a Raspberry pi zero W running this code, the only thing different is the lights to letters mapping.

Raspberry Pis connect to a hotspot running on my phone if it is turned on. Each Pi is running a flask server from this repository, phone is running a simple Android app sending requests to modify the configuration and message.
