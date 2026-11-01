package com.yadev.ubea;

import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class MainActivity extends AppCompatActivity {
    TextView tvLog;
    Button btnTest, btnCopy;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tvLog = findViewById(R.id.tvLog);
        btnTest = findViewById(R.id.btnTest);
        btnCopy = findViewById(R.id.btnCopy);

        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }

        btnTest.setOnClickListener(v -> {
            tvLog.setText("Loading UnityPy...\n");
            try {
                Python py = Python.getInstance();
                py.getModule("main").callAttr("hello");
                String result = py.getModule("main").callAttr("test_unitypy").toString();
                tvLog.setText(result);
            } catch (Exception e) {
                tvLog.setText("Error: " + e.getMessage() + "\n" + e.toString());
                e.printStackTrace();
            }
        });

        btnCopy.setOnClickListener(v -> {
            String text = tvLog.getText().toString();
            ClipboardManager cm = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
            ClipData clip = ClipData.newPlainText("log", text);
            cm.setPrimaryClip(clip);
            Toast.makeText(this, "Log copied!", Toast.LENGTH_SHORT).show();
        });

        tvLog.setText("UnityBundleExtractorAndroid\nReady!\n\nKlik TEST UNITYPY\nKlik COPY LOG untuk copy error");
    }
}