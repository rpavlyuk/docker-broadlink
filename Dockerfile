FROM centos:7
MAINTAINER "Roman Pavlyuk" <roman.pavlyuk@gmail.com>

ENV container docker

RUN yum install -y epel-release

RUN yum update -y

RUN yum install -y less file mc vim-enhanced telnet net-tools which bash-completion openssh-clients

### Let's enable systemd on the container
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup" ]

# Copy RPM packages to Docker image
COPY .rpms/ /rpms/

# Set what we've got
RUN ls -al /rpms

# Install ls-30 and PERL library
RUN yum localinstall -y /rpms/python-broadlink*
RUN systemctl enable broadlink-rest

# Install Zabbix Agent
RUN rpm -Uvh http://repo.zabbix.com/zabbix/3.0/rhel/7/x86_64/zabbix-release-3.0-1.el7.noarch.rpm
RUN yum install -y zabbix-agent
RUN systemctl enable zabbix-agent

# Copy configuration files
COPY ./docker-broadlink/fs/ /

## Expose ports
EXPOSE 6543

### Kick it off
CMD ["/usr/sbin/init"]
