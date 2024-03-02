package com.example.bciproject.util

import android.app.Activity
import android.app.AlertDialog
import com.example.bciproject.R
class ProgressionBar (private var activity: Activity? = null){
    private var alertDialog2: AlertDialog? = null

    fun loading (myActivity: Activity) {
        activity = myActivity
    }
    fun startLoading() {
        val builder = AlertDialog.Builder(activity)
        val inflater = activity!!.layoutInflater
        builder.setView(inflater.inflate(R.layout.progression_layout, null))
        //等於true時滑鼠點一下即可暫停
        //等於false時則不會暫停
        builder.setCancelable(true)
        alertDialog2 = builder.create()
        alertDialog2!!.show()
    }

    fun dismissLoading() {
        alertDialog2!!.dismiss()
    }
}