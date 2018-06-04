#coding=utf8
import re
import os,sys
import urllib,urllib2
import smtplib
from email.mime.text import MIMEText
from email.header import Header

timeout = 30                             # 超时时间
charset = 'utf-8'		# 请求页面的编码格式
subject = '【更新提示】'	# email 中的主题
content = ''			# email 中的内容
isRenew = False			# 是否有更新
record_file = os.path.join(sys.path[0],'record.dat')      # 记录文件
conf_file = os.path.join(sys.path[0],'conf.ini')                # 配置文件
renew_dict = {}                 # 更新记录
my_email = ''                      # 邮箱地址
my_password = ''                   # 邮箱授权码

def get_html(url,timeout=None):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }
    request = urllib2.Request(url,headers=headers)
    response = urllib2.urlopen(request,timeout=timeout)
    return response.read()

def send_email(sub,cont):
    # send email
    global my_email,my_password
    sender = my_email                   # 发送方
    if sub=='【更新提示】海大研究生招生网 有更新！':
        receiver = [my_email,'1074073420@qq.com','1505415678@qq.com','630392694@qq.com']
    elif sub=='【更新提示】青岛事业单位招聘 有更新！':
        receiver = [my_email,'1074073420@qq.com']
    elif '内蒙古大学研究生院' in sub:
        receiver = [my_email,'1074073420@qq.com','1505415678@qq.com','630392694@qq.com']
    else:
        receiver = [my_email]               # 收件方
    subject = sub                       # 邮件主题
    smtpserver = 'smtp.qq.com'          # 邮箱服务器
    username = my_email                 # 用户名
    password = my_password		# 授权码

    msg = MIMEText(cont, 'html', 'utf8')	# 设置内容
    msg['Subject'] = Header(subject, 'utf8')	# 设置主题
    msg['From'] = sender			# 设置发送方
    msg['To'] = ','.join(receiver)		# 设置接收方
    smtp = smtplib.SMTP_SSL(smtpserver,465)
    #smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

def Init():
    global renew_dict,my_email,my_password
    print '正在加载邮箱地址和授权码……'
    try:
        fp = open(conf_file,'r')
    except Exception,e:
        print '加载失败，conf.ini文件不存在'
        raise Exception,e
    lines = fp.readlines()
    my_email = lines[1].strip()     # 加载邮箱地址
    my_password = lines[3].strip()  # 加载邮箱授权码
    fp.close()

    print '正在加载更新记录……'
    # 提取更新情况记录
    try:
        fp = open(record_file,'r')
    except:
        open(record_file,'w')
        fp = open(record_file,'r')
    for line in fp:
        items = line.split(':#:')
        #print items
        key = items[0].strip()
        value = items[1].strip()
        #idx = line.find(':#:')
        #key = line[:idx].strip()
        #value = line[idx:].strip()
        renew_dict[key] = value

    fp.close()


def RenewCheck(key,src_url,des_url,pattern_str,charset):
    # 提示信息
    print '正在检查【%s】的更新状态……'%(key)

    # 检查更新
    global subject,content,isRenew,renew_dict
    host = 'http://'+src_url.split('//')[1].split('/')[0]   # 检查网站的host地址
    html = get_html(src_url,timeout).decode(charset)        # 获得页面源码

    # 解析源码
    pattern = re.compile(pattern_str,re.S)
    items = re.findall(pattern,html)

    # 清洗数据
    items = map(lambda x:x.strip(),items)

    # 输出解析结果
    title = ' '.join(items)

    # 判断是否有更新
    cur = title.encode('utf8')
    if renew_dict.has_key(key): # 判断之前有无记录
        last = renew_dict[key]
    else:
        last = None
    if cur != last or last==None:
        # 如果有更新，发送邮件提示
        isRenew = True

        # 更新记录
        renew_dict[key] = cur
        fp = open(record_file,'w')
        for item,value in renew_dict.items():
            fp.write('%s:#:%s\n'%(item,value))
        fp.close()

        print '【%s】有更新，发送邮件……'%(key)
        subject += '%s '%(key)
        content += '【%s】已经更新到【%s】，戳这里看详情：%s<br/>'%(key,cur,des_url)
    else:
        # 没有更新
        print '【%s】没有更新'%(key)


