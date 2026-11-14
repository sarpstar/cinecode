package com.clearcut.app.ui

import android.content.ContentResolver
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.provider.OpenableColumns
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AutoFixHigh
import androidx.compose.material.icons.rounded.AutoAwesome
import androidx.compose.material.icons.rounded.Collections
import androidx.compose.material.icons.rounded.Download
import androidx.compose.material.icons.rounded.Image
import androidx.compose.material.icons.rounded.Movie
import androidx.compose.material.icons.rounded.MusicNote
import androidx.compose.material.icons.rounded.Settings
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Slider
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import coil.compose.AsyncImage
import com.clearcut.app.R
import com.clearcut.app.data.ProjectDatabase
import com.clearcut.app.data.ProjectEntry
import com.clearcut.app.data.copyMedia
import com.clearcut.app.ui.common.ProjectCard
import com.clearcut.app.ui.theme.ClearCutTheme
import kotlinx.coroutines.launch
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

private enum class AppTab {
    Home,
    Tools,
    Projects,
    Settings,
}

@Composable
fun ClearCutApp() {
    var selectedTab by rememberSaveable { mutableStateOf(AppTab.Home) }
    var selectedMedia by rememberSaveable { mutableStateOf<Uri?>(null) }
    var selectedProject by rememberSaveable { mutableStateOf<ProjectEntry?>(null) }
    var darkTheme by rememberSaveable { mutableStateOf(false) }
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val db = remember { ProjectDatabase.getInstance(context) }
    val recentProjects by db.projectDao().observeRecent().collectAsState(initial = emptyList())
    val picker = rememberLauncherForActivityResult(
        ActivityResultContracts.PickVisualMedia(),
    ) { uri ->
        if (uri != null) {
            context.contentResolver.takePersistableUriPermission(
                uri,
                Intent.FLAG_GRANT_READ_URI_PERMISSION,
            )
            scope.launch {
                db.projectDao().insert(
                    ProjectEntry(
                        title = suggestProjectTitle(context, uri),
                        uri = uri.toString(),
                        mimeType = context.contentResolver.getType(uri),
                        createdAt = System.currentTimeMillis(),
                    ),
                )
            }
            selectedMedia = uri
        }
    }

    ClearCutTheme(darkTheme = darkTheme) {
        if (selectedMedia != null) {
            MediaEditor(
                uri = selectedMedia!!,
                onBack = { selectedMedia = null },
            )
        } else {
            ClearCutRoot(
                selectedTab = selectedTab,
                darkTheme = darkTheme,
                onTabSelected = { selectedTab = it },
                onThemeChanged = { darkTheme = it },
                recentProjects = recentProjects,
                onPickMedia = {
                    picker.launch(
                        androidx.activity.result.PickVisualMediaRequest(
                            ActivityResultContracts.PickVisualMedia.ImageAndVideo,
                        ),
                    )
                },
                onOpenProject = { entry ->
                    selectedProject = entry
                },
            )
        }
        if (selectedProject != null) {
            ProjectDetailSheet(
                entry = selectedProject!!,
                onDismiss = { selectedProject = null },
                onOpen = {
                    val uri = selectedProject?.uri?.takeIf { it.isNotBlank() }?.let(Uri::parse)
                    if (uri != null) {
                        selectedMedia = uri
                    }
                    selectedProject = null
                },
                onDelete = {
                    scope.launch {
                        db.projectDao().deleteById(selectedProject!!.id)
                    }
                    selectedProject = null
                },
            )
        }
    }
}

