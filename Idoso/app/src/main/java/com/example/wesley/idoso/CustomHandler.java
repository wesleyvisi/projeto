package com.example.wesley.idoso;

import android.os.Handler;
import android.os.Message;


import java.io.Serializable;
import java.util.logging.LogRecord;


public class CustomHandler extends Handler {
    private AppReceiver appReceiver;
    public CustomHandler(AppReceiver receiver) {
        appReceiver = receiver;
    }

    @Override
    public void handleMessage(Message msg) {
        super.handleMessage(msg);
        appReceiver.onReceiveResult(msg);
    }


    public interface AppReceiver {
        void onReceiveResult(Message message);
    }
}
