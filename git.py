from core import plugin, model


class _configbackup(plugin._plugin):
    version = 0.1

    def install(self):
        # Register  Models
        model.registerModel(
            "GitOps",
            "_GitOps",
            "_action",
            "plugins.git.models.action",
        )

    def uninstall(self):
        # de-register  Models
        model.deregisterModel(
            "GitOps",
            "_GitOps",
            "_action",
            "plugins.git.models.action",
        )

    def upgrade(self, LatestPluginVersion):

        if self.version < 0.1:
            model.registerModel(
                "GitOps",
                "_GitOps",
                "_action",
                "plugins.git.models.action",
            )
