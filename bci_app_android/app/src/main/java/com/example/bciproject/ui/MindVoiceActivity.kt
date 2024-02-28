package com.example.bciproject.ui

import android.content.Intent
import android.media.MediaPlayer
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.bciproject.R
import com.example.bciproject.adaptor.EEGAdapter
import com.example.bciproject.adaptor.MindVoiceAdapter
import com.example.bciproject.databinding.ActivityMindvoiceBinding
import java.util.Locale

class MindVoiceActivity : AppCompatActivity(){

    private lateinit var binding: ActivityMindvoiceBinding
    private val mindVoiceAdapter = MindVoiceAdapter(this)
    private var classify = mapOf("0" to "hello", "1" to "help_me", "2" to "stop", "3" to "thank_you", "4" to "yes")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMindvoiceBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val testCase = intent.getStringExtra("TESTCASE")

        // default to text mode
        var mode = "text"

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
                mindVoiceAdapter.sendEEGData(testCase.toString()) { label ->
                    binding.result.text = label
                    if(mode == "voice"){
                        val action = classify[label].toString()
                        val resourceName = action.toLowerCase(Locale.getDefault()).replace(" ", "_")
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
                }
            }

        }

        binding.textModeButton.setOnClickListener{
            //switch to text mode
            mode = "text"
        }
        binding.voiceModeButton.setOnClickListener{
            //switch to voice mode
            mode = "voice"
        }

    }

}