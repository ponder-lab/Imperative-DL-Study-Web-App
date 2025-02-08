from .auth_views import user_login, user_logout, register, special
from .bugfix_views import categorizations_by_bugFixID, BugFixesTableView
from .categorization_views import AddCategorization, success_categorization, update_categorization, delete_categorization, categorizations_by_userID
from .commit_views import CommitsTableView, CommitDetailsTableView
from .general_views import index, permission_denied, activateLinks, add_category, AddCategorizer