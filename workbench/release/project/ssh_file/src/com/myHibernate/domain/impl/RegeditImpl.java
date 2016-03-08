package com.myHibernate.domain.impl;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.myHibernate.bean.User;
import com.myHibernate.dao.UserDAO;
import com.myHibernate.domain.Regedit;

@Transactional
@Service
public class RegeditImpl implements Regedit {
	@Resource
	private UserDAO userDao;
	
	public void deleteUser(User user) throws Exception {
		userDao.deleteUser(user);
	}

	public void saveUser(User user) throws Exception {
		userDao.insertUser(user);
	}

	public void updateUser(User user) throws Exception {
		userDao.updateUser(user);
	}
}
