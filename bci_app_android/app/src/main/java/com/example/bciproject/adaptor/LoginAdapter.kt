package com.example.bciproject.adaptor

import com.example.bciproject.apisetting.LoginInterface
import com.example.bciproject.apisetting.LoginRetrofitManager
import com.example.bciproject.model.LoginCallModel
import com.example.bciproject.model.LoginCallbackModel
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class LoginAdapter {

    fun login(username: String, password: String, callback: (Boolean, String) -> Unit) {
        val loginCallModel = LoginCallModel(user = username, password = password)
        val client = LoginRetrofitManager().getLoginClient().create(LoginInterface::class.java)
        client.getLogin(loginCallModel).enqueue(object : Callback<LoginCallbackModel> {
            override fun onResponse(call: Call<LoginCallbackModel>, response: Response<LoginCallbackModel>) {
                if (response.isSuccessful && response.body() != null) {
                    val loginResponse = response.body()!!
                    callback(loginResponse.response, loginResponse.reason ?: "Success")
                } else {
                    callback(false, "Login Failed")
                }
            }

            override fun onFailure(call: Call<LoginCallbackModel>, t: Throwable) {
                callback(false, "Network Error: ${t.message}")
            }
        })
    }
}
