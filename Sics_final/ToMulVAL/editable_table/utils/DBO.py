import pymysql
import ToMulVAL.editable_table.utils.CNVD as CD
import json
import time

class DBO:

    def __init__(self,tpname):
        self.tp = tpname
        self.device = self.tp + "_device"
        self.edges = self.tp + "_edges"
        self.conn = pymysql.connect(host='39.100.88.210', user='mulval', password='mulval', database='grass', charset='utf8')
        # self.conn = pymysql.connect(host='localhost', user='root', password='', database='grass', charset='utf8')
        self.cursor = self.conn.cursor()  # 执行完毕返回的结果集默认以元组显示
        self.rs = ()
        self.dic = {}
        self.ip_name = self.cast()

    def GetAllItems(self):
        sql = "select * from "+self.device+";"
        self.cursor.execute(sql)  # 执行SQL语句
        self.rs = self.cursor.fetchall()
        return self.rs

    def GetSItems(self,sql):
        self.cursor.execute(sql)  # 执行SQL语句
        self.rs = self.cursor.fetchall()
        return self.rs

    def delete(self,ll):
        for i1 in ll:
            cmd = "delete from "+self.device+" where `NICKNAME`='" + i1 + "';"
            self.cursor.execute(cmd)
            self.conn.commit()

    def RetTabEle(self):
        sql = "select * from "+self.device+";"
        self.cursor.execute(sql)  # 执行SQL语句
        self.rs = self.cursor.fetchall()
        for i in self.rs:
            self.dic[i[1]] = json.dumps([i[12],i[10],i[11],i[15],i[14],i[2]])
        return self.dic

    def Infoupdate(self,ll):
        ts = time.time()
        for l in ll:
            if l[2][0]:
                l[2][0] = 'Y'
            else:
                l[2][0] = 'N'
            if l[2][1]:
                l[2][1] = 'Y'
            else:
                l[2][1] = 'N'
            cmd = "update "+self.device+" set `NA` = '"+l[2][0]+"' where `NICKNAME` = '"+l[1]+"';"
            self.cursor.execute(cmd)
            cmd = "update "+self.device+" set `FS` = '"+l[2][1]+"' where `NICKNAME` = '"+l[1]+"';"
            self.cursor.execute(cmd)
            cmd = "update "+self.device+" set `RR` = '"+l[3]+"' where `NICKNAME` = '" + l[1] + "';"
            self.cursor.execute(cmd)
            cmd = "update "+self.device+" set `WR` = '"+l[4]+"' where `NICKNAME` = '" + l[1] + "';"
            self.cursor.execute(cmd)
            cmd = "update "+self.device+" set `MODEL` = '"+l[5]+"' where `NICKNAME` = '" + l[1] + "';"
            self.cursor.execute(cmd)
        self.conn.commit()
        te = time.time()
        print("耗时：",te-ts,"秒")

    def CVEupdate(self,ll):
        cnvd = CD.CNVD()
        cve=''
        for l in ll:
            model = l[5]
            sql = "update "+self.device+" set `MODEL` = '" + model + "' where `NICKNAME` = '" + l[1] + "';"
            self.cursor.execute(sql)
            self.conn.commit()
            if (model != ''):
                cve = cnvd.Getcveid(model)
                if cve != '':
                    tmp = cve.split(",")[:-1]
                    rng_pro = cnvd.Get_Rng_Property(tmp)
                    self.cursor.execute("update "+self.device+" set `EXPLOIT` = '" + rng_pro[0] + "' where `NICKNAME` = '" + l[1] + "';")
                    self.cursor.execute("update "+self.device+" set `SERVICE` = '" + rng_pro[1] + "' where `NICKNAME` = '" + l[1] + "';")
            else:
                self.cursor.execute(
                    "update "+self.device+" set `EXPLOIT` = '' where `NICKNAME` = '" + l[1] + "';")
                self.cursor.execute(
                    "update "+self.device+" set `SERVICE` = '' where `NICKNAME` = '" + l[1] + "';")

            sql = "update "+self.device+" set `CVE` = '" + cve + "' where `NICKNAME` = '" + l[1] + "';"
            self.cursor.execute(sql)
            self.conn.commit()
            cve = ''
        cnvd.close()

    def cast(self):
        ips = set()
        cast = {}
        self.cursor.execute("select * from "+self.edges+";")
        self.rs = self.cursor.fetchall()
        for i1 in self.rs:
            ips.add(i1[0])
            ips.add(i1[1])
        self.cursor.execute("select IP,NICKNAME,OTHERIP from "+self.device+";")
        self.rs = self.cursor.fetchall()
        for i1 in ips:
            for i2 in self.rs:
                if(i1 == i2[0] or i2[2].find(i1)>=1):
                    cast[i1] = i2[1]
        return cast

    def GetAllByCidr(self):
        sql = "select * from " + self.device + ";"
        self.cursor.execute(sql)  # 执行SQL语句
        self.rs = self.cursor.fetchall()
        dic = {}
        r = []
        for i1 in self.rs:
            i1 = list(i1)
            tps = i1[9].split(',')
            tps.insert(0,tps[-1])
            tps = tps[:-1]
            ips = i1[13].split(',')[:-1]
            ips.insert(0,i1[1])
            for i2 in range(len(tps)):
                i1[9] = tps[i2]
                i1[1] = ips[i2]

                r.append(i1.copy())
        for i1 in r:
            try:
                if i1[9] in dic.keys():
                    dic[i1[9]].append(i1)
                else:
                    dic[i1[9]] = [i1]
            except:
                print('error')
        return dic

    def close(self):
        self.cursor.close() # 关闭光标对象
        self.conn.close() # 关闭数据库连接
