# ClearCut Android

ClearCut is an early Android app prototype for photo and video workflows. This milestone includes a Compose interface, Android Photo Picker selection, video preview, project history, and exporting an unchanged copy through Android's system document picker. The original media is not modified.

The editor screen also includes workflow presets for object removal, background cleanup, and audio extraction, along with a precision slider that helps shape the future pipeline without pretending the AI editing is active yet. Object removal, background removal, video processing, audio conversion, downloads, project history, billing, and ads are not implemented yet. The interface labels planned tools as upcoming rather than presenting simulated processing.

## Open and run

Open this `android` directory in Android Studio. Use JDK 17 and install Android SDK Platform 35 when prompted. Let Gradle sync, then run the `app` configuration on an Android 8.0 (API 26) or newer device or emulator.

The project uses Kotlin, Jetpack Compose, Media3, and Coil. The selected media is accessed through Android's system picker; no broad media-library permission is requested. Export uses Android's system document picker.
