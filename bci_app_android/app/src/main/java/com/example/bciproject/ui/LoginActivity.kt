package com.example.bciproject.ui
import android.content.Intent

import android.os.Bundle
import android.widget.Toast
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.findNavController
import androidx.navigation.ui.AppBarConfiguration
import androidx.navigation.ui.navigateUp
import androidx.navigation.ui.setupActionBarWithNavController
import com.example.bciproject.R
import com.example.bciproject.adaptor.LoginAdapter
import com.example.bciproject.databinding.ActivityLoginBinding

class LoginActivity : AppCompatActivity() {

    private lateinit var binding: ActivityLoginBinding
    private val loginAdapter = LoginAdapter()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.loginButton.setOnClickListener {
            val username = binding.usernameEditText.text.toString()
            val password = binding.passwordEditText.text.toString()
            loginAdapter.login(username, password) { isSuccess, message ->
                if (isSuccess) {
                    Toast.makeText(this, "Login Successful", Toast.LENGTH_SHORT).show()
                    startActivity(Intent(this, DevicesActivity::class.java)) // 跳轉至EEGActivity
                    finish() // 結束當前Activity
                } else {
                    runOnUiThread {
                        Toast.makeText(this, "Login Failed: $message", Toast.LENGTH_SHORT).show()
                    }
                }
            }
        }

        binding.registerButton.setOnClickListener {
            // 跳轉至註冊頁面
            startActivity(Intent(this, RegisterActivity::class.java))
        }

        //test without login
        binding.testButton.setOnClickListener {
            startActivity(Intent(this, DevicesActivity::class.java))
        }
    }
}