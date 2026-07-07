[app]

# (str) Title of your application
title = Square Game

# (str) Package name
package.name = squaregame

# (str) Package domain (needed for android/ios packaging)
package.domain = org.example

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (list) List of inclusions using pattern matching
# source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
# source.exclude_exts = spec

# (list) List of directory names to not search for recursive includes
# source.exclude_patterns = 

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy

# (str) Custom source folders for requirements
# requirements.source = 

# (list) Garden requirements
# garden_requirements =

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait, sensorPortrait or default)
orientation = sensor

# (bool) Indicates if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

# (bool) Indicates if the application should be hidden or not
# android.hide = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25c

# (bool) Use --debug buildozer command to build in debug mode
android.debug = 1

# (list) Android AAR archives to add (takes precedence over local JARs)
# android.add_aars =

# (list) Gradle dependencies to add
# android.gradle_dependencies =

# (bool) Enable or disable gradle dependency resolution
# android.gradle_depends =

# (str) Path to a custom AndroidManifest.xml
# android.manifest =

# (str) Path to a custom toolchain recipe
# android.toolchain =

# (list) Java source files to add
# android.add_src =

# (list) Python source files to add
# android.add_py =

# (list) Java classes to add as a jar
# android.add_jar =

# (list) Python source files to add as a jar
# android.add_py_jar =

# (list) Java classes to add as a directory
# android.add_dir =

# (list) Python source files to add as a directory
# android.add_py_dir =

# (list) Android assets to add
# android.add_assets =

# (str) Activity class to use
# android.activity_class_name = org.kivy.android.PythonActivity

# (str) Android theme
# android.theme = @android:style/Theme.NoTitleBar

# (list) Supported CPU architectures
# android.arch = armeabi-v7a,arm64-v8a

# (bool) Whether to enable AndroidX
# android.enable_androidx = True

# (bool) Whether to add a meta-data to set the OpenGL ES version
# android.gles_version = 3

# (str) Android package name to use
# android.package_name =

# (str) Android private storage path
# android.private_storage =

# (str) Android logcat filters
# android.logcat_filters = *:S python:D

# (str) Android logcat tags to exclude
# android.logcat_exclude_tags =

# (bool) Use a custom activity
# android.use_custom_activity =

# (str) Custom activity to use
# android.custom_activity = 

# (list) Android services to add
# android.services =

# (list) Android services to add as a service
# android.add_service =

# (list) Android receivers to add
# android.receivers =

# (list) Android providers to add
# android.providers =

# (list) Android permissions
# android.permissions =

# (list) Android features
# android.features =

# (bool) Use a custom AndroidManifest.xml
# android.manifest =

# (list) Android meta-data
# android.meta_data =

# (list) Android library to add
# android.add_library =

#
# iOS specific
#

# (str) Path to a custom .plist file
# ios.plist =

# (str) Path to a custom .entitlements file
# ios.entitlements =

# (str) Path to a custom .mobileprovision file
# ios.mobileprovision =

# (bool) Use Xcode 8
# ios.use_xcode8 = False

# (str) iOS framework to add
# ios.framework =

# (str) iOS library to add
# ios.lib =

# (list) iOS frameworks to add
# ios.frameworks =

# (list) iOS libraries to add
# ios.libs =

# (list) iOS plist items
# ios.plist_items =

# (list) iOS bundle resources
# ios.bundle_resources =

# (list) iOS extra frameworks
# ios.extra_frameworks =

# (list) iOS extra libraries
# ios.extra_libs =

# (list) iOS extra sources
# ios.extra_sources =

# (list) iOS extra pkg-config
# ios.extra_pkg_config =

#
# Windows specific
#

# (bool) Use Pygame or Pygame_SDL2
# windows.python_requires =

# (list) Windows requirements
# windows.requirements =

# (str) Windows architecture
# windows.arch =

# (str) Windows version
# windows.version =

# (str) Windows publisher
# windows.publisher =

# (str) Windows display name
# windows.display_name =

#
# macOS specific
#

# (list) macOS requirements
# macos.requirements =

# (str) macOS architecture
# macos.arch =

# (str) macOS version
# macos.version =

# (str) macOS publisher
# macos.publisher =

# (str) macOS display name
# macos.display_name =

#
# Linux specific
#

# (list) Linux requirements
# linux.requirements =

# (str) Linux architecture
# linux.arch =

# (str) Linux version
# linux.version =

# (str) Linux publisher
# linux.publisher =

# (str) Linux display name
# linux.display_name =

#
# Buildozer global settings
#

# (str) Path to buildozer directory
# buildozer.dir = ~/.buildozer

# (bool) Enable or disable buildozer logging
# buildozer.log = 1

# (list) Buildozer global requirements
# buildozer.requirements =

# (str) Buildozer log level (one of info, debug, warning, error, critical)
# buildozer.log_level = info

# (bool) Enable or disable buildozer color output
# buildozer.color = 1

# (bool) Enable or disable buildozer verbose output
# buildozer.verbose = 0
