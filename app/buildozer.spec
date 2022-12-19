[app]

title = Cello Nora
author = Elad Ernst
version = 0.1
package.name = cellonora
package.domain = github.com/kazabubu21/cello_nora

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

requirements = python3,kivy,time,requests

orientation = portrait
fullscreen = 1
android.arch = armeabi-v7a

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

[buildozer]
log_level = 2