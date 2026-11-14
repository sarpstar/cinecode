package com.clearcut.app.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "projects")
data class ProjectEntry(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val title: String,
    val uri: String,
    val mimeType: String?,
    val createdAt: Long,
    val outputPath: String? = null,
)
