package com.example.bciproject.apisetting

import com.example.bciproject.model.RegisterCallModel
import com.example.bciproject.model.RegisterCallbackModel
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface RegisterInterface {
    @POST("/api/register")
    fun register(@Body credential: RegisterCallModel): Call<RegisterCallbackModel>
}