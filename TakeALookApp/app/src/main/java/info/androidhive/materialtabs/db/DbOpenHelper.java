package info.androidhive.materialtabs.db;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteDatabase.CursorFactory;
import android.database.sqlite.SQLiteOpenHelper;


public class DbOpenHelper {

    private static final String DATABASE_NAME = "takealookDB.db";
    private static final int DATABASE_VERSION = 1;
    public static SQLiteDatabase mDB;
    private DatabaseHelper mDBHelper;
    private Context mCtx;

    public static final String SQL_RECOMMEND_TCONST = "SELECT tconst FROM basic_titles WHERE tconst NOT IN (SELECT tconst FROM listLike UNION SELECT tconst from listHate UNION SELECT tconst from listInterest) ORDER BY random() LIMIT 4;";

    public static final String SQL_LIST_LIKE_TCONST = "SELECT tconst FROM listLike ;";
    public static final String SQL_LIST_LIKE_TITLEKOR = "SELECT titleKor FROM listLike ;";
    public static final String SQL_LIST_LIKE_RATINGS = "SELECT averRatings FROM listLike ;";
    public static final String SQL_LIST_HATE_TCONST = "SELECT tconst FROM listHate ;";
    public static final String SQL_LIST_HATE_TITLEKOR = "SELECT titleKor FROM listHate ;";
    public static final String SQL_LIST_HATE_RATINGS = "SELECT averRatings FROM listHate ;";
    public static final String SQL_LIST_INTEREST_TCONST = "SELECT tconst FROM listInterest ;";
    public static final String SQL_LIST_INTEREST_TITLEKOR = "SELECT titleKor FROM listInterest ;";
    public static final String SQL_LIST_INTEREST_RATINGS = "SELECT averRatings FROM listInterest ;";



    private class DatabaseHelper extends SQLiteOpenHelper{

        public DatabaseHelper(Context context, String name, CursorFactory factory, int version) {
            super(context, name, factory, version);

        }

        @Override
        public void onCreate(SQLiteDatabase db){
            db.execSQL(DataBases.CreateDB._CREATE0);
            db.execSQL(DataBases.CreateDB._CREATE1);
        }

        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            db.execSQL("DROP TABLE IF EXISTS "+DataBases.CreateDB._TABLENAME0);
            onCreate(db);
        }
    }

    public DbOpenHelper(Context context){
        this.mCtx = context;
    }

    public DbOpenHelper open() throws SQLException{
        mDBHelper = new DatabaseHelper(mCtx, DATABASE_NAME, null, DATABASE_VERSION);
        mDB = mDBHelper.getWritableDatabase();
        return this;
    }

    public DbOpenHelper READ() throws SQLException{
        mDBHelper = new DatabaseHelper(mCtx, DATABASE_NAME, null, DATABASE_VERSION);
        mDB = mDBHelper.getReadableDatabase();
        return this;
    }

    public void create(){
        mDBHelper.onCreate(mDB);
    }

    public void close(){
        mDB.close();
    }

    // insert DB
    public long insertlistLike(int id, String tconst, String titleKor, String averRatings){
        ContentValues values = new ContentValues();
        values.put(DataBases.CreateDB._ID, id);
        values.put(DataBases.CreateDB.TCONST, tconst);
        values.put(DataBases.CreateDB.TITLEKOR, titleKor);
        values.put(DataBases.CreateDB.AVERRATINGS, averRatings);
        return mDB.insert(DataBases.CreateDB._TABLENAME1, null, values);
    }

    public long insertlistHate(int id, String tconst, String titleKor, String averRatings){
        ContentValues values = new ContentValues();
        values.put(DataBases.CreateDB._ID, id);
        values.put(DataBases.CreateDB.TCONST, tconst);
        values.put(DataBases.CreateDB.TITLEKOR, titleKor);
        values.put(DataBases.CreateDB.AVERRATINGS, averRatings);
        return mDB.insert(DataBases.CreateDB._TABLENAME2, null, values);
    }

    public long insertlistInterest(int id, String tconst, String titleKor, String averRatings){
        ContentValues values = new ContentValues();
        values.put(DataBases.CreateDB._ID, id);
        values.put(DataBases.CreateDB.TCONST, tconst);
        values.put(DataBases.CreateDB.TITLEKOR, titleKor);
        values.put(DataBases.CreateDB.AVERRATINGS, averRatings);
        return mDB.insert(DataBases.CreateDB._TABLENAME3, null, values);
    }

    // Update DB
    public boolean updateColumn(int id, String tconst, String genres, String averRatings, String numVotes, String titleKor, String emoName , String empScore, String startYear){
        ContentValues values = new ContentValues();
        values.put(DataBases.CreateDB.TCONST, tconst);
        values.put(DataBases.CreateDB.TITLEKOR, titleKor);
        values.put(DataBases.CreateDB.GENRES, genres);
        values.put(DataBases.CreateDB.AVERRATINGS, averRatings);
        values.put(DataBases.CreateDB.NUMVOTES, numVotes);
        values.put(DataBases.CreateDB.EMONAME, emoName);
        values.put(DataBases.CreateDB.EMOSCORE, empScore);
        values.put(DataBases.CreateDB.STARTYEAR, startYear);
        return mDB.update(DataBases.CreateDB._TABLENAME0, values, "_id=" + id, null) > 0;
    }

    // mylist 초기화 # TABLENAME0 = basic_titles, TABLENAME1 = listLike, TABLENAME2 = listHate, TABLENAME3 = listInterest,
    public void resetLike() {
        mDB.delete(DataBases.CreateDB._TABLENAME1, null, null);
    }

    public void resetHate() {
        mDB.delete(DataBases.CreateDB._TABLENAME2, null, null);
    }

    public void resetInterest() {
        mDB.delete(DataBases.CreateDB._TABLENAME3, null, null);
    }

    // Delete DB
    public boolean deleteColumn(long id){
        return mDB.delete(DataBases.CreateDB._TABLENAME0, "_id="+id, null) > 0;
    }

    // Select DB = mylist 테이블 전체
    public Cursor selectColumns(){
        return mDB.query(DataBases.CreateDB._TABLENAME1, null, null, null, null, null, null);
    }

    public void selectBasictitles(){
        mDB.query(DataBases.CreateDB._TABLENAME0, null, null, null, null, null, null);
    }

    // Delete Column FROM listLike, listHate, listInterest
    public void deleteColumnLike(String _titleKor) {
        mDB.delete(DataBases.CreateDB._TABLENAME1, "titleKor="+_titleKor, null);
    }
    public void deleteColumnHate(String _titleKor) {
        mDB.delete(DataBases.CreateDB._TABLENAME2, "titleKor="+_titleKor, null);
    }
    public void deleteColumnInterest(String _titleKor) {
        mDB.delete(DataBases.CreateDB._TABLENAME3, "titleKor="+_titleKor, null);
    }

}