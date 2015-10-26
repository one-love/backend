from flask.ext.admin import Admin
from ..models import User
from ..models import Cluster
from ..models import Role
from .view import UserView
from .view import RoleView
from .view import ClusterView

admin = Admin(name='OneLove Admin',
              base_template='admin_master.html',
              template_mode='bootstrap3'
              )

admin.add_view(UserView(User))
admin.add_view(ClusterView(Cluster))
admin.add_view(RoleView(Role))
