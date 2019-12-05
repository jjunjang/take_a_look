package info.androidhive.materialtabs.activity;

import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import info.androidhive.materialtabs.R;

public class LogoutActivity  extends AppCompatActivity {
    ImageView logoutImage;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_logout);
        logoutImage = (ImageView)findViewById(R.id.logoutImage);

        logoutImage.setOnClickListener(new View.OnClickListener() {

            public void onClick(View view) {
                Logout();
            }
        });
    }

    void Logout() {
        Toast.makeText(getApplicationContext(),"환영합니다.",Toast.LENGTH_LONG).show();
        startActivity(new Intent(LogoutActivity.this, MainActivity.class));
    }

}
