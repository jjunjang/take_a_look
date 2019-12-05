package info.androidhive.materialtabs.activity;

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import info.androidhive.materialtabs.R;

public class RankActivity extends AppCompatActivity {

    private Toolbar toolbar;
    private static int[] RankImg = new int[10];

    ImageView Rankimg1, Rankimg2, Rankimg3, Rankimg4, Rankimg5, Rankimg6, Rankimg7, Rankimg8, Rankimg9, Rankimg10;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_rank);
        toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        Rankimg1 = (ImageView)findViewById(R.id.Rankimg1);
        Rankimg2 = (ImageView)findViewById(R.id.Rankimg2);
        Rankimg3 = (ImageView)findViewById(R.id.Rankimg3);
        Rankimg4 = (ImageView)findViewById(R.id.Rankimg4);
        Rankimg5 = (ImageView)findViewById(R.id.Rankimg5);
        Rankimg6 = (ImageView)findViewById(R.id.Rankimg6);
        Rankimg7 = (ImageView)findViewById(R.id.Rankimg7);
        Rankimg8 = (ImageView)findViewById(R.id.Rankimg8);
        Rankimg9 = (ImageView)findViewById(R.id.Rankimg9);
        Rankimg10 = (ImageView)findViewById(R.id.Rankimg10);

        for (int i=0; i<10; i++) {
            RankImg[i] = getResources().getIdentifier(MainActivity.RANK_tconst[i], "drawable", getPackageName());
        }

        Rankimg1.setImageResource( RankImg[0] );
        Rankimg2.setImageResource( RankImg[1] );
        Rankimg3.setImageResource( RankImg[2] );
        Rankimg4.setImageResource( RankImg[3] );
        Rankimg5.setImageResource( RankImg[4] );
        Rankimg6.setImageResource( RankImg[5] );
        Rankimg7.setImageResource( RankImg[6] );
        Rankimg8.setImageResource( RankImg[7] );
        Rankimg9.setImageResource( RankImg[8] );
        Rankimg10.setImageResource( RankImg[9] );
    }

    /*View.OnClickListener clickListener = new View.OnClickListener() {
        public void onClick(View v) {
            switch (v.getId()) {
                case R.id.Rankimg1:
                    Toast.makeText(getApplicationContext(), MainActivity.RANK_tconst[1], Toast.LENGTH_LONG).show();
                    break;
                case R.id.Rankimg2:
                    Toast.makeText(getApplicationContext(), "DSA", Toast.LENGTH_LONG).show();
                    break;
                case R.id.Rankimg3:
                    Toast.makeText(getApplicationContext(), "DSA", Toast.LENGTH_LONG).show();
                    break;
                case R.id.Rankimg4:
                    Toast.makeText(getApplicationContext(), "DSA", Toast.LENGTH_LONG).show();
                    break;
                case R.id.Rankimg5:
                    Toast.makeText(getApplicationContext(), "DSA", Toast.LENGTH_LONG).show();
                    break;
                case R.id.Rankimg6:
                    Toast.makeText(getApplicationContext(), "DSA", Toast.LENGTH_LONG).show();
                    break;
                case R.id.Rankimg7:
                    Toast.makeText(getApplicationContext(), "DSA", Toast.LENGTH_LONG).show();
                    break;
                case R.id.Rankimg8:
                    Toast.makeText(getApplicationContext(), "DSA", Toast.LENGTH_LONG).show();
                    break;
                case R.id.Rankimg9:
                    Toast.makeText(getApplicationContext(), "DSA", Toast.LENGTH_LONG).show();
                    break;
                case R.id.Rankimg10:
                    Toast.makeText(getApplicationContext(), "DSA", Toast.LENGTH_LONG).show();
                    break;
            }
        }
    };*/
}