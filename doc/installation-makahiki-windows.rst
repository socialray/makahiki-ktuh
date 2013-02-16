.. _section-installation-makahiki-windows:

Local Installation on Windows
=============================

First off, we must state that native installation of Makahiki on Windows is more complicated and
error-prone than on a Unix environment, because Makahiki uses two technologies (Django and
Memcached) that are more difficult to install in a Windows environment.  

We thus provide documentation for three approaches to installing Makahiki on Windows:
dual-booting, virtual machine, and native installation. The first two approaches get
around the difficulties of native installation by providing a Unix environment within
Windows.   

If you intend to modify or enhance the Makahiki software (i.e. you plan to be a developer
rather than simply deploy a release of the software), we recommend you use the first two
options which provide a unix environment. 

Our estimated hardware requirements for development use are:
  * CPU: modern dual or quad core
  * RAM: 4 GB
  * Disk space: 10 GB

.. toctree::
   :maxdepth: 2

   installation-makahiki-windows-vm
   installation-makahiki-windows-dualbooting
   installation-makahiki-windows-native

