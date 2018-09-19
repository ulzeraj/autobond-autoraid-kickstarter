install
harddrive --partition=disk/by-label/CentOS_6.9_Final --dir=/
keyboard us
lang en_US.UTf-8
graphical
%pre 
mkdir /mnt/sourcemedia
mount -o ro /dev/disk/by-label/CentOS_6.9_Final /mnt/sourcemedia
/usr/bin/python2.6 /mnt/sourcemedia/create-kickstart.py
umount -f /mnt/sourcemedia
%end
%include /tmp/autogen.ks
