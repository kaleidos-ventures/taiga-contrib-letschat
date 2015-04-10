Taiga Contrib Let's Chat
========================

Taiga plugin for Let's Chat (https://sdelements.github.io/lets-chat/) integration.

> **NOTE: This plugin is currently in alpha version**

Installation
------------

#### Taiga Back

In your Taiga back python virtualenv install back/taiga_contrib_letschat app, then modify your settings/local.py and include the line:

```python
  INSTALLED_APPS += ["taiga_contrib_letschat"]
```

Then run the migrations to generate the new need table:

```bash
  python manage.py migrate taiga_contrib_letschat
```

#### Taiga Front

Download in your `dist/js/` directory of Taiga front the `taiga-contrib-letschat` compiled code:

```bash
  cd dist/js
  wget "https://raw.githubusercontent.com/taigaio/taiga-contrib-letschat/master/front/dist/letschat.js"
```

Include in your dist/js/conf.json in the contribPlugins list the value `"/js/letschat.js"`:

```json
...
    "contribPlugins": ["/js/letschat.js"]
...
```
