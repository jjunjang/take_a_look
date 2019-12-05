package info.androidhive.materialtabs.fragments;


import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.v4.app.ListFragment;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;
import android.widget.Toast;
import info.androidhive.materialtabs.activity.SimpleTabsActivity;
import info.androidhive.materialtabs.adapter.ListViewAdapter;
import info.androidhive.materialtabs.db.DbOpenHelper;
import info.androidhive.materialtabs.item.ListViewItem;


public class ThreeFragment extends ListFragment {

    private DbOpenHelper mDbOpenHelper;
    private static int[] SetImageList = new int[50];
    private static String[] SetTitleList = new String[50];
    private static String[] SetRatingList = new String[50];
    private static String String_tconst;
    private static String String_titleKor;
    private static String String_Rating;
    private static int Integer_tconst;
    ListViewAdapter adapter;
    public static String GETtitleKor;

    public ThreeFragment() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        mDbOpenHelper = new DbOpenHelper(getContext());
        mDbOpenHelper.open();
        mDbOpenHelper.create();

        for (int i = 0; i < 30; i++) {
            SetImageList[i] = SELECT_MYLIST_TCONST(i); // 일단 30번돌림
            SetTitleList[i] = SELECT_MYLIST_TITLE(i);
            SetRatingList[i] = SELECT_MYLIST_RATINGS(i);
        }

    }

    private int SELECT_MYLIST_TCONST(int i) {
        mDbOpenHelper.open();
        Cursor cursor = mDbOpenHelper.mDB.rawQuery(mDbOpenHelper.SQL_LIST_INTEREST_TCONST,null);

        if(cursor.moveToPosition(i)) {
            String_tconst = cursor.getString(0);
            Integer_tconst = getResources().getIdentifier(String_tconst, "drawable", getActivity().getPackageName());
        }
        cursor.close();
        return Integer_tconst;
    }



    private String SELECT_MYLIST_TITLE(int i) {
        mDbOpenHelper.open();
        Cursor cursor = mDbOpenHelper.mDB.rawQuery(mDbOpenHelper.SQL_LIST_INTEREST_TITLEKOR,null);

        if(cursor.moveToPosition(i)) {
            String_titleKor = cursor.getString(0);
        }
        cursor.close();
        return String_titleKor;
    }

    private String SELECT_MYLIST_RATINGS(int i) {
        mDbOpenHelper.open();
        Cursor cursor = mDbOpenHelper.mDB.rawQuery(mDbOpenHelper.SQL_LIST_INTEREST_RATINGS,null);

        if(cursor.moveToPosition(i)) {
            String_Rating = cursor.getString(0);
        }
        cursor.close();
        return String_Rating;
    }

    @Override
    public void onListItemClick (ListView l, View v, int position, long id) {
        // get TextView's Text.
        ListViewItem item = (ListViewItem) l.getItemAtPosition(position) ;

        String titleStr = item.getTitle() ;
        String descStr = item.getDesc() ;
        Drawable iconDrawable = item.getIcon() ;

        GETtitleKor = "'" + titleStr + "'";

        // TODO : use item data.
        AlertDialog.Builder builder = new AlertDialog.Builder(getContext());
        builder.setTitle("삭제하시겠습니까?");
        builder.setMessage(titleStr+" 을(를) List 에서 삭제 합니다.");

        builder.setNegativeButton("아니오",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        Toast.makeText(getActivity(),"아니오를 선택했습니다.",Toast.LENGTH_LONG).show();
                    }
                });
        builder.setPositiveButton("예",
                new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        mDbOpenHelper.open();

                        mDbOpenHelper.deleteColumnInterest(GETtitleKor);

                        mDbOpenHelper.close();
                        Toast.makeText(getActivity(),GETtitleKor + " 이(가) 삭제 되었습니다.",Toast.LENGTH_LONG).show();

                        adapter.notifyDataSetChanged();Log.d("OneFragment","Delete titleKor : " + GETtitleKor);
                        Intent re = new Intent(getContext(), SimpleTabsActivity.class);
                        startActivity(re);

                    }
                });

        builder.show();
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        // Adapter 생성 및 Adapter 지정.
        adapter = new ListViewAdapter() ;
        setListAdapter(adapter) ;

        mDbOpenHelper.open();
        Cursor cursor = mDbOpenHelper.mDB.rawQuery(mDbOpenHelper.SQL_LIST_INTEREST_TCONST,null);

        int i=0;
        while(cursor.moveToNext()) {

            adapter.addItem(ContextCompat.getDrawable(getActivity(), SetImageList[i]),
                    SetTitleList[i], "평점 : "+ SetRatingList[i]);
            i++;
        }

        return super.onCreateView(inflater, container, savedInstanceState);
    }

}