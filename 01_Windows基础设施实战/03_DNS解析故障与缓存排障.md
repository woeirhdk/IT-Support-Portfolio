# 配置DNS
打开DNS管理器，”服务器管理器“-”工具“-”DNS”
![](<../images/Pasted image 20261029204255.png>)

在DNS管理器打开“正向查找区域”，右击“lab.local”-“新建主机（A或AAAA）”
>DNS域名解析中添加的各项解析记录
A记录： 将域名指向一个IPv4地址（例如：100.100.100.100），需要增加A记录
CNAME记录： 如果将域名指向一个域名，实现与被指向域名相同的访问效果，需要增加CNAME记录。这个域名一般是主机服务商提供的一个域名
MX记录： 建立电子邮箱服务，将指向邮件服务器地址，需要设置MX记录。建立邮箱时，一般会根据邮箱服务商提供的MX记录填写此记录
NS记录： 域名解析服务器记录，如果要将子域名指定某个域名服务器来解析，需要设置NS记录
TXT记录： 可任意填写，可为空。一般做一些验证记录时会使用此项，如：做SPF（反垃圾邮件）记录
AAAA记录： 将主机名（或域名）指向一个IPv6地址（例如：ff03:0:0:0:0:0:0:c1），需要添加AAAA记录
SRV记录： 添加服务记录服务器服务记录时会添加此项，SRV记录了哪台计算机提供了哪个服务。格式为：服务的名字.协议的类型（例如：_example-server._tcp）。
SOA记录： SOA叫做起始授权机构记录，NS用于标识多台域名解析服务器，SOA记录用于在众多NS记录中那一台是主服务器
PTR记录： PTR记录是A记录的逆向记录，又称做IP反查记录或指针记录，负责将IP反向解析为域名
显性URL转发记录： 将域名指向一个http(s)协议地址，访问域名时，自动跳转至目标地址。例如：将www.liuht.cn显性转发到www.itbilu.com后，访问www.liuht.cn时，地址栏显示的地址为：www.itbilu.com。
隐性UR转发记录L： 将域名指向一个http(s)协议地址，访问域名时，自动跳转至目标地址，隐性转发会隐藏真实的目标地址。例如：将www.liuht.cn显性转发到www.itbilu.com后，访问www.liuht.cn时，地址栏显示的地址仍然是：www.liuht.cn。

![](<../images/Pasted image 20261029204526.png>)
在新建主机对话框中填入名称“fileserver”，本机（域控服务器）IP，勾选“创建相关的指针（PTR）记录
![](<../images/Pasted image 20261029205352.png>)
切换到装有Windows 11的Client，手动配置其DNS为server的IP
![](<../images/Pasted image 20261029205755.png>)
Win+R打开运行面板，输入cmd，确定，在命令行界面输入ping、nslookup查询DNS服务是否建立成功
``` shell
ping fileserver.lab.local
nslookup fileserver.lab.local
```
	可以看到DNS解析成功
![](<../images/Pasted image 20261101145213.png>)
# 人为制造故障
将正向域名解析fileserver.lab.local的A记录IP从192.168.10.10改为一个同网段不可达的IP。
打开“DNS管理器”，找到A记录fileserver.lab.local，双击打开A记录属性面板，修改IP地址
![](<../images/Pasted image 20261030112705.png>)
到Client重新执行，查看变化
``` shell
ping fileserver.lab.local
nslookup fileserver.lab.local
```
发现还是能够解析，说明客户机有DNS缓存
![](<../images/Pasted image 20261101145338.png>)
可以通过查看缓存记录的操作观察现象
```shell
ipconfig /displaydns
```
![](<../images/Pasted image 20261101150000.png>)
命令行刷新DNS，并重新ping和nslookup
``` shell
ipconfig /flushdns
```
可见已无法正常访问
![](<../images/Pasted image 20261101145652.png>)

**故障现象**：Client 执行 `ping`，解析到 `192.168.10.250`，提示 `请求超时 (Request timed out)`。  
**我的第一反应（排查假设）**：

1. 是不是 DNS 解析记录被篡改了？
    
2. 是不是 Win11 缓存了旧的记录？
	
3. 是不是这个 `.250` 的 IP 根本没有机器在用，所以路由不可达？


常见问题：
1.两台虚拟机ping不通
- 解决方案：将两个防火墙都放行icmpv4后可以通信。

自己遇到的问题：
1.不知道什么时候将Server的虚拟网络改为了桥接，导致假同网段，实际并不互通。
- 解决方案：将虚拟网络改回NAT
2.**现象**：正向解析正常，但 `nslookup` 报 `DNS request timed out`。  
**排查过程**：
1. 排除网络层，确认 Ping 通。
2. 排除防火墙层，确认 UDP/TCP 53 端口入站放行。
3. 观察发现超时后依然能返回 IP 地址，定位为**反向解析（PTR）失败**。  
    **根因**：创建 A 记录时勾选了“更新相关 PTR 记录”，但服务器未配置反向查找区域，导致 `nslookup` 在查询服务器名称时静默等待超时。  
    **经验**：正向解析成功但附带超时提示，需排查反向区域配置；面试中必须清楚“入站放行+状态检测”即可满足通信，不应盲目全放行。

项目可写为：
**项目名称：中小企业 AD DS 与 DNS 基础架构部署及故障排查实战**
- 基于 VMware 及 Windows Server 独立搭建 AD DS 域控环境，并配置客户端 DNS 指向与解析。
- 针对企业内网常见的“假同网段”故障（桥接与 NAT 混用），使用 `ipconfig` 抓取真实网段与网关，定位并解决底层虚拟交换机通信异常。
- 模拟 DNS 记录篡改与 PTR 反向解析失败场景，结合 `ping`、`nslookup` 及 `ipconfig /displaydns` 等工具，梳理出“排查缓存假象 -> 验证正向解析 -> 检查反向区域”的结构化排障 SOP，沉淀为技术文档。