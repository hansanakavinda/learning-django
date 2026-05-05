# jobboard/routers.py


class JobsRouter:
    """
    Routes jobs app to the default SQLite database.
    """

    # These are the apps this router is responsible for
    route_app_labels = {'jobs', 'admin', 'auth', 'contenttypes', 'sessions', 'authtoken'}
    #                                      ↑
    #              Django's built-in apps also need to be routed
    #              they should stay on the default SQLite database

    def db_for_read(self, model, **hints):
        """Which database to use when reading."""
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None
        #       ↑
        #  Returning None means
        # "I don't know, ask the next router"

    def db_for_write(self, model, **hints):
        """Which database to use when writing."""
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Can these two objects have a relationship (ForeignKey)?
        Only allow relations if both objects are in the same database.
        """
        if (
            obj1._meta.app_label in self.route_app_labels and
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Should this app's migrations run on this database?
        """
        if app_label in self.route_app_labels:
            return db == 'default'
        return None


class NeonRouter:
    """
    Routes home app to the Neon PostgreSQL database.
    """

    route_app_labels = {'home'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'neon'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'neon'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels and
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'neon'
        return None