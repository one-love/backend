from flask_admin.contrib.mongoengine import ModelView
from flask_security.core import current_user


class RoleView(ModelView):
    column_filters = ['name']

    column_searchable_list = ('name', 'description')

    def is_accessible(self):
        return (
            current_user.is_authenticated() and
            current_user.has_role('admin')
        )


class UserView(ModelView):
    column_list = ('id', 'active', 'email', 'first_name', 'last_name', 'roles')
    column_filters = ['email']

    column_searchable_list = ('first_name', 'last_name', 'email')
    column_editable_list = ['first_name', 'last_name']

    column_exclude_list = ['password']

    form_ajax_refs = {
        'roles': {
            'fields': ('name',)
        }
    }

    def is_accessible(self):
        return (
            current_user.is_authenticated() and
            current_user.has_role('admin')
        )


class ClusterView(ModelView):
    column_list = ('id', 'name', 'applications', 'providers', 'roles')
    column_filters = ['name']

    column_searchable_list = ('name',)
    column_editable_list = ['name']

    form_ajax_refs = {
        'roles': {
            'fields': ('name',)
        }
    }

    form_subdocuments = {
        'applications': {
            'form_subdocuments': {
                None: {
                    # 'form_columns': ('name',),
                    'form_rules': ('name', 'galaxy_role', 'application_name'),
                    'form_widget_args': {
                        'name': {
                            'style': 'color: red'
                        }
                    }
                }
            }
        },
        'providers': {
            'form_subdocuments': {
                None: {
                    'form_columns': ('name',)
                }
            }
        }
    }

    def is_accessible(self):
        return (
            current_user.is_authenticated() and
            current_user.has_role('admin')
        )
