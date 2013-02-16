.. _section-installation-makahiki-dualbooting:

Makahiki installation using dual boot
=====================================

.. warning:: 
   Creating a dual boot environment will overwrite the bootstrap on your computer.
   This can (and most likely will) prevent you from accessing a recovery partition on your
   computer.  While some users have had success restoring their recovery partition after
   installation, restoration of said partition is neither guaranteed nor supported.  If
   you're determined to maintain your recovery partition, it is advisable that you find a
   separate guide to dual booting (as installation details are crucial).

   To compensate for the loss of the recovery partition, we suggest using Windows Backup
   tool to create a system image(full backup) and a System Repair Disk.  Should anything
   go wrong, you can use your System Repair Disk and system image to restore your computer
   to the state it was in when the image was taken.

Create a Repair Disk
--------------------
See `<http://windows.microsoft.com/en-US/windows7/Create-a-system-repair-disc>`_.

Create a System Image
---------------------
See `<http://windows.microsoft.com/en-US/windows7/Back-up-your-files>`_.


Create a Partition
------------------
Create a new partition using the `Windows Disk Management tool <http://technet.microsoft.com/en-us/magazine/gg309170.aspx>`_.  Ubuntu will require two partitions, one for the OS (~15GB recommended), and one for swap space (~2GB recommended).  

Download Ubuntu
---------------
Makahiki supports Ubuntu 12.10, the .iso for which can be found `here <http://www.ubuntu.com/download/help/install-desktop-latest>`_.  Be sure to select the right option for x86 (32 bit) or x64 (64 bit) based systems (drop down on the right side of the page).

Download the .iso file, and `burn the image to a dvd <http://www.ubuntu.com/download/help/burn-a-dvd-on-windows>`_ or `make a bootable flash drive <http://www.ubuntu.com/download/help/create-a-usb-stick-on-windows>`_.

Install Ubuntu
--------------
Follow the `Ubuntu installation guide <http://www.ubuntu.com/download/help/install-desktop-latest>`_, choosing to "Install Ubuntu Alongside Windows <version>" in Step 4.

Point Ubuntu to the empty partition you designated earlier, and let it install (use default settings).  It is recommended that you use the ext2 format for formatting the partition, as it is supported by the Linux OS, and can be accessed in Windows (using Ext2Fsd, a third party program).

After restarting, your computer will load using the `GRUB <https://help.ubuntu.com/community/Grub2 boot loader>`_.  From here, you can choose to access either your Windows or Ubuntu Operating System.  

Mount Windows Drives (Optional)
-------------------------------
Optionally, if you wish to be able to interact with the files on your Windows partition, this `guide on mounting <https://help.ubuntu.com/community/MountingWindowsPartitions>`_ will walk you through the somewhat complicated process.

Mount Linux Drives in Windows (Optional)
----------------------------------------
Windows cannot natively read the ext2 file format, however the third party program Ext2Fsd will allow Windows to mount ext2 formatted drives. Ext2Fsd can be found here: <http://www.ext2fsd.com/>`_.

Once you have the Linux VM, follow the document :ref:`section-installation-makahiki-local` to install Makahiki in a Linux environment.


