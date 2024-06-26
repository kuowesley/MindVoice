plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.bciproject"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.bciproject"
        minSdk = 29
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = "1.8"
    }
    buildFeatures {
        viewBinding = true
    }

    packagingOptions {
        exclude("META-INF/LICENSE.md")
        exclude("META-INF/LICENSE-notice.md")
    }
}

dependencies {

    implementation("androidx.core:core-ktx:1.10.1")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.9.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("androidx.navigation:navigation-fragment-ktx:2.6.0")
    implementation("androidx.navigation:navigation-ui-ktx:2.6.0")
    androidTestImplementation("junit:junit:4.13.2")
    androidTestImplementation("androidx.test.ext:junit:1.1.5")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.5.1")
    // Retrofit核心庫
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    // Gson轉換器，用於Retrofit
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    // OkHttp日誌攔截器（可選）
    implementation("com.squareup.okhttp3:logging-interceptor:4.9.1")
    implementation("com.google.android.material:material:1.4.0")



    // Mockito dependencies
    testImplementation ("org.mockito:mockito-core:2.22")
    testImplementation ("org.robolectric:robolectric:4.+")
    // Android Testing Support for Mockito
    androidTestImplementation ("org.mockito:mockito-android:3.12.4")
    // Additional dependencies for unit testing
    // This is required for mocking final classes
    testImplementation ("org.mockito:mockito-inline:3.12.4")
    // Android Testing Support
    androidTestImplementation ("androidx.test:core:1.x")
    //androidTestImplementation ("androidx.test.ext:junit:1.x")
    androidTestImplementation ("androidx.test:runner:1.x")
    //androidTestImplementation ("androidx.test.espresso:espresso-core:3.x")
    androidTestImplementation("org.junit.jupiter:junit-jupiter:5.8.1")
    testImplementation ("org.mockito.kotlin:mockito-kotlin:4.0.0")
    //androidTestImplementation ("org.mockito:mockito-inline:3.x.x")
    testImplementation ("io.mockk:mockk:1.12.0")
    androidTestImplementation("org.testng:testng:6.9.6")


}