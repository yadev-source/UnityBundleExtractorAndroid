package com.yadev.ubea;

import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class MainActivity extends AppCompatActivity {
    TextView tvLog;
    Button btnTest;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tvLog = findViewById(R.id.tvLog);
        btnTest = findViewById(R.id.btnTest);

        // Init Python
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }

        btnTest.setOnClickListener(v -> {
            tvLog.setText("Loading UnityPy...\n");
            try {
                Python py = Python.getInstance();
                // panggil main.py
                py.getModule("main").callAttr("hello");
                String result = py.getModule("main").callAttr("test_unitypy").toString();
                tvLog.setText(result);
            } catch (Exception e) {
                tvLog.setText("Error: " + e.getMessage() + "\n" + e.toString());
                e.printStackTrace();
            }
        });

        tvLog.setText("UnityBundleExtractorAndroid\nReady!\n\nKlik TEST UNITYPY");
    }
}