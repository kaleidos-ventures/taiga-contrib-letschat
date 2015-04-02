# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
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
from django.db.models import signals

from . import signal_handlers as handlers
from .api import LetsChatHookViewSet
from taiga.projects.history.models import HistoryEntry

# Register route
from taiga.contrib_routers import router
router.register(r"letschat", LetsChatHookViewSet, base_name="letschat")


def connect_taiga_contrib_letschat_signals():
    signals.post_save.connect(handlers.on_new_history_entry, sender=HistoryEntry, dispatch_uid="taiga_contrib_letschat")


def disconnect_taiga_contrib_letschat_signals():
    signals.post_save.disconnect(dispatch_uid="taiga_contrib_letschat")


class TaigaContribLetsChatAppConfig(AppConfig):
    name = "taiga_contrib_letschat"
    verbose_name = "Taiga contrib LetsChat App Config"

    def ready(self):
        connect_taiga_contrib_letschat_signals()
