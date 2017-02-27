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

from django.conf import settings

from taiga.projects.history import services as history_service
from taiga.projects.history.choices import HistoryType

from . import tasks


def _get_project_letschathooks(project):
    letschathooks = []
    for letschathook in project.letschathooks.all():
        letschathooks.append({
            "id": letschathook.pk,
            "url": letschathook.url,
            "token": letschathook.token,
            "notify_config": {
                "notify_epic_create": letschathook.notify_epic_create,
                "notify_epic_change": letschathook.notify_epic_change,
                "notify_epic_delete": letschathook.notify_epic_delete,
                "notify_relateduserstory_create": letschathook.notify_relateduserstory_create,
                "notify_relateduserstory_delete": letschathook.notify_relateduserstory_delete,
                "notify_userstory_create": letschathook.notify_userstory_create,
                "notify_userstory_change": letschathook.notify_userstory_change,
                "notify_userstory_delete": letschathook.notify_userstory_delete,
                "notify_task_create": letschathook.notify_task_create,
                "notify_task_change": letschathook.notify_task_change,
                "notify_task_delete": letschathook.notify_task_delete,
                "notify_issue_create": letschathook.notify_issue_create,
                "notify_issue_change": letschathook.notify_issue_change,
                "notify_issue_delete": letschathook.notify_issue_delete,
                "notify_wikipage_create": letschathook.notify_wikipage_create,
                "notify_wikipage_change": letschathook.notify_wikipage_change,
                "notify_wikipage_delete": letschathook.notify_wikipage_delete
            }
        })
    return letschathooks


def on_new_history_entry(sender, instance, created, **kwargs):
    if instance.is_hidden:
        return None

    model = history_service.get_model_from_key(instance.key)
    pk = history_service.get_pk_from_key(instance.key)
    obj = model.objects.get(pk=pk)

    letschathooks = _get_project_letschathooks(obj.project)

    if instance.type == HistoryType.create:
        task = tasks.create_letschathook
        extra_args = []
    elif instance.type == HistoryType.change:
        task = tasks.change_letschathook
        extra_args = [instance]
    elif instance.type == HistoryType.delete:
        task = tasks.delete_letschathook
        extra_args = []

    for letschathook in letschathooks:
        args = [
            letschathook["url"], letschathook["token"],
            letschathook["notify_config"], obj
        ] + extra_args

        if settings.CELERY_ENABLED:
            task.delay(*args)
        else:
            task(*args)
