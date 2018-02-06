# -*- coding: utf-8 -*-

"""Access to global_context from shortcodes."""

import json
import os

from nikola.plugin_categories import ShortcodePlugin
from nikola import utils

class GlobalContextShortcodesPlugin(ShortcodePlugin):
    """Access to global_context from shortcodes."""

    name = "global_context_shortcodes"

    def set_site(self, site):
        """Set Nikola instance and attach signals."""

        super(GlobalContextShortcodesPlugin, self).set_site(site)
        self.site.register_shortcode('global_context', self.handler)

    def handler(self, name, **kwargs):
        return self.site.GLOBAL_CONTEXT[name], ['####MAGIC####CONFIG:GLOBAL_CONTEXT']
