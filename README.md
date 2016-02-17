Taiga Contrib Let's Chat
========================

Taiga plugin for Let's Chat (https://sdelements.github.io/lets-chat/) integration.

> **NOTE: Let's Chat team is working to add markdown support, please use this branch for testing: https://github.com/sdelements/lets-chat/tree/try-md**

Installation
------------
### Production env

#### Taiga Back

In your Taiga back python virtualenv install the pip package `taiga-contrib-letschat` with:

```bash
  pip install taiga-contrib-letschat
```

Then modify 'taiga-back/settings/local.py' and include the line:

```python
  INSTALLED_APPS += ["taiga_contrib_letschat"]
```

Then run the migrations to generate the new need table:

```bash
  python manage.py migrate taiga_contrib_letschat
```

#### Taiga Front

Download in your `dist/plugins/` directory of Taiga front the `taiga-contrib-letschat` compiled code (you need subversion in your system):

```bash
  cd dist/
  mkdir -p plugins
  cd plugins
  svn export "https://github.com/taigaio/taiga-contrib-letschat/tags/$(pip show taiga-contrib-letschat | awk '/^Version: /{print $2}')/front/dist" "letschat"
```

Include in your 'dist/conf.json' in the 'contribPlugins' list the value `"/plugins/letschat/letschat.json"`:

```json
...
    "contribPlugins": [
        (...)
        "/plugins/letschat/letschat.json"
    ]
...
```

### Dev env

#### Taiga Back

Clone the repo and

```bash
  cd taiga-contrib-letschat/back
  workon taiga
  pip install -e .
```

Then modify 'taiga-back/settings/local.py' and include the line:

```python
  INSTALLED_APPS += ["taiga_contrib_letschat"]
```

Then run the migrations to generate the new need table:

```bash
  python manage.py migrate taiga_contrib_letschat
```

#### Taiga Front

```bash
  npm install
  gulp
```

Link `dist` in `taiga-front` plugins directory:

```bash
  cd taiga-front/dist
  mkdir -p plugins
  cd plugins
  ln -s ../../../taiga-contrib-letschat/dist letschat
```

Include in your 'dist/conf.json' in the 'contribPlugins' list the value `"/plugins/letschat/letschat.json"`:

```json
...
    "contribPlugins": [
        (...)
        "/plugins/letschat/letschat.json"
    ]
...
```

If you only want to build `dist` use:

```bash
  npm install
  gulp build
```
