package com.example.browser.database;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

/**
 * Created by Young on 2016/11/29.
 */

public interface IDatabase {
    /**
     * 增加
     *
     * @param    sqLiteDatabase    数据库
     * @param    tableName        表
     * @param    name    名
     * @param    url        地址
     * @param    date    日期
     */
    public boolean add(SQLiteDatabase sqLiteDatabase, String tableName, String name, String url, long date);

    /**
     * 删除
     *
     * @param    sqLiteDatabase    数据库
     * @param    tableName        表
     * @param    id        书签ID
     */
    public boolean delete(SQLiteDatabase sqLiteDatabase, String tableName, String id);

    /**
     * 删除所有
     *
     * @param    sqLiteDatabase    数据库
     * @param    tableName        表
     */
    public boolean deleteAll(SQLiteDatabase sqLiteDatabase, String tableName);

    /**
     * 修改
     *
     * @param    sqLiteDatabase    数据库
     * @param    tableName        表
     * @param    id        修改的ID
     * @param    name    修改后的名
     * @param    url        修改后的地址
     */
    public boolean modify(SQLiteDatabase sqLiteDatabase, String tableName, String id, String name, String url);

    /**
     * 获取所有
     *
     * @param    sqLiteDatabase    数据库
     * @param    tableName        表
     * @return Cursor
     */
    public Cursor getAll(SQLiteDatabase sqLiteDatabase, String tableName);

    /**
     * 查询某个书签是否存在，即查询url是否重复
     *
     * @param    tableName        表
     * @param    sqLiteDatabase    数据库
     * @param    url        地址
     */
    public boolean multiply(SQLiteDatabase sqLiteDatabase, String tableName, String url);

    /**
     * 开始事务
     * @param    readOnly    是否只读
     * @param    callback    函数回调
     * */
    void transactionAround(boolean readOnly, CallBack callback);
}