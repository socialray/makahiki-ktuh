'''System Administration AdminSite.

Created on Feb 8, 2013

@author: Cam Moore
'''


from django.contrib.admin.sites import AdminSite


challenge_designer_site = AdminSite(name="Challenge Designer Admin")
challenge_manager_site = AdminSite(name="Challenge Manager Admin")
sys_admin_site = AdminSite(name='System Administration Admin')
