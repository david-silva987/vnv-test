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
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_DEV_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

4. Pour l'utilisation des *messages* de Django, il faut juste la configuration suivante:

```python
# Messages
# https://docs.djangoproject.com/en/5.0/ref/contrib/messages/
from django.contrib import messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_TAGS = {
    messages.DEBUG: 'light',
    messages.ERROR: 'danger',
}
```

5. Et finalement, il faut donner un nom à l'application et un fichier pour le numéro de version. Créez un fichier nommé `version.txt` à la racine du projet et le code suivant dans le `settings.py`:

```python
# App information

APP_NAME = 'VNV-TEST'
from datetime import datetime
COPY_YEAR = datetime.now().year

with open(os.path.join(BASE_DIR, 'version.txt'), 'r') as version_file:
    APP_VERSION = version_file.read()
```

## 3. Première app _base_

Nous pouvons à présent créer la première application du projet. Par défaut, celle-ci s'appelera `base`.

```python
django-admin startapp base
```

Un nouveau dossier **base** a été crée dans votre dossier. Ce dossier contiendra les informations les plus généralisés possible (par exemple les classes Mère réutilisable dans les autres applications), ou encore les différents templates globaux.

Il faut enregistrer cette app dans le `settings.py` dans le tableau **INSTALLED_APPS** et aussi ajouter les routes dans le urls.py dans `config`.

Dans **INSTALLED_APPS**:

```py
INSTALLED_APPS = [
    ...
    'base',
    'pcore',
    'pauth',
    'django.contrib.admin',
]
```

Et dans le *urls.py*:

```python
urlpatterns= [
    path('', include('base.urls')),
    ...
]
```

**Note**: Avec la commande *startapp*, le fichier `urls.py` de l'application créée ne se crée pas automatiquement.

Le fichiers `views.py` devrait ressembler à ceci dans un premier temps:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse

from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views import generic

def index(request):
    return HttpResponseRedirect(reverse('base:home'))

class HomePageView(generic.TemplateView):
    '''
    Home page view, still to be defined the content inside
    '''
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
```

Le fichier `urls.py` doit être completé afin d'utiliser les différentes vues:

```python
from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.HomePageView.as_view(), name='home'),
]
```

**Note**: cette configuration a été inspirée par rapport à mon utilisation personnelle lors de l'initialisation d'un projet.

# 4. Dossier static

Le dossier `static`contiendra toutes les images, fichiers au format .css et .js et autres

Ce dossier est créé manuellement avec un clic droit -> Nouveau dossier -> static.

A l'intérieur de celui-ci, nous allons créer les dossiers suivants : **js, css, images, fonts, webfonts**:

a) le dossier **js** contient tous les fichiers JavaScript nécessaires pour les applications. Par défaut nous utilisons des fichiers pour bootstrap, fontawesome, cookies et jquery

b) le dossier **css** contient toutes les feuilles de style. Par défaut nous avons un fichier global pour l'application nommé `nom_app.css` et ensuite nous avons des fichiers pour bootstrap, les cookies, jquery, fontawesome

c) le dossier **images** contient toutes les images utilisées dans l'application

d) les dossiers **font** et **webfonts** contiennent les polices d'écriture pour le site.

**Note**: cette configuration a été inspirée par rapport à mon utilisation personnelle lors de l'initialisation d'un projet.

# 5. Lancement de l'application

Avant de lancer le serveur pour la première fois, il faut lancer les migrations, créer un premier superutilisateur et lancer le serveur:

```python
py manage.py migrate
py manage.py createsuperuser
py manage.py compilemessages
py manage.py runserver
```

# 6. API Django

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

# 7. Application Note

Il faut créer l'application _note_ avec la commande suivante:

```python
django-admin startapp note
```

**Note**: n'oubliez pas d'enregistrer l'application dans les **INSTALLED_APPS** et dans le fichier _urls.py_ de l'app _config_

## 7.1 Models

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

## 7.2 Serializers

Afin de pouvoir communiquer avec l'API, nous allons devoir utiliser des _Serializers_, qui permettra de convertir le modèle _Note_ dans du _json_.

Pour cela il faut créer un fichier _serializers.py_ dans l'application _note_ et y mettre le code suivant:

```python
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('title', 'content', 'updated_at')
```

**Note**: le champ _created_at est ignoré ici et c'est bien voulu étant donné la propriété _auto_add_now définie dans le model. Cette propriété fera en sorte qu'à la création d'un objet Note, la date actuelle sera prise en compte. Cependant, on doit mettre updated_at pour que celle-ci se mette à jour lors de manipulations (notamment lors des mises à jour)

# 7.3 Views

Une fois le modèle et le serializer créé, on peut créer la vue qui va nous permettre d'intéragir avec l'API. Etant donné que nous sommes dans un cas standard, nous allons profiter de la puissance de DRF et utiliser les ModelViewSet, qui contient la logique déjà implémentée pour les CRUD.

```python
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
```

**Note**: les imports ne sont pas pris en compte dans les différents bouts de code intégrés dans la documentation.

## 7.4 Routes

Tout à la fin, nous pouvons nous attaquer aux routes avec un seul endpoint. Pour cela, dans le fichier _urls.py_:

```python
router = DefaultRouter()
router.register(r'notes', views.NoteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

## 7.5 Comment lancer les requêtes

Un fichier **examples.sh** se situe à l'intérieur de l'app _note_ qui contient les différentes requêtes CURL avec quelques exemples d'utilisation.

**Note**: pour pouvoir tester en local, il vous faudra lancer le serveur en 127.0.0.1:8000 avec un `python manage.py runserver` et ensuite ouvrir un nouveau terminal et copier les différentes requêtes CURL présentes dans le fichier **examples.sh**

## 7.6 Tests unitaires

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