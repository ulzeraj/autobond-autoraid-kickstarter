#!/usr/bin/python2.6
#-*- coding: utf-8 -*-
import signal
import subprocess
from glob import glob
from os import listdir
from os.path import basename, dirname

label = 'CentOS_6.9_Final'


def listifaces():
    ethernet = []
    for iface in listdir('/sys/class/net/'):
        if iface != 'lo':
            ethernet.append(iface)
    return ethernet


def listblocks():
    drive = '/sys/block/*/device'
    return [basename(dirname(d)) for d in glob(drive)]


def listlabel(dev):
    command = '/usr/sbin/blkid -o value -s LABEL {0}'.format(dev)
    try:
        lsblk = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output = lsblk.communicate()[0].rstrip()
        return output
    except:
        pass


def discoverdisks():
    disklist = []
    for dev in listblocks():
        removable = open('/sys/block/{0}/removable'.format(dev)).readline()
        disklist.append([dev, removable.rstrip()])
    return disklist


def getinternal(disklist):
    internal = []
    for dev in disklist:
        if dev[1] == '0':
            internal.append(dev[0])
    return internal


def getremovable(disklist):
    removable = []
    for dev in disklist:
        if dev[1] == '1':
            removable.append(dev[0])
    return removable


def getinstallmedia(disklist):
    for dev in disklist:
        firstpart = '/dev/{0}1'.format(dev[0])
        relativep = '{0}1'.format(dev[0])
        partlabel = listlabel(firstpart)
        if  partlabel == label:
            return relativep


discoverdisks = discoverdisks()
source = getinstallmedia(discoverdisks)
localdisks = sorted(getinternal(discoverdisks))[:2]
nics = ','.join(listifaces())

kickstart = """lang en_US.UTF-8
keyboard us
network --bootproto=static --device=bond0 --bootproto=dhcp --bondopts=miimon=100,mode=active-backup --bondslaves="{0}"
firewall --enabled --ssh
timezone --utc America/Sao_Paulo
zerombr yes
clearpart --drives="{1}" --all --initlabel
bootloader --location=mbr --driveorder="{1}" --append="crashkernel=auto rhgb quiet" 
# Please remember to change this. In case you don't the password encrypted bellow is "cheekibreeki".
rootpw  --iscrypted $6$JDAL2eOJcBzAkykb$o9v9XAVC2i9YLyMGWEyG60SO2vXSDO.C42CoI/M5Ai/UCVOoWD6SH1sd9e7ImZJj/rx1aljJShdVjKHJgRa8s/
authconfig --enableshadow --passalgo=sha512
selinux --enabled
skipx

# Disk proposal bellow. You should customize it to your needs.
part raid.0 --size=512 --ondisk {2} --asprimary
part raid.1 --size=512 --ondisk {3} --asprimary
part raid.2 --size=40000 --ondisk {2} --asprimary
part raid.3 --size=40000 --ondisk {3} --asprimary
part raid.4 --size=10000 --ondisk {2} --asprimary --grow
part raid.5 --size=10000 --ondisk {3} --asprimary --grow
raid /boot --fstype xfs --level=RAID1 --device=md0 raid.0 raid.1
raid pv.1  --fstype "physical volume (LVM)" --level=RAID1 --device=md1 raid.2 raid.3
raid pv.2  --fstype "physical volume (LVM)" --level=RAID1 --device=md2 raid.4 raid.5
volgroup system --pesize=32768 pv.1
volgroup data --pesize=32768 pv.2
logvol / --fstype xfs --name=root --vgname=system --size=4096 --fsoptions="noatime,nodiratime"
logvol /usr --fstype xfs --name=usr --vgname=system --size=8192 --fsoptions="noatime,nodiratime,nodev"
logvol /var --fstype xfs --name=var --vgname=system --size=4096 --fsoptions="noatime,nodiratime,nodev,nosuid"
logvol /var/log --fstype xfs --name=varlog --vgname=system --size=4096 --fsoptions="noatime,nodiratime,nodev,nosuid,noexec"
logvol /tmp --fstype xfs --name=tmp --vgname=system --size=4096 --fsoptions="noatime,nodiratime,nodev,nosuid"
logvol /opt --fstype xfs --name=opt --vgname=system --size=512 --fsoptions="noatime,nodiratime,nodev,nosuid"
logvol /srv --fstype xfs --name=srv --vgname=system --size=5120 --fsoptions="noatime,nodiratime,nodev,nosuid,noexec"
logvol swap --fstype swap --name=swap --vgname=system --size=4096
logvol /home --fstype xfs --name=home --vgname=data --size=512 --fsoptions="noatime,nodiratime,nodev,nosuid,noexec"

%packages
@base
@console-internet
@core
@debugging
@directory-client
@hardware-monitoring
@java-platform
@large-systems
@network-file-system-client
@performance
@perl-runtime
@portuguese-support
@server-platform
@server-policy
@workstation-policy
pax
python-dmidecode
oddjob
sgpio
device-mapper-persistent-data
samba-winbind
certmonger
pam_krb5
krb5-workstation
perl-DBD-SQLite
dos2unix
ca-certificates
dhcp
nfs-utils
ipa-client
tcpdump
expect
%post""".format(nics, ','.join(localdisks), localdisks[0], localdisks[1])

if __name__ == '__main__':
    incks = open('/tmp/autogen.ks', 'w+')
    incks.write(kickstart)
    incks.close()
