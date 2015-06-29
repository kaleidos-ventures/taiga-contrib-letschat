Taiga Contrib Let's Chat
========================

Taiga plugin for Let's Chat (https://sdelements.github.io/lets-chat/) integration.

> **NOTE: This plugin is currently in alpha version**  
> **NOTE 2: Let's Chat team is working to add markdown support, please use this branch for testing: https://github.com/sdelements/lets-chat/tree/try-md**

Installation
------------

#### Taiga Back

In your Taiga back python virtualenv install taiga_contrib_letschat app:

```bash
  git clone https://github.com/taigaio/taiga-contrib-letschat.git
  cd taiga-contrib-letschat/back
  python setup.py install
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
  wget "https://raw.githubusercontent.com/taigaio/taiga-contrib-letschat/master/front/dist/letschat.js"
```

Include in your dist/js/conf.json in the contribPlugins list the value `"/js/letschat.js"`:

```json
...
    "contribPlugins": ["/js/letschat.js"]
...
```
