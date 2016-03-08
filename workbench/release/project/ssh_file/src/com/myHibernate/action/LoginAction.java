package com.myHibernate.action;

import javax.annotation.Resource;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Controller;

import com.myHibernate.bean.User;
import com.myHibernate.domain.Login;
import com.opensymphony.xwork2.ActionSupport;

@SuppressWarnings("serial")
@Controller("loginAction")
@Scope("prototype")
public class LoginAction extends ActionSupport {
	@Resource
	private Login login;
	private String msg;
	private User user;
	public String getMsg() {
		return msg;
	}
	public void setMsg(String msg) {
		this.msg = msg;
	}
	public User getUser() {
		return user;
	}
	public void setUser(User user) {
		this.user = user;
	}
	public String login(){
		boolean isSuccess = login.login(user);
		if(isSuccess){
			setMsg("登成功陆");
		}else{
			setMsg("登陆失败");
		}
		return "loginAfter";
	}
}
