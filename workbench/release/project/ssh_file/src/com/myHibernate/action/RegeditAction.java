package com.myHibernate.action;

import javax.annotation.Resource;

import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Controller;

import com.myHibernate.bean.User;
import com.myHibernate.domain.Regedit;
import com.opensymphony.xwork2.ActionSupport;

@SuppressWarnings("serial")
@Controller("regeditAction")
@Scope("prototype")
public class RegeditAction extends ActionSupport {
	@Resource
	private Regedit regedit;
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
	public String reg(){
		try {
			regedit.saveUser(user);
			setMsg("注册成功");
		} catch (Exception e) {
			e.printStackTrace();
			setMsg("注册失败");
		}
		return "regAfter";
	}
}
