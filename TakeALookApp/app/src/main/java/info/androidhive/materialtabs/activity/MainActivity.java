package info.androidhive.materialtabs.activity;

import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import info.androidhive.materialtabs.R;

import info.androidhive.materialtabs.db.DbOpenHelper;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private DbOpenHelper mDbOpenHelper;

    private Toolbar toolbar;
    private Button btnSimpleTabs, btnRank, btnOption, btnRecommend;

    public static int _id;
    public static String _tconst;
    public static String _titleKor;
    public static String _genres;
    public static String _averRatings;
    public static int _numVotes;
    public static String _emoNames;
    public static Float _emoScore;
    public static int _startYear;
    public static int _runtimeMin;

    public static int i;

    public static String[] RANK_tconst = new String[10];

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        mDbOpenHelper = new DbOpenHelper(this);

        btnSimpleTabs = (Button) findViewById(R.id.btnSimpleTabs);
        btnRecommend = (Button) findViewById(R.id.btnRecommend);
        btnRank = (Button) findViewById(R.id.btnRank);
        btnOption = (Button) findViewById(R.id.btnOption);

        btnSimpleTabs.setOnClickListener(this);
        btnRecommend.setOnClickListener(this);
        btnRank.setOnClickListener(this);
        btnOption.setOnClickListener(this);

    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.btnSimpleTabs:
                btnSimpleTabs.setBackgroundResource(R.drawable.btn_states);
                startActivity(new Intent(MainActivity.this, SimpleTabsActivity.class));
                break;

            case R.id.btnRecommend:
                btnRecommend.setBackgroundResource(R.drawable.btn_states);
                startActivity(new Intent(MainActivity.this, RecommendActivity.class));
                break;

            case R.id.btnRank:
                for (i=0; i<10; i++) {
                    RANK_tconst[i] = SELECT_RANK10(i);
                }
//                Toast.makeText(getApplicationContext(),RANK_tconst[0],Toast.LENGTH_LONG).show();

                btnRank.setBackgroundResource(R.drawable.btn_states);
                startActivity(new Intent(MainActivity.this, RankActivity.class));
                break;

            case R.id.btnOption:
                btnOption.setBackgroundResource(R.drawable.btn_states);
                startActivity(new Intent(MainActivity.this, OptionActivity.class));
                break;
        }
    }

    private String SELECT_RANK10(int i) {
        mDbOpenHelper.open();
        Cursor cursor = mDbOpenHelper.mDB.rawQuery("SELECT b.tconst, b.titleKor, b.emoName, b.emoScore FROM basic_titles b WHERE b.emoScore BETWEEN (select avg(b.emoScore)-7.5 from basic_titles b, listLike L where b.tconst = L.tconst and emoName='호러') and (select avg(b.emoScore)+7.5 from basic_titles b, listLike L where b.tconst = L.tconst and emoName='호러') AND emoName='호러' UNION SELECT b.tconst, b.titleKor, b.emoName, b.emoScore FROM basic_titles b WHERE b.emoScore BETWEEN (select avg(b.emoScore)-7.5 from basic_titles b, listLike L where b.tconst = L.tconst and emoName='로맨스') and(select avg(b.emoScore)+7.5 from basic_titles b, listLike L where b.tconst = L.tconst and emoName='로맨스') AND emoName='로맨스' UNION SELECT b.tconst, b.titleKor, b.emoName, b.emoScore FROM basic_titles b WHERE b.emoScore BETWEEN (select avg(b.emoScore)-7.5 from basic_titles b, listLike L where b.tconst = L.tconst and emoName='코미디') and (select avg(b.emoScore)+7.5 from basic_titles b, listLike L where b.tconst = L.tconst and emoName='코미디') AND emoName='코미디' ORDER BY emoScore desc LIMIT 10;", null);

        if(cursor.moveToPosition(i)) {
            _tconst = cursor.getString(0);
        }
        Log.d("recommend","SELECT RANK10 = tconst");

        cursor.close();
        mDbOpenHelper.close();
        return _tconst;
    }

}