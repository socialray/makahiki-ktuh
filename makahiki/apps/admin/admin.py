'''Defines the three AdminSite.

Created on Feb 8, 2013

@author: Cam Moore
'''


from django.contrib.admin.sites import AdminSite


challenge_designer_site = AdminSite(name="Challenge Designer Admin")
challenge_designer_site.index_template = "admin/designer_index.html"
challenge_manager_site = AdminSite(name="Challenge Manager Admin")
challenge_manager_site.index_template = "admin/admin_index.html"
sys_admin_site = AdminSite(name='System Administration Admin')
developer_site = AdminSite(name="Developer Admin")
developer_site.index_template = "admin/developer_index.html"
