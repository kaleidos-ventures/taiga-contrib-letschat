
#curl -X POST -d "{\"text\" : \"eclisse.jpg\"}" -H "Content-Type: application/json"
#-H "Authorization: Bearer NTRlYWZjNjUzYjgyNjNkMmNiNWE0OGIwOjM1NmVhMDNiZGQzYmVmY2NiMDE2OGY5NjQyNGFjNThkNzgzNGU2ODQzNWMzZDA3Zg=="
#http://localhost:5000/rooms/dev/messages


@.taigaContribPlugins = @.taigaContribPlugins or []

letsChatInfo = {
    slug: "letschat"
    name: "LetsChat"
    type: "admin"
    module: 'taigaContrib.letschat'
}

@.taigaContribPlugins.push(letsChatInfo)

module = angular.module('taigaContrib.letschat', [])

debounce = (wait, func) ->
    return _.debounce(func, wait, {leading: true, trailing: false})

initLetsChatPlugin = ($tgUrls) ->
    $tgUrls.update({
        "letschat": "/letschat"
    })

class LetsChatAdmin
    @.$inject = [
        "$rootScope",
        "$scope",
        "$tgRepo",
        "$appTitle",
        "$tgConfirm",
        "$tgHttp",
    ]

    constructor: (@rootScope, @scope, @repo, @appTitle, @confirm, @http) ->
        @scope.sectionName = "LetsChat" #i18n
        @scope.sectionSlug = "letschat" #i18n

        @scope.$on "project:loaded", =>
            promise = @repo.queryMany("letschat", {project: @scope.projectId})

            promise.then (letschathooks) =>
                @scope.letschathook = {project: @scope.projectId}
                if letschathooks.length > 0
                    @scope.letschathook = letschathooks[0]
                @appTitle.set("LetsChat - " + @scope.project.name)

            promise.then null, =>
                @confirm.notify("error")

    testHook: () ->
        promise = @http.post(@repo.resolveUrlForModel(@scope.letschathook) + '/test')
        promise.success (_data, _status) =>
            @confirm.notify("success")
        promise.error (data, status) =>
            @confirm.notify("error")

module.controller("ContribLetsChatAdminController", LetsChatAdmin)

LetsChatWebhooksDirective = ($repo, $confirm, $loading) ->
    link = ($scope, $el, $attrs) ->
        form = $el.find("form").checksley({"onlyOneErrorElement": true})
        submit = debounce 2000, (event) =>
            event.preventDefault()

            return if not form.validate()

            $loading.start(submitButton)

            if not $scope.letschathook.id
                promise = $repo.create("letschat", $scope.letschathook)
                promise.then (data) ->
                    $scope.letschathook = data
            else if $scope.letschathook.url
                promise = $repo.save($scope.letschathook)
                promise.then (data) ->
                    $scope.letschathook = data
            else
                promise = $repo.remove($scope.letschathook)
                promise.then (data) ->
                    $scope.letschathook = {project: $scope.projectId}

            promise.then (data)->
                $loading.finish(submitButton)
                $confirm.notify("success")

            promise.then null, (data) ->
                $loading.finish(submitButton)
                form.setErrors(data)
                if data._error_message
                    $confirm.notify("error", data._error_message)

        submitButton = $el.find(".submit-button")

        $el.on "submit", "form", submit
        $el.on "click", ".submit-button", submit

    return {link:link}

module.directive("contribLetschatWebhooks", ["$tgRepo", "$tgConfirm", "$tgLoading", LetsChatWebhooksDirective])

module.run(["$tgUrls", initLetsChatPlugin])
