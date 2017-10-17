# docker-broadlink — Docker container to run BroadLink IoT toolset
[BroadLink](http://www.ibroadlink.com) is very popular solution for making your home smart. They offer Wi-Fi switches, sensors, remote controls and some other quite interesting devices. You can find more about BroadLink on their official WEB-page: http://www.ibroadlink.com

BroadLink's vendor provides mobile phone application called [e-Control](https://itunes.apple.com/app/broadlink-e-control/id793152994?mt=8) to manage the devices. However, what BroadLink doesn't provide is the official SDK and/or API and that creates a problem if you want to integrate your BroadLink devices into your "smart home" system along with the other IoT devices you already have.

Luckly, we have Python library created by **Matthew Garrett** aka @mjg59: https://github.com/mjg59/python-broadlink. What I did in scope of this project is that I've put this library inside Docker container and added some other useful stuff that you would probably like.

## What is inside the Docker image?
* Fork of ```python-broadlink``` library by user @eschava (to have ```get_energy()``` available)
* ```python-broadlink``` installed as Python library
* Pre-configured [Zabbix Agent](https://www.zabbix.com/zabbix_agent) to allow monitoring of certain parameters

## Running broadlink docker image
### Pre-requisites
* Please, make sure you have [Docker](http://docker.io) installed and configured before you continue with any further steps.
* Setup all BroadLink devices first using [e-Control](https://itunes.apple.com/app/broadlink-e-control/id793152994). Otherwise the system on the container won't be able to use them correctly.

### Run using systemdock (recommended)
[SystemDock](https://github.com/rpavlyuk/systemdock) is the tool to run Docker containers as ```systemd``` service.
* Install systemdock by following the instructions from https://github.com/rpavlyuk/systemdock
* Within the project root, change directory to where the systemdock profile is:
```
cd systemdock-broadlink/
```
* If you're using RedHat-based OS and installed ```systemdock``` using RPM installer (see above) then:
```
sudo make install-rpm clean
```
* Otherwise, use classic method:
```
sudo make install clean
```
* Check configuration file ```/etc/systemdock/containers.d/broadlink/config.yml```. Make sure that TCP ports 10555 and 8888 are not in-use by any existing processes on the host system.
One more thing in file ```/etc/systemdock/containers.d/broadlink/config.yml``` is changing Zabbix Server IP and hostname (in case you're using it). Change ```192.168.1.5``` and ```liberty.home.pavlyuk.lviv.ua``` provided as a sample to something relevant to your configuration. 

* Enable the service on system boot:
```
sudo systemctl enable systemdock-broadlink
```
* Start the service:
```
sudo systemctl start systemdock-broadlink
```
* You can monitor service log by calling ```journalctl``` (hit CRTL+C to abort):
```
journalctl -u systemdock-broadlink -f
```

### Plain run of the container
* You can run the container as any other Docker container:
```
docker run -it --name broadlink -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 8888:8888 -p 10555:10555 --net host docker.io/rpavlyuk/c7-broadlink
```
> **NOTE:** You have to run container with ```network_mode``` set to ```host```. Otherwise, it won't be able to communicate with BroadLink devices using multicast UDP packages.
* If you plan to use it with Zabbix Server, then run the following commands to configure the agent (replace ```ZABBIX_SERVER_IP``` and ```ZABBIX_SERVER_HOSTNAME``` with your own values):
```
docker exec broadlink perl -pi -e "s/\=127.0.0.1/\=ZABBIX_SERVER_IP/gi" /etc/zabbix/zabbix_agentd.conf
docker exec broadlink perl -pi -e "s/\=zabbix.server/\=ZABBIX_SERVER_HOSTNAME/gi" /etc/zabbix/zabbix_agentd.conf
docker exec broadlink systemctl restart zabbix-agent
```

## Using BroadLink toolset
### Using python-broadlink
Once you have the container installed, you can try using it to test any programming samples like described by @mjg59
* First, enter the container's shell:
```
docker exec -it broadlink bash
```
* Try communicating and controlling your BroadLink devices using the library:
```
[root@broadlink ~]# python
Python 2.7.5 (default, Aug  4 2017, 00:39:18)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import broadlink
>>>
>>> devices = broadlink.discover(timeout=5)
>>>
>>> devices
[<broadlink.sp2 instance at 0x7fe69e48c315>, <broadlink.a1 instance at 0x7fe69e43c9d0>]
>>>
>>>
>>> devices[0].auth()
True
>>>
>>> devices[0].check_power()
False
>>>
>>> devices[0].get_energy()
0.0
```
You can find more samples in ```python-broadlink``` [manual](https://github.com/mjg59/python-broadlink#example-use).

### Using with Zabbix
Container comes with Zabbix Agent enabled that you can use to collect various metrics from your BroadLink devices.

Currently two types of devices are supported:
* SP series (SP2, SP3, SP3S). Supported keys: ```power```, ```energy``` (SP3S only)
* A1. Supported keys: ```temperature```, ```humidity```, ```light```, ```air_quality```, ```noise```
But this list can be extended by adding propper helper scripts and Zabbix Agent params.

First, let's try if Zabbix Agent running on the container is accessible by the server. So, log into the shell of the box where you have Zabbix Server running and try this:
* For A1 device:
```
zabbix_get -s <ZABBIX_AGENT_IP> -p 10555 -k "broadlink.device.a1.get[<MAC_ADDRESS_OF_BL_DEVICE>, <IP_OF_BL_DEVICE>, <KEY>]"
```
Example:
```
zabbix_get -s 192.168.1.6 -p 10555 -k "broadlink.device.a1.get[34EA34E52EDD, 192.168.3.12, temperature]"
```
* For SPx device:
```
zabbix_get -s <ZABBIX_AGENT_IP> -k "broadlink.device.sp2.get[<MAC_ADDRESS_OF_BL_DEVICE>, <IP_OF_BL_DEVICE>, <KEY>]"
```
Example:
```
zabbix_get -s 192.168.1.6 -p 10555 -k "broadlink.device.sp2.get[34EA34BD2E4B, 192.168.3.11, power]"
```

Correct response should look like these:
```
[rpavlyuk@liberty ~]$ zabbix_get -s 192.168.1.6 -p 10555 -k "broadlink.device.a1.get[34EA34E52EDD, 192.168.3.12, temperature]"
21.5
[rpavlyuk@liberty ~]$  zabbix_get -s 192.168.1.6 -p 10555 -k "broadlink.device.sp2.get[34EA34BE61CA, 192.168.3.10, energy]"
0.0
[rpavlyuk@liberty ~]$  zabbix_get -s 192.168.1.6 -p 10555 -k "broadlink.device.sp2.get[34EA34BE61CA, 192.168.3.10, power]"
0
```
If you get errors then:
* When using SystemDock, check ```config.yml``` if Zabbix Server IP and and hostname are correct (section ```command.host.post```). In not then correct them and restart the service ```systemdock-broadlink```  
* If not using SystemDock then check if you've executed commands that configure the Agent. This is a snippet of commands **Plain run of the container** (see above)
* Make sure you're trying to call the tight type of the device
* Check file ```/var/log/zabbix/zabbix_agentd.log``` on the container for errors
* Well, if you need backup from me and you can't get around by yourself — open an issue here

Next, let's configure Zabbix Server. 
* There's a sample template in the source code here available. Find the one in folder ```zabbix/templates```.
* Import the template using _Configuration_ > _Templates_ > _Import_ menu from Zabbix Server WEB interface
* Create a new host with name, for example, _BROADLINK_ and assign template ```BroadLink Monitoring``` to it. Also, make sure you specify correct IP of Zabbix agent and port ```10555``` (instead of default ```10050```)
* Now you can update the items in the template so match your confguration. Especially, mac addresses and IPs.
* Yon can now also build your custom graphs and screens


## TO-DO
* Embedd [broadlink-http-rest](https://github.com/radinsky/broadlink-http-rest) project into the container (That's why I've reserved port 8888 for ;))

## Credits
* First of all, to @mjg59 for creating the libraty
* @eschava for adding SP3S device support
* And me :) [Roman Pavlyuk](mailto:roman.pavlyuk@gmail.com) aka @rpavlyuk http://roman.pavlyuk.lviv.ua/

