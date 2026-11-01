plugins {
    alias(libs.plugins.android.application)
    id("com.chaquo.python") version "17.2.0"
}

android {
    namespace = "com.yadev.ubea"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.yadev.ubea"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildFeatures {
        viewBinding = true
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

chaquopy {
    defaultConfig {
        version = "3.11"
        pip {
            install("UnityPy")
            install("tqdm")
            install("lz4")
            install("Pillow")
            install("brotli")
            // install("texture2ddecoder") // nanti kalau butuh
            // install("etcpak") // nanti kalau butuh
        }
    }
}

dependencies {
    implementation(libs.androidx.core)
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
    implementation(libs.androidx.constraintlayout)
}