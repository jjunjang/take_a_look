package info.androidhive.materialtabs.activity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.database.Cursor;
import android.os.Bundle;
import android.support.v4.widget.SwipeRefreshLayout;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.util.Log;

import android.widget.ImageView;

import android.widget.Toast;

import info.androidhive.materialtabs.R;
import info.androidhive.materialtabs.db.DbOpenHelper;

public class RecommendActivity extends AppCompatActivity {
    private Toolbar toolbar;
    private DbOpenHelper mDbOpenHelper;
    private static String String_tconst;
    private static String SELECT_Tcont;
    private static int Integer_tconst;
    private static String[] SetDialogRecommend = new String[4];
    private static int[] SetImageRecommend = new int[4];

    public static int _id;
    public static String _tconst;
    public static String _titleKor;
    public static String _genres;
    public static String _averRatings;
    public static int _numVotes;
    public static String _emoNames;
    public static String _emoScore;
    public static int _startYear;
    public static int _runtimeMin;
    public static boolean CheckBoolean;

    SwipeRefreshLayout layout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_recommend);
        toolbar = (Toolbar) findViewById(R.id.toolbar);

        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        mDbOpenHelper = new DbOpenHelper(this);
        mDbOpenHelper.open();
        mDbOpenHelper.create();

        final ImageView reimg1 = (ImageView)findViewById(R.id.reimg1);
        final ImageView reimg2 = (ImageView)findViewById(R.id.reimg2);
        final ImageView reimg3 = (ImageView)findViewById(R.id.reimg3);
        final ImageView reimg4 = (ImageView)findViewById(R.id.reimg4);

        // 중복제거
        for (int i=0; i<4; i++) {
            SELECT_Tcont = SELECT_TCONST();
            Integer_tconst = getResources().getIdentifier(SELECT_Tcont, "drawable", getPackageName());
            SetDialogRecommend[i] = SELECT_Tcont; // 다이얼로그에 재활용
            SetImageRecommend[i] = Integer_tconst;
            for (int j=0; j<i; j++) {

                if (SetImageRecommend[i] == SetImageRecommend[j]) {
                    i--; // J번째에서 중복이므로 다시 돌려서 넣음
                }
            }
        }

        // RECOMMEND 이미지 4개 출력
        reimg1.setImageResource( SetImageRecommend[0] ); //tt1010012
        reimg2.setImageResource( SetImageRecommend[1] );
        reimg3.setImageResource( SetImageRecommend[2] );
        reimg4.setImageResource( SetImageRecommend[3] );

        mDbOpenHelper.close();

        // 새로고침
        layout = (SwipeRefreshLayout) findViewById(R.id.layout);
        layout.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
            @Override
            public void onRefresh() {

                // 중복제거
                for (int i=0; i<4; i++) {
                    SELECT_Tcont = SELECT_TCONST();
                    Integer_tconst = getResources().getIdentifier(SELECT_Tcont, "drawable", getPackageName());
                    SetDialogRecommend[i] = SELECT_Tcont; // 다이얼로그에 재활용
                    SetImageRecommend[i] = Integer_tconst;
                    for (int j=0; j<i; j++) {

                        if (SetImageRecommend[i] == SetImageRecommend[j]) {
                            i--; // J번째에서 중복이므로 다시 돌려서 넣음
                        }
                    }
                }

                //새로고침 작업 실행...
                reimg1.setImageResource( SetImageRecommend[0] );
                reimg2.setImageResource( SetImageRecommend[1] );
                reimg3.setImageResource( SetImageRecommend[2] );
                reimg4.setImageResource( SetImageRecommend[3] );

                layout.setRefreshing(false);

            }
        });

        reimg1.setOnClickListener(new View.OnClickListener() {

            public void onClick(View view) {
                ClickImg1();
            }
        });
        reimg2.setOnClickListener(new View.OnClickListener() {

            public void onClick(View view) {
                ClickImg2();
            }
        });
        reimg3.setOnClickListener(new View.OnClickListener() {

            public void onClick(View view) {
                ClickImg3();
            }
        });
        reimg4.setOnClickListener(new View.OnClickListener() {

            public void onClick(View view) {
                ClickImg4();
            }
        });
    }

    private String SELECT_TCONST() {
        mDbOpenHelper.READ();
        Cursor cursor = mDbOpenHelper.mDB.rawQuery(mDbOpenHelper.SQL_RECOMMEND_TCONST,null);

        if(cursor.moveToFirst()) {
            String_tconst = cursor.getString(0);
        }
        cursor.close();
        return String_tconst;
    }

    private String INSERT_Like(int i) {
        mDbOpenHelper.open();
        Cursor cursor = mDbOpenHelper.mDB.rawQuery("SELECT * FROM basic_titles where tconst = '" + SetDialogRecommend[i] + "' ", null);
        Log.d("recommend","tconst : " + SetDialogRecommend[i]);

        if(cursor.moveToFirst()) {
            _id = cursor.getInt(0);
            _tconst = cursor.getString(1);
            _titleKor = cursor.getString(2);
            _averRatings = cursor.getString(4);
        }
        Log.d("recommend","SELECT basic_titles DB");

        mDbOpenHelper.insertlistLike(_id, _tconst, _titleKor, _averRatings);
        Log.d("recommend","INSERT listLike DB : " + _titleKor);

        cursor.close();
        mDbOpenHelper.close();
        return null;
    }

    private String INSERT_Hate(int i) {
        mDbOpenHelper.open();
        Cursor cursor = mDbOpenHelper.mDB.rawQuery("SELECT * FROM basic_titles where tconst = '" + SetDialogRecommend[i] + "' ", null);
        Log.d("recommend","tconst : " + SetDialogRecommend[i]);
        cursor.moveToFirst();
        if(cursor.moveToFirst()) {
            _id = cursor.getInt(0);
            _tconst = cursor.getString(1);
            _titleKor = cursor.getString(2);
            _averRatings = cursor.getString(4);
        }
        Log.d("recommend","SELECT basic_titles DB");

        mDbOpenHelper.insertlistHate(_id, _tconst, _titleKor, _averRatings);
        Log.d("recommend","INSERT listHate DB : " + _titleKor);

        mDbOpenHelper.close();
        return null;
    }

    private String INSERT_Interest(int i) {
        mDbOpenHelper.open();
        Cursor cursor = mDbOpenHelper.mDB.rawQuery("SELECT * FROM basic_titles where tconst = '" + SetDialogRecommend[i] + "' ", null);
        Log.d("recommend","tconst : " + SetDialogRecommend[i]);
        cursor.moveToFirst();
        if(cursor.moveToFirst()) {
            _id = cursor.getInt(0);
            _tconst = cursor.getString(1);
            _titleKor = cursor.getString(2);
            _averRatings = cursor.getString(4);
        }
        Log.d("recommend","SELECT basic_titles DB");

        mDbOpenHelper.insertlistInterest(_id, _tconst, _titleKor, _averRatings);
        Log.d("recommend","INSERT listInterest DB : " + _titleKor);

        mDbOpenHelper.close();
        return null;
    }

    private boolean tconstCheckLike(int i) {
        mDbOpenHelper.open();

        Cursor cursor = mDbOpenHelper.mDB.rawQuery("SELECT * FROM listLike WHERE tconst = " + "'" + SetDialogRecommend[i] + "'", null);
        if(cursor.moveToFirst()) {
            _tconst = cursor.getString(1);
        }

        if (SetDialogRecommend[i].equals(_tconst)) {
            CheckBoolean =  false;
        }
        else {
            CheckBoolean = true;
        }
        cursor.close();
        mDbOpenHelper.close();

        return CheckBoolean;
    }

    private boolean tconstCheckHate(int i) {
        mDbOpenHelper.open();

        Cursor cursor = mDbOpenHelper.mDB.rawQuery("SELECT * FROM listHate WHERE tconst = " + "'" + SetDialogRecommend[i] + "'", null);
        if(cursor.moveToFirst()) {
            _tconst = cursor.getString(1);
        }

        if (SetDialogRecommend[i].equals(_tconst)) {
            CheckBoolean =  false;
        }
        else {
            CheckBoolean = true;
        }
        cursor.close();
        mDbOpenHelper.close();

        return CheckBoolean;
    }

    private boolean tconstCheckInterest(int i) {
        mDbOpenHelper.open();

        Cursor cursor = mDbOpenHelper.mDB.rawQuery("SELECT * FROM listInterest WHERE tconst = " + "'" + SetDialogRecommend[i] + "'", null);
        if(cursor.moveToFirst()) {
            _tconst = cursor.getString(1);
        }

        if (SetDialogRecommend[i].equals(_tconst)) {
            CheckBoolean =  false;
        }
        else {
            CheckBoolean = true;
        }
        cursor.close();
        mDbOpenHelper.close();

        return CheckBoolean;
    }

    void ClickImg1() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setPositiveButton("Like", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckLike(0) == true) {
                    INSERT_Like(0);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Like 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        }).setNegativeButton("Hate", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckHate(0) == true) {
                    INSERT_Hate(0);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Hate 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        }).setNeutralButton("Interest", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckInterest(0) == true) {
                    INSERT_Interest(0);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Interest 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        });

        final AlertDialog dialog = builder.create();

        ImageView showImage = new ImageView(this);
        showImage.setImageResource( SetImageRecommend[0] );
        dialog.setView(showImage);

        dialog.setTitle(" ");

        dialog.show();

    }

    void ClickImg2() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setPositiveButton("Like", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckLike(1) == true) {
                    INSERT_Like(1);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Like 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        }).setNegativeButton("Hate", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckHate(1) == true) {
                    INSERT_Hate(1);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Hate 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        }).setNeutralButton("Interest", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckInterest(1) == true) {
                    INSERT_Interest(1);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Interest 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        });

        final AlertDialog dialog = builder.create();

        ImageView showImage = new ImageView(this);
        showImage.setImageResource( SetImageRecommend[1] );
        dialog.setView(showImage);

        dialog.setTitle(" ");

        dialog.show();

    }

    void ClickImg3() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setPositiveButton("Like", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckLike(2) == true) {
                    INSERT_Like(2);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Like 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        }).setNegativeButton("Hate", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckHate(2) == true) {
                    INSERT_Hate(2);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Hate 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        }).setNeutralButton("Interest", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckInterest(2) == true) {
                    INSERT_Interest(2);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Interest 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        });

        final AlertDialog dialog = builder.create();

        ImageView showImage = new ImageView(this);
        showImage.setImageResource( SetImageRecommend[2] );
        dialog.setView(showImage);

        dialog.setTitle(" ");

        dialog.show();

    }

    void ClickImg4() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setPositiveButton("Like", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckLike(3) == true) {
                    INSERT_Like(3);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Like 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        }).setNegativeButton("Hate", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckHate(3) == true) {
                    INSERT_Hate(3);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Hate 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        }).setNeutralButton("Interest", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                if (tconstCheckInterest(3) == true) {
                    INSERT_Interest(3);
                    Toast.makeText(getApplicationContext(), "'" + _titleKor + "' 이(가) Interest 탭에 추가 되었습니다", Toast.LENGTH_LONG).show();
                }
                else {
                    Toast.makeText(getApplicationContext(), _titleKor + "이(가) 이미 list 탭에 있습니다!", Toast.LENGTH_LONG).show();
                }
            }
        });

        final AlertDialog dialog = builder.create();

        ImageView showImage = new ImageView(this);
        showImage.setImageResource( SetImageRecommend[3] );
        dialog.setView(showImage);

        dialog.setTitle(" ");

        dialog.show();

    }

}