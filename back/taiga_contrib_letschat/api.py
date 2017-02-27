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

from taiga.base import filters
from taiga.base import response
from taiga.base.api import ModelCrudViewSet
from taiga.base.decorators import detail_route

from . import models
from . import serializers
from . import permissions
from . import tasks


class LetsChatHookViewSet(ModelCrudViewSet):
    model = models.LetsChatHook
    serializer_class = serializers.LetsChatHookSerializer
    permission_classes = (permissions.LetsChatHookPermission,)
    filter_backends = (filters.IsProjectAdminFilterBackend,)
    filter_fields = ("project",)

    @detail_route(methods=["POST"])
    def test(self, request, pk=None):
        letschathook = self.get_object()
        self.check_permissions(request, 'test', letschathook)

        tasks.test_letschathook(letschathook.url, letschathook.token)

        return response.NoContent()
