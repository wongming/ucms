<%@page contentType="text/html;charset=GBK"%>
<html>
	<head>
		<title>Spring��Struts��Hibernate����֮�û�ע��</title>
	</head>
	<body>
		${msg }
		<form name="user" action="regedit.action" method="post">
			�û���
			<input type="text" name="user.username" value="${user.username }" />
			<br>
			�� ��
			<input type="password" name="user.password" value="${user.password }" />
			<br>
			<input type="submit" name=��method�� value="�ύ" />
		</form>
	</body>
</html>
