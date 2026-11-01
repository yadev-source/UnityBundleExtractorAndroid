package com.yadev.ubea;

import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.OpenableColumns;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import java.io.*;

public class MainActivity extends AppCompatActivity {
    TextView tvLog;
    Button btnTest, btnCopy, btnPick;
    String lastBundlePath = null;
    ActivityResultLauncher<Intent> filePicker;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tvLog = findViewById(R.id.tvLog);
        btnTest = findViewById(R.id.btnTest);
        btnCopy = findViewById(R.id.btnCopy);
        btnPick = findViewById(R.id.btnPick);

        if (!Python.isStarted()) Python.start(new AndroidPlatform(this));

        filePicker = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    Uri uri = result.getData().getData();
                    handleFile(uri);
                }
            });

        btnTest.setOnClickListener(v -> {
            try {
                String r = Python.getInstance().getModule("main").callAttr("test_unitypy").toString();
                tvLog.setText(r);
            } catch (Exception e) {
                tvLog.setText("Error: " + e);
            }
        });

        btnPick.setOnClickListener(v -> {
            Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
            intent.addCategory(Intent.CATEGORY_OPENABLE);
            intent.setType("*/*");
            filePicker.launch(intent);
        });

        btnCopy.setOnClickListener(v -> {
            ClipboardManager cm = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
            cm.setPrimaryClip(ClipData.newPlainText("log", tvLog.getText()));
            Toast.makeText(this, "Log copied!", Toast.LENGTH_SHORT).show();
        });

        tvLog.setText("UnityBundleExtractorAndroid\n\n1. TEST UNITYPY dulu\n2. PICK BUNDLE file .bundle/.assets\n3. COPY LOG kalau error");
    }

    void handleFile(Uri uri) {
        try {
            String fileName = getFileName(uri);
            File inputFile = new File(getCacheDir(), fileName);
            copyUriToFile(uri, inputFile);
            lastBundlePath = inputFile.getAbsolutePath();
            
            tvLog.setText("Picked: " + fileName + "\nExtracting...\n");
            
            File outDir = new File(getExternalFilesDir(null), "extracted/" + fileName + "_out");
            String result = Python.getInstance().getModule("main")
                .callAttr("extract_bundle", lastBundlePath, outDir.getAbsolutePath()).toString();
            
            tvLog.setText(result + "\n\nPath: " + outDir.getAbsolutePath());
            Toast.makeText(this, "Done! Check " + outDir.getAbsolutePath(), Toast.LENGTH_LONG).show();
            
        } catch (Exception e) {
            tvLog.setText("Pick failed: " + e + "\n" + e.toString());
        }
    }

    String getFileName(Uri uri) {
        String result = "bundle_file";
        if (uri.getScheme().equals("content")) {
            try (Cursor cursor = getContentResolver().query(uri, null, null, null, null)) {
                if (cursor != null && cursor.moveToFirst()) {
                    int idx = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                    if (idx >=0) result = cursor.getString(idx);
                }
            }
        }
        if (result == null) result = uri.getPath().substring(uri.getPath().lastIndexOf('/')+1);
        return result;
    }

    void copyUriToFile(Uri uri, File dest) throws IOException {
        try (InputStream in = getContentResolver().openInputStream(uri);
             OutputStream out = new FileOutputStream(dest)) {
            byte[] buf = new byte[8192];
            int len;
            while ((len = in.read(buf)) > 0) out.write(buf, 0, len);
        }
    }
}