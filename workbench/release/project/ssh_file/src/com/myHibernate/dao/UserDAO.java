package com.myHibernate.dao;
import com.myHibernate.bean.User;
public interface UserDAO {
    User queryUser(String name,String password);
	void insertUser(User user) throws Exception;
	void updateUser(User user);
	void deleteUser(User user);
}
