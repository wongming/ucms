<%@page contentType="text/html;charset=GBK"%>
<html>
	<head>
		<title>Spring��Struts��Hibernate����֮�û���¼</title>
	</head>
	<body>
		${msg }
		<form name="user" action="login.action" method="post">
			�û���
			<input type="text" name="user.username" value="${user.username }" />
			<br>
			�� ��
			<input type="password" name="user.password" value="${user.password }" />
			<br>
			<input type="submit" name="method" value="��¼" />
		</form>
	</body>
</html>
