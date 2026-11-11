package com.clearcut.app.data

import android.content.ContentResolver
import android.net.Uri
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.IOException

suspend fun copyMedia(
    contentResolver: ContentResolver,
    source: Uri,
    destination: Uri,
) = withContext(Dispatchers.IO) {
    try {
        val input = contentResolver.openInputStream(source)
            ?: throw IOException("The selected media could not be opened.")
        input.use { sourceStream ->
            val output = contentResolver.openOutputStream(destination, "w")
                ?: throw IOException("The destination could not be opened.")
            output.use { destinationStream ->
                sourceStream.copyTo(destinationStream)
            }
        }
    } catch (error: IOException) {
        contentResolver.delete(destination, null, null)
        throw error
    } catch (error: SecurityException) {
        contentResolver.delete(destination, null, null)
        throw error
    }
}