@Composable
private fun ClearCutRoot(
    selectedTab: AppTab,
    darkTheme: Boolean,
    onTabSelected: (AppTab) -> Unit,
    onThemeChanged: (Boolean) -> Unit,
    recentProjects: List<ProjectEntry>,
    onPickMedia: () -> Unit,
    onOpenProject: (ProjectEntry) -> Unit,
) {
    Scaffold(
        bottomBar = {
            NavigationBar {
                val tabs = listOf(
                    Triple(AppTab.Home, R.string.nav_home, Icons.Rounded.Collections),
                    Triple(AppTab.Tools, R.string.nav_tools, Icons.Rounded.AutoFixHigh),
                    Triple(AppTab.Projects, R.string.nav_projects, Icons.Rounded.Download),
                    Triple(AppTab.Settings, R.string.nav_settings, Icons.Rounded.Settings),
                )
                tabs.forEach { (tab, label, icon) ->
                    NavigationBarItem(
                        selected = selectedTab == tab,
                        onClick = { onTabSelected(tab) },
                        icon = { Icon(icon, contentDescription = null) },
                        label = { Text(stringResource(label)) },
                    )
                }
            }
        },
    ) { padding ->
        when (selectedTab) {
            AppTab.Home -> HomeScreen(
                padding = padding,
                onPickMedia = onPickMedia,
                onOpenTools = { onTabSelected(AppTab.Tools) },
                recentProjects = recentProjects,
                onOpenProject = onOpenProject,
            )
            AppTab.Tools -> ToolsScreen(
                padding = padding,
                onPickMedia = onPickMedia,
                recentProjects = recentProjects,
                onOpenProject = onOpenProject,
            )
            AppTab.Projects -> ProjectsScreen(
                padding = padding,
                recentProjects = recentProjects,
                onOpenProject = onOpenProject,
            )
            AppTab.Settings -> SettingsScreen(
                padding = padding,
                darkTheme = darkTheme,
                onThemeChanged = onThemeChanged,
            )
        }
    }
}

