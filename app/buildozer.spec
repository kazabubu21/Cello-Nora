[app]

title = Cello Nora
author = Elad Ernst
version = 0.1
package.name = cellonora
package.domain = org.cello_nora

source.dir = .
source.include_exts = py

requirements = python3,kivy,urllib3,requests,chardet, certifi, idna

orientation = portrait
fullscreen = 1
android.arch = armeabi-v7a

android.permissions = INTERNET



[buildozer]
log_level = 5