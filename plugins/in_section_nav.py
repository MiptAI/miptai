# -*- coding: utf-8 -*-

"""Calc prev and next post in section."""

import blinker
from collections import defaultdict
from nikola.plugin_categories import SignalHandler

class InSectionNavPlugin(SignalHandler):
    """Calc prev and next post in section."""

    name = "in_section_nav"

    def set_site(self, site):
        """Set Nikola instance and attach signals."""

        super(InSectionNavPlugin, self).set_site(site)
        blinker.signal("scanned").connect(self._do_extra_navigation)

    def _do_extra_navigation(self, site):
        # Needed to avoid strange errors during tests
        if site is not self.site:
            return

        section_posts = defaultdict(lambda: [])

        for post in site.timeline:
            # Don’t classify posts that are hidden (draft/private/future)
            if post.is_post and not post.use_in_feeds:
                continue

            section_posts[post.section_slug()].append(post)

        for _, posts in section_posts.items():
            posts[0].next_post_in_section = None
            posts[-1].prev_post_in_section = None

            for i, p in enumerate(posts[1:]):
                p.next_post_in_section = posts[i]
            for i, p in enumerate(posts[:-1]):
                p.prev_post_in_section = posts[i + 1]

