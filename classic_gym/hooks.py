app_name = "classic_gym"
app_title = "Classic Gym"
app_publisher = "Polito"
app_description = "This app manages the day to day running of a local gym"
app_email = "omondipaulok@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/classic_gym/css/classic_gym.css"
# app_include_js = "/assets/classic_gym/js/classic_gym.js"

# include js, css files in header of web template
# web_include_css = "/assets/classic_gym/css/classic_gym.css"
# web_include_js = "/assets/classic_gym/js/classic_gym.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "classic_gym/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "classic_gym.utils.jinja_methods",
# 	"filters": "classic_gym.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "classic_gym.install.before_install"
# after_install = "classic_gym.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "classic_gym.uninstall.before_uninstall"
# after_uninstall = "classic_gym.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "classic_gym.utils.before_app_install"
# after_app_install = "classic_gym.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "classic_gym.utils.before_app_uninstall"
# after_app_uninstall = "classic_gym.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "classic_gym.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"classic_gym.tasks.all"
# 	],
# 	"daily": [
# 		"classic_gym.tasks.daily"
# 	],
# 	"hourly": [
# 		"classic_gym.tasks.hourly"
# 	],
# 	"weekly": [
# 		"classic_gym.tasks.weekly"
# 	],
# 	"monthly": [
# 		"classic_gym.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "classic_gym.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "classic_gym.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "classic_gym.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["classic_gym.utils.before_request"]
# after_request = ["classic_gym.utils.after_request"]

# Job Events
# ----------
# before_job = ["classic_gym.utils.before_job"]
# after_job = ["classic_gym.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"classic_gym.auth.validate"
# ]
