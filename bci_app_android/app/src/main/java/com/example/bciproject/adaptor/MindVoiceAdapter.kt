package com.example.bciproject.adaptor

import com.example.bciproject.apisetting.EEGInterface
import com.example.bciproject.apisetting.EEGRetrofitManager
import com.example.bciproject.model.EEGCallModel
import com.example.bciproject.model.EEGCallbackModel
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import android.content.Context
import com.example.bciproject.util.ProgressionBar
import com.google.gson.Gson
import com.google.gson.JsonObject
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class MindVoiceAdapter(private val context: Context){
    fun sendEEGData(action: String, callback: (String) -> Unit, progressionBar: ProgressionBar) {
        val eegData = loadEEGDataFromAssets(action) // 假設你有一個方法來從assets加載對應的JSON數據
        progressionBar.startLoading()
        val client = EEGRetrofitManager().getEEGClient().create(EEGInterface::class.java)
        client.analyzeEEGData(eegData!!).enqueue(object : Callback<EEGCallbackModel> {
            override fun onResponse(call: Call<EEGCallbackModel>, response: Response<EEGCallbackModel>) {
                progressionBar.dismissLoading()
                if (response.isSuccessful && response.body() != null) {
                    val eegResponse = response.body()!!
                    callback(eegResponse.label)
                } else {
                    callback("Error: Unable to analyze data")
                }
            }

            override fun onFailure(call: Call<EEGCallbackModel>, t: Throwable) {
                progressionBar.dismissLoading()
                println("------------------")
                println(t.message)
                callback("Network error: ${t.message}")
            }
        })
    }

    private fun loadEEGDataFromAssets(action: String): EEGCallModel? {
        val fileName = "$action.json"
        val jsonString = try {
            context.assets.open(fileName).bufferedReader().use { it.readText() }
        } catch (ioException: IOException) {
            ioException.printStackTrace()
            return null
        }

        val jsonObject = Gson().fromJson(jsonString, JsonObject::class.java)
        val dataAsArray = Gson().fromJson(jsonObject.get("data"), Array<Array<Float>>::class.java)
        val dataList = dataAsArray.map { it.toList() }

        val currentTime = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(Date())
        val userName = "Jack_Liao"

        return EEGCallModel(dataList, currentTime, userName)
    }

}