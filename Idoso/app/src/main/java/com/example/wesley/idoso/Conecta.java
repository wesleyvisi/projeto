package com.example.wesley.idoso;

import android.app.AlertDialog;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.TaskStackBuilder;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Build;
import android.os.Message;
import android.os.Messenger;
import android.os.Parcel;
import android.os.Parcelable;
import android.support.annotation.RequiresApi;
import android.support.v4.app.NotificationCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.Serializable;


public class Conecta extends AppCompatActivity implements CustomHandler.AppReceiver, Serializable {

    private CustomHandler handler;
    TextView status;
    TextView mensagem;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_conecta);

        Intent it = getIntent();
        String ip = it.getStringExtra("ip");
        String port = it.getStringExtra("port");
        String user = it.getStringExtra("user");

        this.status = (TextView) findViewById(R.id.status);
        this.mensagem = (TextView) findViewById(R.id.mensagem);
        status.setText("Conectando a: "+user+"  -  "+ip+" : "+port);


        handler = new CustomHandler(this);

        final Intent itService = new Intent(this,ConectaService.class);
        itService.putExtra("ip", ip);
        itService.putExtra("port", port);
        itService.putExtra("user", user);
        itService.putExtra("handler", new Messenger(handler));
        startService(itService);

        Button stop = (Button) findViewById(R.id.stop);

        stop.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                stopService(itService);
            }
        });


    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    public void onReceiveResult(Message message) {
        switch (message.what) {
            case 0:
                Toast.makeText(this,(String)message.obj,Toast.LENGTH_SHORT).show();
                this.status.setText((String)message.obj);
                break;
            case 1:
//                int notifyID = 1;
//                String CHANNEL_ID = "my_channel_01";// The id of the channel.
//                CharSequence name = CHANNEL_ID;
//                int importancee = NotificationManager.IMPORTANCE_HIGH;
//
//                NotificationManager mNotificationManager =
//                        (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
//
//                NotificationCompat.Builder notificationc = new NotificationCompat.Builder(this);
//
//                notificationc.setSmallIcon(R.drawable.ic_launcher_foreground)
//                        .setContentTitle("My notification")
//                        .setContentText("Hello World!")
//                        .setColor(Color.rgb(255,50,50))
//                        .setCategory(Notification.CATEGORY_ALARM)
//                        .setVibrate(new long[]{150,300,150,600,150,600});
//
//
//                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
//
//                    NotificationChannel mChannell = new NotificationChannel(CHANNEL_ID, name, importancee);
//                    mNotificationManager.createNotificationChannel(mChannell);
//
//                    notificationc.setChannelId(CHANNEL_ID);
//                }
//
//                Notification notification = notificationc.build();
//
//
//
//
//                mNotificationManager.notify(notifyID , notification);
////                this.finish();
                break;
            case 2:

                break;
            case 3:

                this.mensagem.setText((String)message.obj);
                break;
            case 4:

                this.mensagem.setText((String)message.obj);


                int notifyID = 1;
                String CHANNEL_ID = "my_channel_01";// The id of the channel.
                CharSequence name = CHANNEL_ID;
                int importancee = NotificationManager.IMPORTANCE_HIGH;

                NotificationManager mNotificationManager =
                        (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);

                NotificationCompat.Builder notificationc = new NotificationCompat.Builder(this);

                notificationc.setSmallIcon(R.drawable.ic_launcher_foreground)
                        .setContentTitle("My notification")
                        .setContentText("Hello World!")
                        .setVibrate(new long[]{150,300,150,600,150,600});


                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {

                    NotificationChannel mChannell = new NotificationChannel(CHANNEL_ID, name, importancee);
                    mNotificationManager.createNotificationChannel(mChannell);

                    notificationc.setChannelId(CHANNEL_ID);
                }

                Notification notification = notificationc.build();




                mNotificationManager.notify(notifyID , notification);



                Intent resultIntent = new Intent(this, Alerta.class);
                startActivity(resultIntent);
                break;
        }
    }

    @Override
    public void onDestroy(){
        super.onDestroy();
    }


}
