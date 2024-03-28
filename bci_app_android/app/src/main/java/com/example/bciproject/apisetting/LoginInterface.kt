package com.example.bciproject.apisetting

import com.example.bciproject.model.LoginCallModel
import com.example.bciproject.model.LoginCallbackModel
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface LoginInterface {
    @POST("/api/login/")
    fun getLogin(@Body credential: LoginCallModel): Call<LoginCallbackModel>
}
