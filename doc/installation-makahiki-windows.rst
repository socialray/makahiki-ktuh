.. _section-installation-makahiki-windows:

Installation on Windows
=======================

First off, we must state that native installation of Makahiki on Windows is more complicated and
error-prone than on a Unix environment, because Makahiki uses two technologies (Django and
Memcached) that are more difficult to run in a Windows environment.  

We provide documentation for three approaches to installing Makahiki on Windows:
dual-booting, virtual machine, and native installation. The first two approaches get
around the difficulties of native installation by providing a Unix environment within
Windows.   

If you intend to modify or enhance the Makahiki software (i.e. you plan to be a developer
rather than simply deploy a release of the software), we recommend you use the first two
options which provide a unix environment. 

.. toctree::
   :maxdepth: 2

   installation-using-virtual-machine
   installation-makahiki-dualbooting
   installation-native-windows

