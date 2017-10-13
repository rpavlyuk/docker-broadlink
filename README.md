# docker-broadlink
BroadLink is very popular solution for making your home smart. It offers Wi-Fi switches, sensors, remote controls and some other interesting devices. You can find more about BroadLink at their home WEB-page: http://www.ibroadlink.com

BroadLink vendor provides mobile phone application called ```e-Control``` to manage the devices. However, BroadLink doesn't provide official SDK and API and that creates problem if you want to integrate your BroadLink devices into "smart home" system along with the others you already have.

Luckly, we have a Python library created by Matthew Garrett aka **mjg59**: https://github.com/mjg59/python-broadlink. I've put this library inside the Docker container and added some other useful stuff that you would probably like.

## What is inside the Docker image?
* Fork of ```python-broadlink``` library by user ```eschava``` (to have ```get_energy()``` available)
* ```python-broadlink``` installed as Python library
* Pre-configured Zabbix Agent to allow monitoring of certain parameters

## Running broadlink docker image
TBD
