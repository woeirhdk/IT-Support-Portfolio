# 给Windows server配置ip
![](<../images/Pasted image 20261029145446.png>)![](<../images/Pasted image 20261029145609.png>)
![](<../images/Pasted image 20261029151240.png>)
![](<../images/Pasted image 20261029151225.png>)
# 建立域控和DNS服务器
还是在“服务器管理器”中，右上角“管理”-“添加角色和功能”
![](<../images/Pasted image 20261029153540.png>)
在“添加角色和功能向导”中点击下一页，选择“基于角色或基于功能的安装”
![](<../images/Pasted image 20261029153628.png>)
“服务器类型”选择“从服务器池中选择服务器”，选择当前计算机
![](<../images/Pasted image 20261029153733.png>)
在“服务器角色”选项卡中勾选”Active Directory域服务“
![](<../images/Pasted image 20261029161536.png>)
弹出窗口后点击添加功能
![](<../images/Pasted image 20261029153957.png>)
一直点下一步，最后点击安装，此时这个窗口就可以关闭了，它会在后台继续安装
![](<../images/Pasted image 20261029161608.png>)
回到”服务器管理器“页，右上角可见带黄色感叹号的旗帜标识，点击将其展开，点击”将此服务器提升为域控制器“
![](<../images/Pasted image 20261029155341.png>)
选择”添加新林“，输入根域名
![](<../images/Pasted image 20261029155728.png>)
配置DSRM密码
> DSRM**（Directory Services Restore Mode目录服务恢复模式）**，是Windows服务器域控制器的安全模式启动选项。DSRM允许管理员用来修复或还原修复或重建活动目录数据库。活动目录安装后，安装向导提示管理员选择一个DSRM密码。有了密码，管理员可以防护数据库后门，避免之后出问题。但是它不提供访问域或任何服务。

![](<../images/Pasted image 20261029155921.png>)
点击安装
![](<../images/Pasted image 20261029162138.png>)
安装程序走完之后会自动重启
![](<../images/Pasted image 20261029162321.png>)
