#coding=utf8
import re
import os,sys
import urllib,urllib2
import smtplib
from email.mime.text import MIMEText
from email.header import Header

timeout = 30                    # 超时时间
charset = 'utf-8'		# 请求页面的编码格式
subject = '【更新提示】'	# email 中的主题
content = ''			# email 中的内容
isRenew = False			# 是否有更新
record_file = os.path.join(sys.path[0],'record.dat')      # 记录文件
renew_dict = {}                 # 更新记录

def get_html(url,timeout=None):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  }
    request = urllib2.Request(url,headers=headers)
    response = urllib2.urlopen(request,timeout=timeout)
    return response.read()

def send_email(sub,cont):
    # send email to notice new WestWorld is coming
    sender = '951376975@qq.com'			# 发送方
    receiver = ['951376975@qq.com']		# 收件方
    subject = sub				# 邮件主题
    smtpserver = 'smtp.qq.com'			# 邮箱服务器
    username = '951376975@qq.com'		# 用户名
    password = 'khjpspljoawzbeij'		# 授权码

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
    global renew_dict
    print '正在加载更新记录……'
    # 提取更新情况记录
    try:
        fp = open(record_file,'r')
    except:
        open(record_file,'w')
        fp = open(record_file,'r')
    for line in fp:
        idx = line.find(' ')
        key = line[:idx].strip()
        value = line[idx:].strip()
        renew_dict[key] = value

    fp.close()


def RenewCheck(key,src_url,des_url,pattern_str,charset):
    # 参数介绍 :
    # key - 检查对象，例如：西部世界、扳手少年等
    # src_url - 检查对象的网站地址
    # des_url - 如果有更新，提示中所指向的跳转地址
    # pattern_str - 匹配正则表达式
    # charset - 检查对象网站的编码
    global subject,content,isRenew,renew_dict
    host = 'http://'+src_url.split('//')[1].split('/')[0]   # 检查网站的host地址
    html = get_html(src_url,timeout).decode(charset)        # 获得页面源码

    # 提示信息
    print '正在检查【%s】的更新状态……'%(key)

    # 解析源码
    pattern = re.compile(pattern_str,re.S)
    items = re.findall(pattern,html)

    # 输出解析结果
    title = items[0].strip()

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
            fp.write('%s %s\n'%(item,value))
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
    RenewCheck('扳手少年',\
            'http://ac.qq.com/Comic/ComicInfo/id/520794',\
            'http://ac.qq.com/ComicView/index/id/520794/cid/176',\
            r'<a class="works-ft-new" href=".*?">(.*?)</a><span.*?>.*?</span>',\
            'utf8'\
            )	# 漫画：扳手少年

    RenewCheck('斗战狂潮',\
            'http://www.qidian.com/Book/1003694333.aspx',\
            'http://www.qidian.com',\
            r'</b><a class="blue" href=".*?" data-eid="qd_G19" data-cid=".*?" title=".*?" target="_blank">(.*?)</a><i>.*?</i><em class="time">.*?</em>',\
            'utf8'\
            )   # 小说：斗战狂潮

    RenewCheck('雪鹰领主',\
            'http://www.qidian.com/Book/1003694333.aspx',\
            'http://www.qidian.com',\
            r'</b><a class="blue" href=".*?" data-eid="qd_G19" data-cid=".*?" title=".*?" target="_blank">(.*?)</a><i>.*?</i><em class="time">.*?</em>',\
            'utf8'\
            )   # 小说：斗战狂潮

    if isRenew:
        send_email(subject+'有更新！',content)


if __name__ == '__main__':
    main()

