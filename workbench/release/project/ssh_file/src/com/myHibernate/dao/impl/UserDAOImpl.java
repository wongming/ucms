package com.myHibernate.dao.impl;

import java.util.List;

import javax.annotation.Resource;

import org.hibernate.HibernateException;
import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.Transaction;
import org.springframework.stereotype.Repository;

import com.myHibernate.bean.User;
import com.myHibernate.dao.UserDAO;

@Repository
public class UserDAOImpl implements UserDAO {
	@Resource
	private SessionFactory sessionFactory;
	private Transaction tr;
	private Session getSession() {
		return sessionFactory.getCurrentSession();
	}
	
	public void deleteUser(User user) {
		this.getSession().delete(user);
	}

	public void insertUser(User user) throws Exception{
		try {
			getSession().save(user);
		} catch (Exception e) {
			e.printStackTrace();
			throw new Exception("failed");
		}
	}

	public User queryUser(String name, String password) {
		List<User> users = getSession().createQuery("from User u where u.username=? and u.password=?")
								.setParameter(0, name)
								.setParameter(1, password)
								.list();
		if(users.size()!=0){
			return users.get(0);
		}
		return null;
	}

	public void updateUser(User user) {
		getSession().update(user);
	}

}
