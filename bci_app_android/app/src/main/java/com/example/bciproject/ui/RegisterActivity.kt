package com.example.bciproject.ui

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.widget.Toast
import com.example.bciproject.adaptor.RegisterAdapter
import com.example.bciproject.databinding.ActivityRegisterBinding

class RegisterActivity : AppCompatActivity() {

    private lateinit var binding: ActivityRegisterBinding
    private val registerAdapter = RegisterAdapter()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityRegisterBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.registerButton.setOnClickListener {
            val username = binding.usernameEditText.text.toString()
            val password = binding.passwordEditText.text.toString()
            val email = binding.emailEditText.text.toString()
            registerAdapter.register(username, password, email) { isSuccess, message ->
                if (isSuccess) {
                    Toast.makeText(this, "Registration Successful", Toast.LENGTH_SHORT).show()
                    startActivity(Intent(this, DevicesActivity::class.java))

                } else {
                    Toast.makeText(this, "Registration Failed: $message", Toast.LENGTH_SHORT).show()
                }
            }
        }

        binding.backToLoginButton.setOnClickListener {
            // Navigate back to the Login Activity
            finish()
        }
    }
}
