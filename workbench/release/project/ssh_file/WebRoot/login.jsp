<%@page contentType="text/html;charset=GBK"%>
<html>
	<head>
		<title>Spring、Struts和Hibernate整合之用户登录</title>
	</head>
	<body>
		${msg }
		<form name="user" action="login.action" method="post">
			用户名
			<input type="text" name="user.username" value="${user.username }" />
			<br>
			密 码
			<input type="password" name="user.password" value="${user.password }" />
			<br>
			<input type="submit" name="method" value="登录" />
		</form>
	</body>
</html>
