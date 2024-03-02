package com.example.bciproject.apisetting
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
class LoginRetrofitManager {
    fun getLoginClient(): Retrofit {
        return Retrofit.Builder()
            .baseUrl("https://ssw555-agile-duck.onrender.com") // 更換為你的API基礎URL
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }
}
