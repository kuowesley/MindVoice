package com.example.bciproject.adaptor

import android.Manifest
import android.app.Activity
import com.example.bciproject.apisetting.EEGInterface
import com.example.bciproject.apisetting.EEGRetrofitManager
import com.example.bciproject.model.EEGCallModel
import com.example.bciproject.model.EEGCallbackModel
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.content.ContextCompat.startActivity
import com.example.bciproject.apisetting.MindVoiceInterface
import com.example.bciproject.apisetting.MindVoiceRetrofitManager
import com.example.bciproject.util.ProgressionBar
import com.google.gson.Gson
import com.google.gson.JsonObject
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class MindVoiceAdapter(private val context: Context, private val activity: Activity){
    fun sendEEGData(action: String, callback: (String) -> Unit, progressionBar: ProgressionBar) {
        val eegData = loadEEGDataFromAssets(action) // 假設你有一個方法來從assets加載對應的JSON數據
        progressionBar.startLoading()
        val client = MindVoiceRetrofitManager().getEEGClient().create(MindVoiceInterface::class.java)
        client.analyzeEEGData(eegData!!).enqueue(object : Callback<EEGCallbackModel> {
            override fun onResponse(call: Call<EEGCallbackModel>, response: Response<EEGCallbackModel>) {
                progressionBar.dismissLoading()
                if (response.isSuccessful && response.body() != null) {
                    val eegResponse = response.body()!!
                    val result = mapLabelToString(eegResponse.label)
                    callback(result)
                    if(result == "Help Me"){
                        makePhoneCall()
                    }
                    //callback(eegResponse.label)
                } else {
                    callback("Error: Unable to analyze data")
                }
            }

            override fun onFailure(call: Call<EEGCallbackModel>, t: Throwable) {
                progressionBar.dismissLoading()
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

    private fun mapLabelToString(label: String): String{
        val fileName = "classify.json"
        val jsonString = try {
            context.assets.open(fileName).bufferedReader().use { it.readText() }
        } catch (ioException: IOException) {
            ioException.printStackTrace()
            return "Map label fail"
        }

        val jsonObject = Gson().fromJson(jsonString, JsonObject::class.java)
        val action = jsonObject.get(label).toString().trim('"')
        return action
    }

    private fun makePhoneCall() {
        val callIntent = Intent(Intent.ACTION_CALL)
        callIntent.data = Uri.parse("tel:000") // Use the emergency number for your country

        if (ContextCompat.checkSelfPermission(context, Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(activity, arrayOf(Manifest.permission.CALL_PHONE), 1)
        } else {
            context.startActivity(callIntent)
        }
    }

}