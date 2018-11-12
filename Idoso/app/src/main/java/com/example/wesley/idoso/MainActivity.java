package com.example.wesley.idoso;

import android.content.DialogInterface;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);



        Button conecta = (Button) findViewById(R.id.conecta);
        conecta.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent it = new Intent(view.getContext(), Conecta.class);
                it.putExtra("ip", ((EditText) findViewById(R.id.ip)).getText().toString());
                it.putExtra("port", ((EditText) findViewById(R.id.port)).getText().toString());
                it.putExtra("user", ((EditText) findViewById(R.id.user)).getText().toString());
                startActivity(it);
            }
        });


    }



}
