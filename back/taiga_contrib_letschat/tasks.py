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

import requests
import logging

from django.conf import settings
from django.template import loader, Context

from taiga.base.api.renderers import UnicodeJSONRenderer
from taiga.base.utils.db import get_typename_for_model_instance
from taiga.celery import app

logger = logging.getLogger(__name__)


def _get_type(obj):
    content_type = get_typename_for_model_instance(obj)
    return content_type.split(".")[1]


def _send_request(url, token, data):
    serialized_data = UnicodeJSONRenderer().render(data)
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-type': 'application/json',
    }
    if settings.CELERY_ENABLED:
        requests.post(url, data=serialized_data, headers=headers)
        return
    try:
        requests.post(url, data=serialized_data, headers=headers)
    except Exception:
        logger.error("Error sending request to LetsChat")


def _markdown_field_to_attachment(template_field, field_name, values):
    context = Context({"field_name": field_name, "values": values})
    change_field_text = template_field.render(context.flatten())

    return change_field_text.strip()


def _field_to_attachment(template_field, field_name, values):
    context = Context({"field_name": field_name, "values": values})
    change_field_text = template_field.render(context.flatten())

    return change_field_text.strip()

def _check_notify_permission(notify_config, obj_type, action):
    return notify_config.get('notify_{0}_{1}'.format(obj_type, action), False)


@app.task
def change_letschathook(url, token, notify_config, obj, change):
    obj_type = _get_type(obj)

    if not _check_notify_permission(notify_config, obj_type, 'change'):
        return

    template_change = loader.get_template('taiga_contrib_letschat/change.jinja')
    context = Context({"obj": obj, "obj_type": obj_type, "change": change})

    change_text = template_change.render(context.flatten())
    data = {"text": change_text.strip()}

    # Get markdown fields
    if change.diff:
        template_field = loader.get_template('taiga_contrib_letschat/field-diff.jinja')
        included_fields = ["description", "content", "blocked_note"]

        for field_name, values in change.diff.items():
            if field_name in included_fields:
                attachment = _markdown_field_to_attachment(template_field, field_name, values)

                data["text"] += '\n' + attachment

    # Get rest of fields
    if change.values_diff:
        template_field = loader.get_template('taiga_contrib_letschat/field-diff.jinja')
        excluded_fields = ["description_diff", "description_html", "content_diff",
                           "content_html", "blocked_note_diff", "blocked_note_html",
                           "backlog_order", "kanban_order", "taskboard_order", "us_order",
                           "finish_date", "is_closed"]

        for field_name, values in change.values_diff.items():
            if field_name in excluded_fields:
                continue

            attachment = _field_to_attachment(template_field, field_name, values)

            if attachment:
                data["text"] += '\n' + attachment

    _send_request(url, token, data)


@app.task
def create_letschathook(url, token, notify_config, obj):
    obj_type = _get_type(obj)

    if not _check_notify_permission(notify_config, obj_type, 'create'):
        return

    template = loader.get_template('taiga_contrib_letschat/create.jinja')
    context = Context({"obj": obj, "obj_type": obj_type})

    data = {
        "text": template.render(context.flatten()),
    }
    _send_request(url, token, data)


@app.task
def delete_letschathook(url, token, notify_config, obj):
    obj_type = _get_type(obj)

    if not _check_notify_permission(notify_config, obj_type, 'delete'):
        return

    template = loader.get_template('taiga_contrib_letschat/delete.jinja')
    context = Context({"obj": obj, "obj_type": obj_type})

    data = {
        "text": template.render(context.flatten()),
    }

    _send_request(url, token, data)


@app.task
def test_letschathook(url, token):
    data = {
        "text": "**Test:** *LetsChat* message",
    }

    _send_request(url, token, data)