def main():
    global subject,content,isRenew
    isRenew = False

    # 提取更新情况记录
    Init()

    # 检查所有更新，并输出提示信息
    # 函数原型：
    # def RenewCheck( key,src_url,des_url,pattern_str,charset )
    # 参数介绍 :
    # key           - 检查对象，例如：西部世界、扳手少年等
    # src_url       - 检查对象的网站地址
    # des_url       - 如果有更新，提示中所指向的跳转地址
    # pattern_str   - 匹配正则表达式
    # charset       - 检查对象网站的编码
    renewObjList = [
        ('扳手少年',\
            'http://ac.qq.com/Comic/ComicInfo/id/520794',\
            'http://ac.qq.com/ComicView/index/id/520794/cid/176',\
            r'<a class="works-ft-new" href=".*?">(.*?)</a><span.*?>.*?</span>',\
            'utf8'
        ),  # 漫画：扳手少年
        
        ('飞剑问道',\
            'https://book.qidian.com/info/1010468795',\
            'http://www.booktxt.net/6_6454',\
            r'<a class="blue" href=".*?" data-eid="qd_G19" data-cid=".*?" title=".*?" target="_blank">(.*?)</a><i>.*?</i><em class="time">.*?</em>',\
            'utf8'\
        ),   # 小说：飞剑问道
        
        ('五行天',\
            'https://book.qidian.com/info/3638453',\
            'http://www.booktxt.net/1_1142/',\
            r'<a class="blue" href=".*?" data-eid="qd_G19" data-cid=".*?" title=".*?" target="_blank">(.*?)</a><i>.*?</i><em class="time">.*?</em>',\
            'utf8'\
        ),   # 小说：五行天

        ('凡人修仙传之仙界篇',\
               'https://book.qidian.com/info/1010734492',\
               'http://www.booktxt.net/4_4891/',\
                r'<a class="blue" href=".*?" data-eid="qd_G19" data-cid=".*?" title=".*?" target="_blank">(.*?)</a><i>.*?</i><em class="time">.*?</em>',\
                'utf8'\
        ),   # 小说：凡人修仙传之仙界篇

        ('伊塔之柱',\
               'https://book.qidian.com/info/1011139133',\
               'http://www.booktxt.net/5_5014/',\
                r'<a class="blue" href=".*?" data-eid="qd_G19" data-cid=".*?" title=".*?" target="_blank">(.*?)</a><i>.*?</i><em class="time">.*?</em>',\
                'utf8'\
        ),   # 小说：伊塔之柱

        ('青岛事业单位招聘',\
               'http://www.qdhrss.gov.cn/pages/wsbs/syzp/index.html',\
               'http://www.qdhrss.gov.cn/pages/wsbs/syzp/index.html',\
                r'<ul class="listbgdot_list">.*?<li><span class="time">.*?</span>.*?<div class="text"><a href=".*?">(.*?)</a></div>',\
                'gbk'\
        ),   # 公告：青岛事业单位招聘 

        ('青岛公务员招录',\
               'http://www.qdhrss.gov.cn/pages/wsbs/gwyzl/index.html',\
               'http://www.qdhrss.gov.cn/pages/wsbs/gwyzl/index.html',\
                r'<ul class="listbgdot_list">.*?<li><span class="time">.*?</span>.*?<div class="text"><a href=".*?">(.*?)</a></div>',\
                'gbk'\
        )   # 公告：青岛公务员招录
    ]

    for renewObj in renewObjList:
        try:
            RenewCheck(*renewObj)
        except Exception,e:
            print '[ERROR]:%s'%e
            continue

    if isRenew:
        send_email(subject+'有更新！',content)


if __name__ == '__main__':
    main()
    '''
    try:
        main()
    except Exception,e:
        print '[ERROR]:%s'%e

    '''
