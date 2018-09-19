# autobond-autoraid-kickstarter
Script to generate a kickstart file to Red Hat or Centos for automatic raid and bonding.

This is a proof of concept script to generate kickstart on the fly that can detect and configure your disks and network interfaces to group those into raid and bonding groups respectively. Obviously you will have to customize it to your needs. This is made for a isohybrid install of Centos 6.9 but you can easily customize it to other scenarios.

This is presented as an example and you will probably have to customize it for your installation. I had to go through a small amount of pain and Red Hat documentation pages that annoyingly keep appearing on search results even while being paywalled so I hope this helps someone.

## How does this works
You need to call this script from your main kickstart file (the one which you assign during boot). It runs and generates a file named /tmp/autogen.ks on the installation system which will be used through the include parameter of the main kickstart file.

## How can I use this
You need to download and run the python script. You can do this by downloading it or by adding the file to the custom ISO file and temporarily mounting the install media to run it.
