package com.example.bciproject.ui

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.bciproject.databinding.ActivityProfileBinding

class ProfileActivity : AppCompatActivity(){

    private lateinit var binding: ActivityProfileBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityProfileBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.devicesButton.setOnClickListener{
            startActivity(Intent(this, DevicesActivity::class.java))
        }
        binding.mindVoiceButton.setOnClickListener{
            startActivity(Intent(this, MindVoiceActivity::class.java))
        }
        binding.profileButton.setOnClickListener{
            //startActivity(Intent(this, ProfileActivity::class.java))
        }


    }

}