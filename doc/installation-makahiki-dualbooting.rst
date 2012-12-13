.. _section-installation-makahiki-dualbooting:

Dual Booting Linux and Windows
==============================
!!WARNING!!
-----------
Creating a dual boot environment will overwrite the bootstrap on your computer.  This can (and most likely will) prevent you from accessing a recovery partition on your computer.  Therefore, it is highly recommended that you backup your data (both now, and regularly thereafter).  This can be achieved by using the built in `Windows Backup <http://windows.microsoft.com/en-US/windows7/Back-up-your-files>`_, or simply saving important files off to an external hard drive.  Creating a full backup will allow you to restore your system, programs, and files should anything go wrong (now or ever).

While some users have had success restoring their recovery partition after installation, restoration of said partition is neither guaranteed nor supported.  If you're determined to maintain your recovery partition, it is advisable that you find a separate guide to dual booting (as installation details are crucial).  Otherwise, continue to the steps below.




1. Create a Partition
---------------------
If you have an EMPTY partition on your hard drive (about 15 GB or so), you can skip this step.  Otherwise, create a new partition using the `Windows Disk Management tool <http://technet.microsoft.com/en-us/magazine/gg309170.aspx>`_.

2. Download Ubuntu 12.10
------------------------
Makahiki supporrts Ubuntu 12.10, the .iso for which can be found `here <http://www.ubuntu.com/download/help/install-desktop-latest>`_.  Be sure to select the right option for x86 (32 bit) or x64 (64 bit) based systems (drop down on the right side of the page).

Download the .iso file, and `burn the image to a dvd <http://www.ubuntu.com/download/help/burn-a-dvd-on-windows>`_ or `make a bootable flash drive <http://www.ubuntu.com/download/help/create-a-usb-stick-on-windows>`_.

3. Install Ubuntu 12.10
-----------------------
Follow the `Ubuntu installation guide <http://www.ubuntu.com/download/help/install-desktop-latest>`_, choosing to "Install Ubuntu Alongside Windows <version>" in Step 4.

Point Ubuntu to the empty partition you designated earlier, and let it install (use default settings)

After restarting, your computer will load using the `GRUB <https://help.ubuntu.com/community/Grub2 boot loader>`_.  From here, you can choose to access either your Windows or Ubuntu Operating System.  

4. Mount Windows Drives (Optional)
----------------------------------
Optionally, if you wish to be able to interact with the files on your Windows partition, this `guide on mounting <https://help.ubuntu.com/community/MountingWindowsPartitions>`_ will walk you through the somewhat complicated process.

