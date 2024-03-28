package com.example.bciproject.apisetting

import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

class RegisterRetrofitManager {
    fun getRegisterClient(): Retrofit {
        val okHttpClient = OkHttpClient.Builder()
            .connectTimeout(300, TimeUnit.SECONDS) // Set your desired connection timeout
            .readTimeout(300, TimeUnit.SECONDS)    // Set your desired read timeout
            .writeTimeout(300, TimeUnit.SECONDS)   // Set your desired write timeout
            .build()

        return Retrofit.Builder()
            .baseUrl("https://ssw555-agile-duck.onrender.com") // 更換為你的API基礎URL
            .addConverterFactory(GsonConverterFactory.create())
            .client(okHttpClient)
            .build()
    }
}
