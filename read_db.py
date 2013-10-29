#!/usr/bin/python
import MySQLdb
HOST_IP = '172.16.140.10'
TOTAL=39
USER = 'AuditUser'
TIMES=180
PASSWD='1234'
PORT=3506
DB='audit_db'
class auditDB:
    def __init__(self,HOST_IP,USER,PASSWD,PORT,DB):
        try:
            self.conn=MySQLdb.connect(host=HOST_IP,user=USER,passwd=PASSWD,port=PORT,db=DB)
            self.cur=self.conn.cursor()
            #print "SUCCESS"
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    def read_db(self):
        self.cur.execute("SELECT net_cards.UUID,net_cards.LOG_TIME,DISK_WR_SPEED,DISK_RD_SPEED,CPU_USAGE,RX_RATE_KB,TX_RATE_KB FROM audit_db.disk_status,audit_db.audit_static_data,audit_db.net_cards where disk_status.uuid=audit_static_data.UUID and disk_status.LOGTIME=audit_static_data.LOGED_TIME and audit_static_data.UUID=net_cards.UUID and disk_status.LOGTIME=net_cards.LOG_TIME   order by disk_status.TID DESC;")
    
    def fetch_data(self,n):
        md=self.cur.fetchmany(n)
        return md

    
    def closedb(self):
        self.cur.close()
        self.conn.close()


def do_sol1(filename):
    file_handle_cpu = open('./cpuinfo.txt','w')
    file_handle_net_in = open('./net_in.txt','w')
    file_handle_net_out = open('./net_out.txt','w')
    file_handle_disk_WR = open('./disk_in.txt','w')
    file_handle_disk_RD = open('./disk_out.txt','w')
    
    mydbread = auditDB(HOST_IP,USER,PASSWD,PORT,DB)
    mydbread.read_db()
    writelist=[([0] * TOTAL) for i in range(TIMES)]
    writelist2=[([0] * TOTAL) for i in range(TIMES)]
    writelist3=[([0] * TOTAL) for i in range(TIMES)]
    writelist4=[([0] * TOTAL) for i in range(TIMES)]
    writelist5=[([0] * TOTAL) for i in range(TIMES)]
    for j in range(0,TIMES):
        md = mydbread.fetch_data(TOTAL)
        for i  in range(0,TOTAL):
            try:#lista.append(md[i][4])
                writelist[j][i]=md[i][2]
                writelist2[j][i]=md[i][3]
                writelist3[j][i]=md[i][4]
                writelist4[j][i]=md[i][5]
                writelist5[j][i]=md[i][6]
            except :
                print md
                #print i, j
    mydbread.closedb()
        
    for j in writelist:
        file_handle_disk_WR.writelines(str(j)[1:-1])
        print ".",
        file_handle_disk_WR.write('\n')


    for j in writelist2:
        file_handle_disk_RD.writelines(str(j)[1:-1])
        print ".",
        file_handle_disk_RD.write('\n')


    for j in writelist3:
        file_handle_cpu.writelines(str(j)[1:-1])
        print ".",
        file_handle_cpu.write('\n')


    for j in writelist4:
        file_handle_net_in.writelines(str(j)[1:-1])
        print ".",
        file_handle_net_in.write('\n')


    for j in writelist5:
        file_handle_net_out.writelines(str(j)[1:-1])
        print ".",
        file_handle_net_out.write('\n')
if __name__ =='__main__':
    do_sol1("./result.txt")
