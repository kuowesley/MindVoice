package com.example.bciproject.ui

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.bciproject.adaptor.DevicesAdapter
import com.example.bciproject.adaptor.EEGAdapter
import com.example.bciproject.databinding.ActivityDevicesBinding
import android.widget.PopupMenu
import android.widget.TextView
import android.widget.Toast
import com.example.bciproject.R

class DevicesActivity : AppCompatActivity(){

    private lateinit var binding: ActivityDevicesBinding
    private val devicesAdapter = DevicesAdapter()
    private var testCase = ""

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityDevicesBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.devicesButton.setOnClickListener{
            //startActivity(Intent(this, DevicesPageActivity::class.java))
        }
        binding.mindVoiceButton.setOnClickListener{
            startActivity(Intent(this, MindVoiceActivity::class.java))
        }
        binding.profileButton.setOnClickListener{
            startActivity(Intent(this, ProfileActivity::class.java))
        }

        binding.pairDeviceImage.setOnClickListener{
            val popup = PopupMenu(this@DevicesActivity, it)
            popup.menuInflater.inflate(R.menu.popup_menu, popup.menu)
            popup.setOnMenuItemClickListener { item ->
                //Toast.makeText(this@DevicesActivity, "You Clicked: ${item.title}", Toast.LENGTH_SHORT).show()

                val textPair: TextView = findViewById(R.id.text_pair)
                textPair.text = item.title
                testCase = item.title.toString()
                true
            }
            popup.show()
        }

        binding.startButton.setOnClickListener{
            if (testCase.isNotEmpty()) {
                // Variable is not empty, proceed with starting the activity and pass the variable
                val intent = Intent(this, MindVoiceActivity::class.java)
                intent.putExtra("TESTCASE", testCase)
                startActivity(intent)
            } else {
                // Variable is empty, show an error
                Toast.makeText(this@DevicesActivity, "Error: Variable is empty", Toast.LENGTH_SHORT).show()
            }
        }

    }
}