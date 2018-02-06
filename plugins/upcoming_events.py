# -*- coding: utf-8 -*-

"""Upcoming events."""

from __future__ import unicode_literals

import os
import uuid
import natsort
import operator

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from nikola import utils
from nikola.plugin_categories import RestExtension
from nikola.packages.datecond import date_in_range

class UpcomingEventsPlugin(RestExtension):
    """Upcoming events."""

    name = "upcoming_events"

    def set_site(self, site):
        """Set Nikola instance and register directives."""
        super(UpcomingEventsPlugin, self).set_site(site)
        directives.register_directive('upcoming-events', UpcomingEvents)
        UpcomingEvents.site = site


class UpcomingEvents(Directive):
    option_spec = {
        'count': int,
        'lang': directives.unchanged,
        'template': directives.path,
    }

    def run(self):
        """Run post-list directive."""

        count = int(self.options.get('count'))
        lang = self.options.get('lang', utils.LocaleBorg().current_lang)
        template = self.options.get('template', 'post_list_directive.tmpl')

        _now = utils.current_time()
        posts = [post for post in self.site.timeline
                 if post.section_slug() == "events" and
                 utils.to_datetime(post.meta[lang]['event_end']) > _now]

        if not posts:
            return []

        for post in posts:
            bp = post.translated_base_path(lang)
            if os.path.exists(bp):
                self.state.document.settings.record_dependencies.add(bp)

        posts.sort(key=lambda x: utils.to_datetime(post.meta[lang]['event_start']))
        posts = posts[:count]

        self.state.document.settings.record_dependencies.add("####MAGIC####TIMELINE")
        for d in self.site.template_system.template_deps(template):
            self.state.document.settings.record_dependencies.add(d)

        template_data = {
            'lang': lang,
            'posts': posts,
            'date_format': self.site.GLOBAL_CONTEXT.get('date_format')[lang],
            'messages': self.site.MESSAGES,
            '_link': self.site.link,
        }
        output = self.site.template_system.render_template(
            template, None, template_data)

        return [nodes.raw('', output, format='html')]

