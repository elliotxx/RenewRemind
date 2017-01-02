# 一个 小说/番剧/漫画 更新提示脚本

## 简介
关注的 **小说/番剧/漫画** 如果有更新，立刻给你发送提示邮件。

脚本中内置了一部漫画和两部小说的更新检查。

第一次运行会发送它们的当前更新情况到你的邮箱。

你可以自行修改代码中的更新检查对象。

如果你有linux云服务器，可以用crontab设置隔一段时间就运行脚本，这样就可以24小时时时刻刻监控更新情况啦！

该脚本仅供参考。
## 如何使用
1.将项目clone到本地

```
git clone https://github.com/windcode/renewremind.git
```

2.设置email用户名和授权码

![设置email用户名和授权码](https://github.com/windcode/renewremind/raw/master/screenshots/1.png)

授权码获取方式：[什么是授权码，它又是如何设置？ - qq邮箱帮助中心](http://service.mail.qq.com/cgi-bin/help?subtype=1&&no=1001256&&id=28)

3.运行脚本

```
python renewremind/renewremind.py
```

运行脚本会检查更新情况，如果有更新，发送提示邮件给你。

初次运行会发送当前更新情况。

##注意

* 脚本默认仅支持qq邮箱。若要支持其它邮箱，请自行修改代码。
* 测试环境为linux




