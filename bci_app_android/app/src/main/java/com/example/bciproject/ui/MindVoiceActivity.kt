package com.example.bciproject.ui

import android.Manifest
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.content.res.ColorStateList
import android.media.MediaPlayer
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.example.bciproject.R
import com.example.bciproject.adaptor.MindVoiceAdapter
import com.example.bciproject.databinding.ActivityMindvoiceBinding
import com.example.bciproject.util.ProgressionBar
import com.google.android.material.button.MaterialButton
import java.util.Locale



class MindVoiceActivity : AppCompatActivity(){

    private lateinit var binding: ActivityMindvoiceBinding
    private val mindVoiceAdapter = MindVoiceAdapter(this, this@MindVoiceActivity)
    private var classify = mapOf("0" to "hello", "1" to "help_me", "2" to "stop", "3" to "thank_you", "4" to "yes")


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMindvoiceBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val testCase = intent.getStringExtra("TESTCASE")

        // default to text mode
        var mode = "text"

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CALL_PHONE) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this@MindVoiceActivity, arrayOf(Manifest.permission.CALL_PHONE), 1)
        }

        binding.devicesButton.setOnClickListener{
            startActivity(Intent(this, DevicesActivity::class.java))
        }
        binding.mindVoiceButton.setOnClickListener{
            //startActivity(Intent(this, MindVoiceActivity::class.java))
        }
        binding.profileButton.setOnClickListener{
            startActivity(Intent(this, ProfileActivity::class.java))
        }



        binding.startEndButton.setOnClickListener{
            //switch between start and end

            //test
            if(testCase.isNullOrEmpty()){
                Toast.makeText(this@MindVoiceActivity, "Error: TestCase is empty", Toast.LENGTH_SHORT).show()
            }else{
                val progressionBar = ProgressionBar(this)
                mindVoiceAdapter.sendEEGData(testCase.toString(), { action ->
                    binding.result.text = action

                    if(mode == "voice"){
                        val resourceName = action.lowercase(Locale.getDefault()).replace(" ", "_")
                        val resourceId = resources.getIdentifier(resourceName, "raw", packageName)
                        if (resourceId != 0){
                            val mediaPlayer = MediaPlayer.create(this@MindVoiceActivity, resourceId)
                            mediaPlayer.start() // Start playback

                            // Optional: Release the MediaPlayer resources once playback is completed
                            mediaPlayer.setOnCompletionListener {
                                mediaPlayer.release()
                            }
                        }
                    }
                }, progressionBar)
            }

        }

        var textModeButton = findViewById<MaterialButton>(com.example.bciproject.R.id.textModeButton)
        var voiceModeButton = findViewById<MaterialButton>(com.example.bciproject.R.id.voiceModeButton)
        binding.textModeButton.setOnClickListener{
            //switch to text mode

            mode = "text"
            textModeButton.setBackgroundColor(ContextCompat.getColor(this, R.color.mode_on));
            voiceModeButton.setBackgroundColor(ContextCompat.getColor(this, R.color.mode_off));
        }
        binding.voiceModeButton.setOnClickListener{
            //switch to voice mode
            mode = "voice"
            textModeButton.setBackgroundColor(ContextCompat.getColor(this, R.color.mode_off));
            voiceModeButton.setBackgroundColor(ContextCompat.getColor(this, R.color.mode_on));
        }

    }

}