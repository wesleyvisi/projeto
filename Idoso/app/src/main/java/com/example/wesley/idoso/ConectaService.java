package com.example.wesley.idoso;

import android.app.IntentService;
import android.content.Intent;
import android.os.Message;
import android.os.Messenger;
import android.os.RemoteException;
import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;



public class ConectaService extends IntentService {


    public static final int STATUS_RUNNING = 0;
    public static final int STATUS_FINISHED = 1;
    public static final int STATUS_ERROR = 2;
    public static final int STATUS_STATUS = 3;

    public static final int COMODO_VAZIO = 0;
    public static final int OBJETO_NO_COMODO = 1;
    public static final int PESSOA_NO_COMODO = 2;
    public static final int ALERTA_RISCO = 3;
    public static final int SAIU_DA_CASA = 4;
    public static final int PODE_ESTAR_NO_BANHEIRO = 5;


    String ip;
    int port;
    String user;
    Socket socket;
    Boolean ativo = true;
    String message;
    Messenger handler;
    BufferedReader stdIn = null;
    PrintWriter out;

    /**
     * A constructor is required, and must call the super IntentService(String)
     * constructor with a name for the worker thread.
     */
    public ConectaService() {
        super("ConectaServiceThread");

    }


    /**
     * The IntentService calls this method from the default worker thread with
     * the intent that started the service. When this method returns, IntentService
     * stops the service, as appropriate.
     */
    @Override
    protected void onHandleIntent(Intent intent) {
        // Normally we would do some work here, like download a file.
        // For our sample, we just sleep for 5 seconds.
        this.ip =  intent.getStringExtra("ip");
        this.port = intent.getIntExtra("port",5000);
        this.user =  intent.getStringExtra("user");


        handler = intent.getParcelableExtra("handler");


//        Intent notificationIntent = new Intent(this, MainActivity.class);
//
//        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0,
//                notificationIntent, 0);
//
//        Notification notification = new NotificationCompat.Builder(this)
//                .setSmallIcon(R.mipmap.ic_launcher_round)
//                .setContentTitle("My Awesome App")
//                .setContentText("Doing some work...")
//                .setContentIntent(pendingIntent).build();
//
//        startForeground(1337, notification);



        conectaSocket();



        // Read data
//        DataInputStream inputStream = null;
//        try {
//            inputStream = new DataInputStream(socket.getInputStream());
//        } catch (IOException e) {
//            e.printStackTrace();
//        }


        Message msg = new Message();
        msg.obj = "Conectado com: "+this.ip+":"+this.port;
        msg.what = STATUS_RUNNING;
        try {
            handler.send(msg);
        } catch (RemoteException e) {
            e.printStackTrace();
        }
        JSONObject obj = null;
        while(this.ativo){
            obj = lerSocket();


            Log.e("while", String.valueOf(message));



            msg = new Message();
            msg.obj = "Conectado com: "+this.ip+":"+this.port;

            String comodo = "";
            int estado = 0;


            try {
                comodo = obj.getString("comodo");
                estado = obj.getInt("estado");
            } catch (JSONException e) {
                e.printStackTrace();
            }

            switch (estado){
                case COMODO_VAZIO:
                    msg.obj = "Comodo vazio";
                    break;
                case OBJETO_NO_COMODO:
                    msg.obj = "Objeto no comodo";

                    break;
                case PESSOA_NO_COMODO:
                    msg.obj = "Pessoa no comodo";

                    break;
                case ALERTA_RISCO:
                    msg.obj = "SOCORRO!";

                    Intent alerta = new Intent(ConectaService.this, Alerta.class);
                    startActivity(alerta);

                    break;
                case SAIU_DA_CASA:
                    msg.obj = "Saiu de casa";

                    break;
                case PODE_ESTAR_NO_BANHEIRO:
                    msg.obj = "Pode estar no banheiro";

                    break;
            }

            msg.what = STATUS_STATUS;



            try {
                handler.send(msg);
            } catch (RemoteException e) {
                e.printStackTrace();
            }

        }

        // Shut down socket
        try {
            this.socket.shutdownInput();
            this.socket.shutdownOutput();
            this.socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }






    }



    private void conectaSocket(){

        this.socket = null;

        while(this.socket == null) {
            try {

                InetAddress serverAddr = InetAddress.getByName(this.ip);


                this.socket = new Socket(serverAddr, this.port);


            } catch (UnknownHostException e1) {
                e1.printStackTrace();

            } catch (IOException e1) {

                e1.printStackTrace();

            }

            if(this.socket == null){
                try {
                    Thread.sleep(5000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }








        try {
            this.stdIn = new BufferedReader(new InputStreamReader(this.socket.getInputStream()));
            this.out = new PrintWriter(this.socket.getOutputStream(), true);
            this.out.print("2");
            this.out.print(String.format("%03d", this.user.length()));
            this.out.print(this.user);



            this.out.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    private void desconectaSocket(){
        try {
            this.socket.shutdownInput();
            this.socket.shutdownOutput();
            this.socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }



    private JSONObject lerSocket(){

        JSONObject obj = null;
        message = null;
        int erro = -1;

        while(message == null) {
            erro += 1;

            try {
                message = this.stdIn.readLine();


            } catch (IOException e) {
                e.printStackTrace();

            }

            if(erro > 50){
                desconectaSocket();
                conectaSocket();
                erro = -1;
            }


        }

        try {

            obj = new JSONObject(message);


        } catch (JSONException e) {
            e.printStackTrace();
        }

        return obj;
    }




    @Override
    public void onDestroy() {
        super.onDestroy();
        try {
            this.ativo = false;
            this.socket.shutdownInput();
            this.socket.shutdownOutput();
            this.socket.close();


            Message msg = new Message();
            msg.what = this.STATUS_FINISHED;

            try {
                handler.send(msg);
            } catch (RemoteException e) {
                e.printStackTrace();
            }


        } catch (IOException e) {
            e.printStackTrace();
        }
    }


}






















