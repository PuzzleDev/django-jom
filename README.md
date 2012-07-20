# django-jom

django-jom (Django Javascript Object Model) is a Django based library to extract Javascript objects from data models.

# The base idea

django-jom is a Django/Javascript implementation of the [SSMVC pattern](wiki/The-SSMVC-pattern). Interactive, rich and mobile web applications are based on the MVC pattern in which models contains the data on which the application is built. However mobile and Javascript clients are forced to replicate the MVC pattern in order to operate. The SSMVC pattern avoid code duplication by automatically extracting and synchronizing the front-end models with back-end.

# How to add django-jom to your django project

First [download and install](wiki/Installing-django-jom) django-jom as you would do for any other git-hosted django app.

Then create a [jom descriptor](wiki/Creating-a-JomDescriptor) for each model that you would like to export and run [export_jom](wiki/Exporting-Jom-files) to generate the javascript code.

The jom generation path can be configured by adding [JOM_ROOT](wiki/Configure-the-javascript-export-path) to your settings file.

# How to contribute

Please feel free to improve django-jom and submit a pull request.

# Related information

django-jom is developed and maintained by [PuzzleDev](www.puzzledev.com).

django-jom is based on the SSMVC pattern which was originally designed by Michele Sama (@msama) and Franco Raimondi.