package com.example.bciproject.adaptor

import com.example.bciproject.apisetting.RegisterInterface
import com.example.bciproject.apisetting.RegisterRetrofitManager
import com.example.bciproject.model.RegisterCallModel
import com.example.bciproject.model.RegisterCallbackModel
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class RegisterAdapter {

    fun register(username: String, password: String, email: String, callback: (Boolean, String) -> Unit) {
        val registerCallModel = RegisterCallModel(username, password, email)
        val client = RegisterRetrofitManager().getRegisterClient().create(RegisterInterface::class.java)
        client.register(registerCallModel).enqueue(object : Callback<RegisterCallbackModel> {
            override fun onResponse(call: Call<RegisterCallbackModel>, response: Response<RegisterCallbackModel>) {
                if (response.isSuccessful && response.body() != null) {
                    val registerResponse = response.body()!!
                    callback(true, "Registration successful")
                } else {
                    callback(false, "Registration failed")
                }
            }

            override fun onFailure(call: Call<RegisterCallbackModel>, t: Throwable) {
                callback(false, "Network error: ${t.message}")
            }
        })
    }
}
