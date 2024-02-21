package com.example.bciproject.apisetting

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class RegisterRetrofitManager {
    fun getRegisterClient(): Retrofit {
        return Retrofit.Builder()
            .baseUrl("http://0.0.0.0:8000") // 更換為你的API基礎URL
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }
}
