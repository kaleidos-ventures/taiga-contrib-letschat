# Copyright (C) 2014-2017 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2017 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2017 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2017 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# Copyright (C) 2014-2017 Andrea Stagi <stagi.andrea@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.apps import AppConfig
from django.conf.urls import include, url


def connect_taiga_contrib_letschat_signals():
    from django.db.models import signals
    from taiga.projects.history.models import HistoryEntry
    from . import signal_handlers as handlers
    signals.post_save.connect(handlers.on_new_history_entry, sender=HistoryEntry, dispatch_uid="taiga_contrib_letschat")


def disconnect_taiga_contrib_letschat_signals():
    from django.db.models import signals
    signals.post_save.disconnect(dispatch_uid="taiga_contrib_letschat")


class TaigaContribLetsChatAppConfig(AppConfig):
    name = "taiga_contrib_letschat"
    verbose_name = "Taiga contrib LetsChat App Config"

    def ready(self):
        from taiga.base import routers
        from taiga.urls import urlpatterns
        from .api import LetsChatHookViewSet

        router = routers.DefaultRouter(trailing_slash=False)
        router.register(r"letschat", LetsChatHookViewSet, base_name="letschat")
        urlpatterns.append(url(r'^api/v1/', include(router.urls)))

        connect_taiga_contrib_letschat_signals()
