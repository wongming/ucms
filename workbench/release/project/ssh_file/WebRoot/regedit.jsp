<%@page contentType="text/html;charset=GBK"%>
<html>
	<head>
		<title>Spring、Struts和Hibernate整合之用户注册</title>
	</head>
	<body>
		${msg }
		<form name="user" action="regedit.action" method="post">
			用户名
			<input type="text" name="user.username" value="${user.username }" />
			<br>
			密 码
			<input type="password" name="user.password" value="${user.password }" />
			<br>
			<input type="submit" name=”method” value="提交" />
		</form>
	</body>
</html>
