package com.example.wesley.idoso;

import android.content.Intent;
import android.media.MediaPlayer;
import android.os.Bundle;
import android.os.Vibrator;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;


public class Alerta extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_alerta);

        Vibrator vibrator = (Vibrator) getSystemService(VIBRATOR_SERVICE);
        long milliseconds = 2000;
        vibrator.vibrate(milliseconds);
//        for(int i = 0;i < 50;i++){
//            Vibrator vibrator = (Vibrator) getSystemService(VIBRATOR_SERVICE);
//            long milliseconds = 2000;
//            vibrator.vibrate(milliseconds);
//        }

        MediaPlayer mp = MediaPlayer.create(Alerta.this, R.raw.alert);
        mp.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {

            @Override
            public void onCompletion(MediaPlayer mp) {

                mp.release();
            }

        });
        mp.start();


        Button botao_img = findViewById(R.id.button_img);

        botao_img.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent it = new Intent(Alerta.this, tela_alerta.class);
                startActivity(it);
            }
        });
    }
}
