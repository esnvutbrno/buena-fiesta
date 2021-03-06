from pathlib import Path

from ._utils import PathValue, BaseConfigurationProtocol


class FilesConfigMixin(BaseConfigurationProtocol):
    MEDIA_ROOT: Path = PathValue()

    STATIC_ROOT: Path = PathValue()

    BUILD_DIR: Path = PathValue()

    # internal for nginx
    MEDIA_URL = "/media/"
    STATIC_URL = "static/"

    def STATICFILES_DIRS(self):
        return [
            (self.BASE_DIR / "static"),
            (self.BASE_DIR / "templates/static"),
        ]

    def USE_WEBPACK_INTEGRITY(self):
        return not self.DEBUG

    @property
    def WEBPACK_LOADER(self):
        return {
            "DEFAULT": {
                "CACHE": False,
                "BUNDLE_DIR_NAME": "./",  # must end with slash
                "STATS_FILE": self.BUILD_DIR / "webpack-stats.json",
                "INTEGRITY": self.USE_WEBPACK_INTEGRITY,
            }
        }
