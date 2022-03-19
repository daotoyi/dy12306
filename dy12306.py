from splinter.browser import Browser
from time import sleep
import traceback

class Tickets(object):
    def __init__(self):
    #def __init__(self, username, passwd, order, passengers, dtime, starts, ends, seat, tictyp):
        self.username = username
        self.password = password

        self.order = 0                                  # 车次选择，0代表所有车次
        self.passengers = [u'xxx','xxx','xxx']   #多名 users = [u"张三",u"李四"]
        self.starts = cities.get(u'深圳')
        self.ends = cities.get(u'北京') 
        self.dtime = u'2020-10-23'
        
        self.periodtime = periodtime.get(u'12:00--18:00')  # value         
        self.seat = u'二等座'
        self.seattype = seattype.get(self.seat)
        self.tictyp = u'成人票'
        self.traintpye = u'GC-高铁/城际'  # value
        '''  'GC-高铁/城际':'G', 'D-动车':'D', 'Z-直达':'Z', 'T-特快':'T', 'K-快速':'K', '其他':'QT'  '''

        #self.driver_name = 'chrome'
        #self.executable_path = 'D:\Program Files (x86)\Centbrowser\CentBrowser\Application\chromedriver'
 
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.initMy_url = 'https://kyfw.12306.cn/otn/view/index.html'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'

    def login(self):    
        self.driver.visit(self.login_url)
        #self.driver.fill('loginUserDTO.user_name', self.username) #用户名密码验证码方式
        #self.driver.fill('userDTO.password', self.password)
        print('请用12306 APP扫码...')
        self.driver.find_by_text(u'扫码登录').click()
        while True:
            if self.driver.url != self.initMy_url:
                sleep(1)
            else:
                break

    def buy(self):
        #self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        self.driver = Browser()
        #self.driver = Browser(headless=True)
        self.driver.driver.set_window_size(1400, 800)
        self.login()
        self.driver.visit(self.ticket_url)
        try:
            print('开始购票...')
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
            self.driver.reload()

            if self.driver.find_by_value(str(self.periodtime)):
                self.driver.find_by_value(str(self.periodtime)).click()
            else:
                pass
            self.driver.find_by_text(str(self.traintpye)).click()
            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        self.driver.find_by_text('预订')[self.order-1].click()
                        sleep(1.5)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        for i in self.driver.find_by_text('预订'):
                            i.click()
                            sleep(1)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue

            print('开始预订...')            
            print('选择用户...')
            sleep(1)
            for user in self.passengers:
                self.driver.find_by_text(user).last.click()
                sleep(0.5)
                #if user[-1] == ')':
                    #self.driver.find_by_id('dialog_xsertcj_ok').click()
            
            print('提交订单...\n')
            sleep(1)
            for n in range(len(self.passengers)):
                print('  第%d名乘客车票信息：' % (n + 1), end='')
                print(' 乘客 %s \t %s \t %s \t %s ' % (self.passengers[n], self.traintpye, self.seat, self.tictyp))
                self.driver.find_by_value(self.seattype).click()
                sleep(1)
                self.driver.find_by_text(self.tictyp).click()
                sleep(1)
            self.driver.find_by_id('submitOrder_id').click()
            #self.driver.find_by_text('提交订单').click()
            sleep(2)
            print('\n确认选座...')
            #self.driver.find_by_id('1F').click()    # 选座 1 line F seat
            #self.driver.find_by_id('qr_submit_id').click()
            print('预订成功...')
        except Exception as e:
            print(e)

cities = {
    '成都':'%u6210%u90FD%2CCDW',
    '重庆':'%u91CD%u5E86%2CCQW',  
    '北京':'%u5317%u4EAC%2CBJP',
    '广州':'%u5E7F%u5DDE%2CGZQ', 
    '杭州':'%u676D%u5DDE%2CHZH',
    '宜昌':'%u5B9C%u660C%2CYCN',
    '郑州':'%u90D1%u5DDE%2CZZF',
    '深圳':'%u6DF1%u5733%2CSZQ',
    '西安':'%u897F%u5B89%2CXAY',
    '大连':'%u5927%u8FDE%2CDLT',
    '武汉':'%u6B66%u6C49%2CWHN',
    '上海':'%u4E0A%u6D77%2CSHH',
    '南京':'%u5357%u4EAC%2CNJH',
    '合肥':'%u5408%u80A5%2CHFH',
    '许昌':'%u8BB8%u660C%2CXCF'
}

periodtime = {
    '00:00--24:00':'00002400',  # value
    '00:00--06:00':'00000600',
    '00:00--12:00':'00001200',
    '12:00--18:00':'12001800',
    '18:00--24:00':'18002400'
} 

traintyoe = {
    'GC-高铁/城际':'G',  # value
    'D-动车':'D',
    'Z-直达':'Z',
    'T-特快':'T',
    'K-快速':'K',
    '其他':'QT'
} 

seattype = {
    '二等座':'O',
    '一等座':'M',
    '硬卧':'3',
    '硬座':'1',
    '软卧':'4',
}

if __name__ == '__main__':
    username = 'xxx'
    password = 'xxx'

    g = Tickets()
    g.buy()