# README for this test

# Documentation

## 1. Créer depôt Github

Se connecter sur github.com avec compte personnel et créer le repo

## 2. Initialiser le projet

Créer un nouveau `venv` en Python **3.11**, puis installer `Django`, `django_simple_captcha`et `wheel`.

```python
pip install 'Django' wheel
```

**Note**: n'oubliez pas de _freeze_ vos dépendances via un `pip freeze > requirements.txt`

Initialiser le projet avec la commande *django-admin startproject*

**Note:** on choisira *config* pour cette première étape

```python
django-admin startproject config .
# le point veut dire que nous voulons installer directement dans ce repertoire
```

Un certain nombre de paramètres sont déjà renseignés dans le fichiers `settings.py`. Il faut en rajouter d'autres comme :

1. Accès au `local_settings.py.` Ce fichier sera créé **exclusivement** sur le serveur et permettra de renseigner plus d'informations confidentielles. A remplir en toute fin du fichier

```python
# Allow override of these settings by a local_settings.py file
try:
    from .local_settings import *
except ImportError:
    pass
```

2. Le chemin d'accès pour les STATIC est configuré, il faut cependant en fournir d'autres pour ne pas avoir de problèmes en dev et en prod (ainsi que les media).

```python
STATICFILES_DIRS = (
   BASE_DIR / 'static', # all generic static files are in /static
)
STATIC_DEV_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

3. Et finalement, il faut donner un nom à l'application et un fichier pour le numéro de version. Créez un fichier nommé `version.txt` à la racine du projet et le code suivant dans le `settings.py`:

```python
# App information

APP_NAME = 'VNV-TEST'
from datetime import datetime
COPY_YEAR = datetime.now().year

with open(os.path.join(BASE_DIR, 'version.txt'), 'r') as version_file:
    APP_VERSION = version_file.read()
```

# 3. Lancement de l'application

Avant de lancer le serveur pour la première fois, il faut lancer les migrations, créer un premier superutilisateur et lancer le serveur:

```python
py manage.py migrate
py manage.py createsuperuser
py manage.py compilemessages
py manage.py runserver
```

# 4. API Django

Pour pouvoir utiliser la librairie permettant de manipuler des librairies, il faut installer `djangorestframework`:

```python
pip install djangorestframework
```

**Note**: n'oubliez pas de *freeze* vos dépendances via un `pip freeze > requirements.txt`

Ensuite il faut ajouter `rest_framework`à vos `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

# 5. Application Note

Il faut créer l'application _note_ avec la commande suivante:

```python
django-admin startapp note
```

**Note**: n'oubliez pas d'enregistrer l'application dans les **INSTALLED_APPS** et dans le fichier _urls.py_ de l'app _config_

## 5.1 Models

Une fois la première configuration faite, nous pouvons désormais créer notre modèle, pour cela j'ai utilisé le modèle fourni dans la donné que je copie ici:

```python
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

On peut désormais créer la migration et l'appliquer avec les deux commandes suivantes:

```python
python manage.py makemigrations
python manage.py createsuperuser
```

A ce stade, la base de données contient la table Note.

## 5.2 Serializers

Afin de pouvoir communiquer avec l'API, nous allons devoir utiliser des _Serializers_, qui permettra de convertir le modèle _Note_ dans du _json_.

Pour cela il faut créer un fichier _serializers.py_ dans l'application _note_ et y mettre le code suivant:

```python
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('title', 'content', 'updated_at')
```

**Note**: le champ _created_at est ignoré ici et c'est bien voulu étant donné la propriété _auto_add_now définie dans le model. Cette propriété fera en sorte qu'à la création d'un objet Note, la date actuelle sera prise en compte. Cependant, on doit mettre updated_at pour que celle-ci se mette à jour lors de manipulations (notamment lors des mises à jour)

## 5.3 Views

Une fois le modèle et le serializer créé, on peut créer la vue qui va nous permettre d'intéragir avec l'API. Etant donné que nous sommes dans un cas standard, nous allons profiter de la puissance de DRF et utiliser les ModelViewSet, qui contient la logique déjà implémentée pour les CRUD.

```python
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
```

**Note**: les imports ne sont pas pris en compte dans les différents bouts de code intégrés dans la documentation.

## 5.4 Routes

Tout à la fin, nous pouvons nous attaquer aux routes avec un seul endpoint. Pour cela, dans le fichier _urls.py_:

```python
router = DefaultRouter()
router.register(r'notes', views.NoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

## 5.5 Comment lancer les requêtes

Un fichier **examples.sh** se situe à l'intérieur de l'app _note_ qui contient les différentes requêtes CURL avec quelques exemples d'utilisation.

**Note**: pour pouvoir tester en local, il vous faudra lancer le serveur en 127.0.0.1:8000 avec un `python manage.py runserver` et ensuite ouvrir un nouveau terminal et copier les différentes requêtes CURL présentes dans le fichier **examples.sh**

## 5.6 Tests unitaires

Nous allons profiter du fait que l'application _note_ contient déjà un module _tests.py_ pour y insérer nos tests unitaires.

Quelques remarques:

- Nous créons un premier jeu de données avec la méthode _setUp()_ 

- 4 tests unitaires ont été créés:
  
  - Compter le nombre de Notes
  
  - Vérifier mise à jour d'une note
  
  - Vérifier suppresion d'une Note
  
  - Vérifier mise à jour du champ update_at

Pour lancer les tests unitaires, il suffit de lancer la commande:

```python
python manage.py test note
```