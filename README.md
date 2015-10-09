Taiga Contrib Let's Chat
========================

Taiga plugin for Let's Chat (https://sdelements.github.io/lets-chat/) integration.

> **NOTE 2: Let's Chat team is working to add markdown support, please use this branch for testing: https://github.com/sdelements/lets-chat/tree/try-md**

Installation
------------

#### Taiga Back

In your Taiga back python virtualenv install the pip package `taiga-contrib-letschat` with:

```bash
  pip install taiga-contrib-letschat
```

Then modify your settings/local.py and include the line:

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
  wget "https://raw.githubusercontent.com/taigaio/taiga-contrib-letschat/$(pip show taiga-contrib-letschat | awk '/^Version: /{print $2}')/front/dist/letschat.js"
```

Include in your dist/js/conf.json in the contribPlugins list the value `"/js/letschat.js"`:

```json
...
    "contribPlugins": ["/js/letschat.js"]
...
```
