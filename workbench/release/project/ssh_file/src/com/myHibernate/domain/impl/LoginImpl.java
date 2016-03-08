package com.myHibernate.domain.impl;

import javax.annotation.Resource;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.myHibernate.bean.User;

import com.myHibernate.dao.UserDAO;
import com.myHibernate.domain.Login;

@Transactional
@Service
public class LoginImpl implements Login {
	@Resource
	private UserDAO userDao;

	public boolean login(User user) {
		return userDao.queryUser(user.getUsername(), user.getPassword()) == null ? false
				: true;
	}
}
