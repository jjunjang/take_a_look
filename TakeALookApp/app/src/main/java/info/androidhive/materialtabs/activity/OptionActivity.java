package info.androidhive.materialtabs.activity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import info.androidhive.materialtabs.R;
import info.androidhive.materialtabs.db.DbOpenHelper;

public class OptionActivity extends AppCompatActivity {
    private Toolbar toolbar;
    private DbOpenHelper mDbOpenHelper;
    Button btnReset, btnLogout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_option);

        mDbOpenHelper = new DbOpenHelper(this);
        mDbOpenHelper.open();
        mDbOpenHelper.create();

        toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        btnReset = (Button) findViewById(R.id.btnReset);
        btnLogout = (Button) findViewById(R.id.btnLogout);

        btnLogout.setOnClickListener(new View.OnClickListener() {

            public void onClick(View view) {
                Logout();
            }
        });

        btnReset.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Reset();
            }
        });

        mDbOpenHelper.close();
    }

    void Reset() {
        btnReset.setBackgroundResource(R.drawable.btn_states);
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("정말 초기화 하시겠습니까?");
        builder.setMessage("List의 모든 데이터 베이스가 초기화 됩니다");

        builder.setNegativeButton("아니오",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        Toast.makeText(getApplicationContext(),"아니오를 선택했습니다.",Toast.LENGTH_LONG).show();
                    }
                });
        builder.setPositiveButton("예",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        mDbOpenHelper.open();

                        mDbOpenHelper.resetLike();
                        mDbOpenHelper.resetHate();
                        mDbOpenHelper.resetInterest();
                        Log.d("ButtonDialog","reset 함수 성공");

                        mDbOpenHelper.close();
                        Toast.makeText(getApplicationContext(),"초기화 되었습니다.",Toast.LENGTH_LONG).show();
                    }
                });
        builder.show();
    }


    void Logout() {
        btnLogout.setBackgroundResource(R.drawable.btn_states);
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("로그아웃 하시겠습니까?");


        builder.setNegativeButton("아니오",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        Toast.makeText(getApplicationContext(),"아니오를 선택했습니다.",Toast.LENGTH_LONG).show();
                    }
                });
        builder.setPositiveButton("예",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        Toast.makeText(getApplicationContext(),"로그아웃 되었습니다.",Toast.LENGTH_LONG).show();
                        startActivity(new Intent(OptionActivity.this, LogoutActivity.class));
                    }
                });


        builder.show();
    }

}