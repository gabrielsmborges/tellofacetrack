# TelloFaceTrack

[Site Web](https://axeldebat.github.io/Tello-Face-Track/)

**Ce programme à été conçu en Python 3.7, le code n'est pas compatible avec la version 3.8 de Python.**
 Ceci est le projet des élèves [Gabriel Borges](https://github.com/gabrielsmborges), [Axel Debat](https://github.com/axeldebat) et [Paul Landa](https://github.com/padvan) de la classe d'ISN de 2019/20 du Lycée Marceau à Chartres

## But
Notre but est d'apporter un système de reconnaissance faciale au DJI Tello. Notre programme est codé en Python. Nous recommendons d'utiliser Python 3.6 ou supérieur pour éviter toute sorte de bug informatique.

## Configuration

```diff
- Python 3.7 requis
```
Afin que le programme fonctionne sur votre machine veuillez éxécuter le fichier [_setup.py_](setup.py)

Terminal:
```
python setup.py
```
&nbsp;&nbsp;
_Cela risque de prendre plusieurs minutes._

#### ou
Méthode alternative

Terminal: 
```
pip install -r requirements.txt
```
&nbsp;&nbsp;
_Cela risque de prendre plusieurs minutes._


## Exécuter

**Veuillez vous assurer que votre machine est connectée au réseau WiFi du Drone.**

Une fois votre machine configurée vous pouvez exécuter le fichier [main.py](main.py)

Terminal:
```
python main.py
```
Si vous n'avez pas un DJI Tello, vous pouvez tester la reconnaissance faciale avec le fichier [exemplewebcam.py](exemplewebcam.py)

Terminal:
```
python exemplewebcam.py
```
