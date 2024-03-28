package com.example.bciproject.apisetting

import com.example.bciproject.model.EEGCallModel
import com.example.bciproject.model.EEGCallbackModel
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface MindVoiceInterface {
    @POST("/api/analyze/")
    fun analyzeEEGData(@Body eegData: EEGCallModel): Call<EEGCallbackModel>
}