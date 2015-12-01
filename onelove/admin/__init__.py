from .view import UserView, RoleView, ClusterView
from ..models import User, Cluster, Role


def register_admin_views(admin):
    return
    admin.add_view(UserView(User))
    admin.add_view(ClusterView(Cluster))
    admin.add_view(RoleView(Role))
