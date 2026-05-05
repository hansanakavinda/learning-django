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
    

class AnalyticsRouter:
    """
    Model-level routing for the analytics app.
    Report       → SQLite (default)
    MetricLog    → Neon PostgreSQL
    """

    # Map each model to its database
    model_database_map = {
        'report': 'default',        # model_name is always lowercase
        'metriclog': 'neon',
    }

    def _get_db(self, model):
        """
        Helper method.
        Checks if the model belongs to analytics app,
        then looks up which database it should use.
        """
        if model._meta.app_label == 'analytics':
            return self.model_database_map.get(model._meta.model_name)
            #                                        ↑
            #                          'report' or 'metriclog'
            #                          always lowercase version
            #                          of the class name
        return None

    def db_for_read(self, model, **hints):
        return self._get_db(model)

    def db_for_write(self, model, **hints):
        return self._get_db(model)

    def allow_relation(self, obj1, obj2, **hints):
        """
        Only allow relations between models
        that live in the same database.
        """
        if (
            obj1._meta.app_label == 'analytics' and
            obj2._meta.app_label == 'analytics'
        ):
            db1 = self.model_database_map.get(obj1._meta.model_name)
            db2 = self.model_database_map.get(obj2._meta.model_name)

            # Only allow relation if both are in same database
            return db1 == db2

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Control which database each model's table gets created in.
        """
        if app_label == 'analytics':
            if model_name is None:
                # If no specific model, allow both databases
                return True

            target_db = self.model_database_map.get(model_name)
            return db == target_db
            #     ↑         ↑
            #  database    database this model
            #  being       should live in
            #  migrated

        return None