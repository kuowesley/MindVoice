package com.example.bciproject.ui

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.bciproject.adaptor.EEGAdapter
import com.example.bciproject.databinding.ActivityEegBinding

class EEGActivity : AppCompatActivity() {

    private lateinit var binding: ActivityEegBinding
    private val eegAdapter = EEGAdapter(this)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityEegBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // 這裡只是一個示例按鈕的設置，你需要為其他按鈕做類似的設置
        binding.yesButton.setOnClickListener {
            eegAdapter.sendEEGData("yes") { label ->
                binding.resultTextView.text = label
            }
        }

        binding.helpMeButton.setOnClickListener {
            eegAdapter.sendEEGData("help_me") { label ->
                binding.resultTextView.text = label
            }
        }

        binding.stopButton.setOnClickListener {
            eegAdapter.sendEEGData("stop") { label ->
                binding.resultTextView.text = label
            }
        }

        binding.thankYouButton.setOnClickListener {
            eegAdapter.sendEEGData("thank_you") { label ->
                binding.resultTextView.text = label
            }
        }

        binding.helloButton.setOnClickListener {
            eegAdapter.sendEEGData("hello") { label ->
                binding.resultTextView.text = label
            }
        }

// Analyze按鈕留置空操作
        binding.analyzeButton.setOnClickListener {
            // 這裡可以添加對Analyze操作的處理，目前留空
        }


    }
}