@Composable
private fun HomeScreen(
    padding: PaddingValues,
    onPickMedia: () -> Unit,
    onOpenTools: () -> Unit,
    recentProjects: List<ProjectEntry>,
    onOpenProject: (ProjectEntry) -> Unit,
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(padding),
        contentPadding = PaddingValues(start = 20.dp, end = 20.dp, top = 18.dp, bottom = 28.dp),
        verticalArrangement = Arrangement.spacedBy(20.dp),
    ) {
        item {
            Row(verticalAlignment = Alignment.CenterVertically) {
                BrandMark()
                Spacer(Modifier.width(12.dp))
                Column(Modifier.weight(1f)) {
                    Text(
                        stringResource(R.string.app_name),
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                    )
                    Text(
                        stringResource(R.string.home_tagline),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
                Text(
                    stringResource(R.string.pro_badge),
                    modifier = Modifier
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.14f))
                        .padding(horizontal = 14.dp, vertical = 8.dp),
                    color = MaterialTheme.colorScheme.primary,
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.Bold,
                )
            }
        }
        item {
            Card(
                shape = RoundedCornerShape(28.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primary),
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(
                            Brush.linearGradient(
                                listOf(
                                    MaterialTheme.colorScheme.primary,
                                    MaterialTheme.colorScheme.primary.copy(alpha = 0.74f),
                                    ColorAccent,
                                ),
                            ),
                        )
                        .padding(22.dp),
                    verticalArrangement = Arrangement.spacedBy(14.dp),
                ) {
                    Text(
                        stringResource(R.string.hero_eyebrow),
                        style = MaterialTheme.typography.labelLarge,
                        color = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.82f),
                    )
                    Text(
                        stringResource(R.string.hero_title),
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onPrimary,
                    )
                    Text(
                        stringResource(R.string.hero_body),
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onPrimary.copy(alpha = 0.88f),
                    )
                    Button(
                        onClick = onPickMedia,
                        colors = ButtonDefaults.buttonColors(
                            containerColor = MaterialTheme.colorScheme.surface,
                            contentColor = MaterialTheme.colorScheme.primary,
                        ),
                    ) {
                        Icon(Icons.Rounded.Image, contentDescription = null)
                        Spacer(Modifier.width(8.dp))
                        Text(stringResource(R.string.choose_media))
                    }
                }
            }
        }
        item {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    stringResource(R.string.tools_title),
                    modifier = Modifier.weight(1f),
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                )
                OutlinedButton(onClick = onOpenTools) {
                    Text(stringResource(R.string.see_all))
                }
            }
        }
        item {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                FeatureCard(
                    icon = Icons.Rounded.AutoFixHigh,
                    title = stringResource(R.string.feature_remove_title),
                    subtitle = stringResource(R.string.feature_remove_subtitle),
                )
                FeatureCard(
                    icon = Icons.Rounded.AutoAwesome,
                    title = stringResource(R.string.feature_background_title),
                    subtitle = stringResource(R.string.feature_background_subtitle),
                )
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    FeatureCard(
                        modifier = Modifier.weight(1f),
                        icon = Icons.Rounded.Movie,
                        title = stringResource(R.string.feature_video_title),
                        subtitle = stringResource(R.string.planned),
                    )
                    FeatureCard(
                        modifier = Modifier.weight(1f),
                        icon = Icons.Rounded.MusicNote,
                        title = stringResource(R.string.feature_audio_title),
                        subtitle = stringResource(R.string.planned),
                    )
                }
            }
        }
        item {
            Text(
                stringResource(R.string.projects_title),
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
            )
        }
        if (recentProjects.isNotEmpty()) {
            items(recentProjects.take(3).size) { index ->
                ProjectCard(
                    entry = recentProjects[index],
                    onClick = { onOpenProject(recentProjects[index]) },
                )
            }
        } else {
            item {
                Text(
                    stringResource(R.string.projects_empty),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
        item {
            Text(
                stringResource(R.string.mvp_notice),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun ToolsScreen(
    padding: PaddingValues,
    onPickMedia: () -> Unit,
    recentProjects: List<ProjectEntry>,
    onOpenProject: (ProjectEntry) -> Unit,
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(padding),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Text(
                stringResource(R.string.tools_title),
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
            )
        }
        item {
            Text(
                stringResource(R.string.tools_intro),
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        item {
            FeatureCard(
                icon = Icons.Rounded.AutoFixHigh,
                title = stringResource(R.string.feature_remove_title),
                subtitle = stringResource(R.string.planned),
            )
        }
        item {
            FeatureCard(
                icon = Icons.Rounded.AutoAwesome,
                title = stringResource(R.string.feature_background_title),
                subtitle = stringResource(R.string.planned),
            )
        }
        item {
            FeatureCard(
                icon = Icons.Rounded.Movie,
                title = stringResource(R.string.feature_video_title),
                subtitle = stringResource(R.string.planned),
            )
        }
        item {
            FeatureCard(
                icon = Icons.Rounded.MusicNote,
                title = stringResource(R.string.feature_audio_title),
                subtitle = stringResource(R.string.planned),
            )
        }
        item {
            Button(onClick = onPickMedia, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Rounded.Image, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text(stringResource(R.string.choose_media))
            }
        }
        if (recentProjects.isNotEmpty()) {
            item {
                Text(
                    stringResource(R.string.projects_title),
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                )
            }
            items(recentProjects.size) { index ->
                ProjectCard(
                    entry = recentProjects[index],
                    onClick = { onOpenProject(recentProjects[index]) },
                )
            }
        }
    }
}

@Composable
private fun ProjectsScreen(
    padding: PaddingValues,
    recentProjects: List<ProjectEntry>,
    onOpenProject: (ProjectEntry) -> Unit,
) {
    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(padding),
        contentPadding = PaddingValues(20.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            Text(
                stringResource(R.string.projects_title),
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
            )
        }
        if (recentProjects.isEmpty()) {
            item {
                Text(
                    stringResource(R.string.projects_empty),
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        } else {
            items(recentProjects.size) { index ->
                ProjectCard(
                    entry = recentProjects[index],
                    onClick = { onOpenProject(recentProjects[index]) },
                )
            }
        }
    }
}

@Composable
private fun SettingsScreen(
    padding: PaddingValues,
    darkTheme: Boolean,
    onThemeChanged: (Boolean) -> Unit,
) {
    Column(
        modifier = Modifier.fillMaxSize().padding(padding).padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp),
    ) {
        Text(
            stringResource(R.string.nav_settings),
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
        )
        Row(verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f)) {
                Text(stringResource(R.string.dark_mode), fontWeight = FontWeight.SemiBold)
                Text(
                    stringResource(R.string.dark_mode_hint),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Switch(checked = darkTheme, onCheckedChange = onThemeChanged)
        }
        Card(
            shape = RoundedCornerShape(18.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        ) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Export quality", fontWeight = FontWeight.SemiBold)
                Text("Balanced · 1080p preview", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        Card(
            shape = RoundedCornerShape(18.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        ) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Save location", fontWeight = FontWeight.SemiBold)
                Text("Pictures/ClearCut • Movies/ClearCut", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
        Text(
            stringResource(R.string.language_hint),
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Text(
            stringResource(R.string.settings_notice),
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}

@Composable
private fun FeatureCard(
    icon: ImageVector,
    title: String,
    subtitle: String,
    modifier: Modifier = Modifier,
) {
    Card(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(22.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Box(
                modifier = Modifier
                    .size(46.dp)
                    .clip(RoundedCornerShape(15.dp))
                    .background(MaterialTheme.colorScheme.primary.copy(alpha = 0.12f)),
                contentAlignment = Alignment.Center,
            ) {
                Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
            }
            Spacer(Modifier.width(12.dp))
            Column(Modifier.weight(1f)) {
                Text(title, style = MaterialTheme.typography.titleSmall, fontWeight = FontWeight.SemiBold)
                Spacer(Modifier.height(3.dp))
                Text(
                    subtitle,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
        }
    }
}

@Composable
private fun BrandMark() {
    Box(
        modifier = Modifier
            .size(46.dp)
            .clip(RoundedCornerShape(15.dp))
            .background(MaterialTheme.colorScheme.primary),
        contentAlignment = Alignment.Center,
    ) {
        Icon(
            Icons.Rounded.AutoFixHigh,
            contentDescription = stringResource(R.string.app_name),
            tint = MaterialTheme.colorScheme.onPrimary,
        )
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun MediaEditor(uri: Uri, onBack: () -> Unit) {
    val context = LocalContext.current
    val contentResolver = context.contentResolver
    val db = remember { ProjectDatabase.getInstance(context) }
    val mimeType = remember(uri) { contentResolver.getType(uri) }
    val isVideo = mimeType?.startsWith("video/") == true
    var saveMessage by rememberSaveable(uri.toString()) { mutableStateOf("") }
    var isSaving by rememberSaveable(uri.toString()) { mutableStateOf(false) }
    var selectedWorkflow by rememberSaveable(uri.toString()) { mutableStateOf("object") }
    var precision by rememberSaveable(uri.toString()) { mutableStateOf(78f) }
    var workflowSheet by rememberSaveable(uri.toString()) { mutableStateOf<String?>(null) }
    val workflows = listOf(
        "object" to stringResource(R.string.tool_object),
        "background" to stringResource(R.string.tool_background),
        "audio" to stringResource(R.string.tool_audio),
    )
    val selectedWorkflowText = workflows.firstOrNull { it.first == selectedWorkflow }?.second ?: workflows.first().second
    val scope = rememberCoroutineScope()
    val exportPicker = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument(mimeType ?: "application/octet-stream"),
    ) { destination ->
        if (destination != null) {
            scope.launch {
                isSaving = true
                saveMessage = context.getString(R.string.saving)
                try {
                    copyMedia(contentResolver, uri, destination)
                    db.projectDao().insert(
                        ProjectEntry(
                            title = suggestProjectTitle(context, uri),
                            uri = uri.toString(),
                            mimeType = mimeType,
                            createdAt = System.currentTimeMillis(),
                            outputPath = destination.toString(),
                        ),
                    )
                    saveMessage = context.getString(R.string.save_success)
                } catch (_: IOException) {
                    saveMessage = context.getString(R.string.save_error)
                } catch (_: SecurityException) {
                    saveMessage = context.getString(R.string.save_error)
                } finally {
                    isSaving = false
                }
            }
        }
    }

    val sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)

    if (workflowSheet != null) {
        ModalBottomSheet(
            onDismissRequest = { workflowSheet = null },
            sheetState = sheetState,
        ) {
            WorkflowDetailSheet(
                workflow = workflowSheet ?: "object",
                onSelect = {
                    selectedWorkflow = workflowSheet ?: "object"
                    workflowSheet = null
                },
            )
        }
    }

    Column(
        modifier = Modifier.fillMaxSize().padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            OutlinedButton(onClick = onBack) { Text(stringResource(R.string.back)) }
            Spacer(Modifier.width(12.dp))
            Text(
                stringResource(R.string.preview_title),
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
            )
        }
        if (isVideo) {
            VideoPreview(uri = uri, modifier = Modifier.weight(1f).fillMaxWidth())
        } else {
            AsyncImage(
                model = uri,
                contentDescription = stringResource(R.string.media_preview_description),
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(24.dp))
                    .background(MaterialTheme.colorScheme.surface),
                contentScale = ContentScale.Fit,
            )
        }

        Card(
            shape = RoundedCornerShape(20.dp),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Text(
                    stringResource(R.string.workflow_title),
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                )
                Row(
                    modifier = Modifier.horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    workflows.forEach { (key, label) ->
                        FilterChip(
                            selected = selectedWorkflow == key,
                            onClick = { selectedWorkflow = key },
                            label = { Text(label) },
                        )
                    }
                }

                Text(
                    text = when (selectedWorkflow) {
                        "object" -> stringResource(R.string.workflow_object_desc)
                        "background" -> stringResource(R.string.workflow_background_desc)
                        else -> stringResource(R.string.workflow_audio_desc)
                    },
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )

                Text(
                    text = stringResource(R.string.workflow_precision, precision.toInt()),
                    style = MaterialTheme.typography.labelLarge,
                    fontWeight = FontWeight.SemiBold,
                )
                Slider(
                    value = precision,
                    onValueChange = { precision = it },
                    valueRange = 20f..100f,
                    steps = 4,
                )
                Text(
                    text = stringResource(R.string.workflow_details, selectedWorkflowText),
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                Button(
                    onClick = { workflowSheet = selectedWorkflow },
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Text(stringResource(R.string.workflow_details_button))
                }
            }
        }

        Text(
            stringResource(R.string.preview_notice),
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        if (saveMessage.isNotEmpty()) {
            Text(saveMessage, color = MaterialTheme.colorScheme.secondary)
        }
        Button(
            onClick = { exportPicker.launch(suggestedFileName(contentResolver, uri, isVideo)) },
            enabled = !isSaving,
            modifier = Modifier.fillMaxWidth(),
        ) {
            if (isSaving) {
                CircularProgressIndicator(modifier = Modifier.size(18.dp), strokeWidth = 2.dp)
                Spacer(Modifier.width(8.dp))
            }
            Text(stringResource(R.string.save_copy))
        }
    }
}

@Composable
private fun VideoPreview(uri: Uri, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val player = remember(uri) {
        ExoPlayer.Builder(context).build().apply {
            setMediaItem(MediaItem.fromUri(uri))
            prepare()
        }
    }
    DisposableEffect(player) {
        onDispose { player.release() }
    }
    AndroidView(
        factory = { viewContext ->
            PlayerView(viewContext).apply {
                this.player = player
            }
        },
        modifier = modifier.clip(RoundedCornerShape(24.dp)),
    )
}

private fun suggestProjectTitle(context: Context, uri: Uri): String {
    val displayName = context.contentResolver.query(
        uri,
        arrayOf(OpenableColumns.DISPLAY_NAME),
        null,
        null,
        null,
    )?.use { cursor ->
        if (cursor.moveToFirst()) {
            cursor.getString(cursor.getColumnIndexOrThrow(OpenableColumns.DISPLAY_NAME))
        } else {
            null
        }
    }
    val baseName = displayName?.substringBeforeLast('.')?.takeIf { it.isNotBlank() }
        ?: "ClearCut project"
    return baseName.replace(Regex("\\s+"), " ").trim()
}

private fun suggestedFileName(
    resolver: ContentResolver,
    uri: Uri,
    isVideo: Boolean,
): String {
    val mimeExtension = when (resolver.getType(uri)) {
        "image/jpeg" -> "jpg"
        "image/png" -> "png"
        "image/webp" -> "webp"
        "image/gif" -> "gif"
        "video/mp4" -> "mp4"
        "video/webm" -> "webm"
        "video/3gpp" -> "3gp"
        "video/quicktime" -> "mov"
        else -> null
    }
    val originalExtension = resolver.query(
        uri,
        arrayOf(OpenableColumns.DISPLAY_NAME),
        null,
        null,
        null,
    )?.use { cursor ->
        if (cursor.moveToFirst()) {
            val name = cursor.getString(0)
            name.substringAfterLast('.', "").takeIf { it.matches(Regex("[A-Za-z0-9]{1,8}")) }
        } else {
            null
        }
    }
    val extension = mimeExtension ?: originalExtension ?: if (isVideo) "mp4" else "jpg"
    return "clearcut-copy.$extension"
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ProjectDetailSheet(
    entry: ProjectEntry,
    onDismiss: () -> Unit,
    onOpen: () -> Unit,
    onDelete: () -> Unit,
) {
    ModalBottomSheet(
        onDismissRequest = onDismiss,
        sheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 20.dp, vertical = 16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            Text(
                text = entry.title,
                style = MaterialTheme.typography.headlineSmall,
                fontWeight = FontWeight.Bold,
            )
            Text(
                text = "Type: ${if (entry.mimeType?.startsWith("video/") == true) "Video" else "Image"}",
                style = MaterialTheme.typography.bodyMedium,
            )
            Text(
                text = "Created: ${formatTime(entry.createdAt)}",
                style = MaterialTheme.typography.bodyMedium,
            )
            Text(
                text = if (entry.outputPath != null) "Saved copy available" else "Original source only",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Button(onClick = onOpen, modifier = Modifier.fillMaxWidth()) {
                Text("Open in editor")
            }
            OutlinedButton(onClick = onDelete, modifier = Modifier.fillMaxWidth()) {
                Text("Remove from history")
            }
        }
    }
}

@Composable
private fun WorkflowDetailSheet(
    workflow: String,
    onSelect: () -> Unit,
) {
    val title = when (workflow) {
        "background" -> stringResource(R.string.tool_background)
        "audio" -> stringResource(R.string.tool_audio)
        else -> stringResource(R.string.tool_object)
    }
    val description = when (workflow) {
        "background" -> stringResource(R.string.workflow_background_desc)
        "audio" -> stringResource(R.string.workflow_audio_desc)
        else -> stringResource(R.string.workflow_object_desc)
    }
    val stages = listOf(
        stringResource(R.string.workflow_stage_1, title),
        stringResource(R.string.workflow_stage_2),
        stringResource(R.string.workflow_stage_3),
    )

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = 20.dp, vertical = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold,
        )
        Text(
            text = description,
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
            stages.forEach { stage ->
                Row(verticalAlignment = Alignment.Top) {
                    Box(
                        modifier = Modifier
                            .size(10.dp)
                            .clip(CircleShape)
                            .background(MaterialTheme.colorScheme.primary)
                            .padding(top = 4.dp),
                    )
                    Spacer(Modifier.width(10.dp))
                    Text(stage, style = MaterialTheme.typography.bodyMedium)
                }
            }
        }
        Button(onClick = onSelect, modifier = Modifier.fillMaxWidth()) {
            Text(stringResource(R.string.workflow_select_button))
        }
    }
}

private fun formatTime(timestamp: Long): String {
    val formatter = SimpleDateFormat("dd MMM yyyy • HH:mm", Locale.getDefault())
    return formatter.format(Date(timestamp))
}

private val ColorAccent = androidx.compose.ui.graphics.Color(0xFF4DC9AA)
