package com.clearcut.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val Ink = Color(0xFF10111A)
private val Panel = Color(0xFF191B28)
private val Violet = Color(0xFF9B8CFF)
private val Mint = Color(0xFF72E6C1)
private val LightBackground = Color(0xFFF6F5FB)
private val LightSurface = Color(0xFFFFFFFF)
private val DeepIndigo = Color(0xFF5146B8)

private val DarkColors = darkColorScheme(
    primary = Violet,
    onPrimary = Ink,
    secondary = Mint,
    background = Ink,
    surface = Panel,
    onBackground = Color(0xFFF3F1FF),
    onSurface = Color(0xFFF3F1FF),
)

private val LightColors = lightColorScheme(
    primary = DeepIndigo,
    onPrimary = Color.White,
    secondary = Color(0xFF087E66),
    background = LightBackground,
    surface = LightSurface,
    onBackground = Color(0xFF191827),
    onSurface = Color(0xFF191827),
)

@Composable
fun ClearCutTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit,
) {
    MaterialTheme(
        colorScheme = if (darkTheme) DarkColors else LightColors,
        content = content,
    )
}
