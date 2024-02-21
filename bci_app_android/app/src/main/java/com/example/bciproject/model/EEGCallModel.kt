package com.example.bciproject.model

data class EEGCallModel(
    val data: List<List<Float>>, // 假設為64個包含795項浮點數的列表
    val time: String,
    val userName: String
)
