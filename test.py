import csv
import time
import tushare as ts
import gc
import requests

class PairTrade:

    def __init__(self):
        print("Welcome to PairTrading System v1.0!")
        print("")
 
    def main(self):
        #initialize two lists to store the data
        store1=[]
        store2=[]
        #ask for user input to get the file needed to be compared
        stock1,length1=PairTrade.openFile()
        data1 = PairTrade.readFile(store1,stock1,length1)
        
        stock2,length2=PairTrade.openFile()
        data2 = PairTrade.readFile(store2,stock2,length2)


        if (length1>=length2):
            length = length2
            temp = data1
            data1 = data2
            data2 = temp
        else:
            length = length1

        PairTrade.result(data1,data2,length)
    
    def openFile():
        try:
            input1 = input("Please enter the file directory: ")
            fag = open("Desktop/"+input1,"r")
            ag = fag.readlines()
            length1 = len(ag)
            return ag,length1
            
        except:
            print("File unfound. Please enter again!")
            print("")
            del input1
            gc.collect()
            PairTrade.openFile()


    def readFile(store1,ag, length1):
        for i in range(length1):
            agProcessed = ag[i].split(",")
            line = []
            line.append(agProcessed[0])
            line.append(agProcessed[1])
            line.append(agProcessed[5])
            store1.append(line)
            
        return store1
        
                        
    def result(data1,data2,length1):
        
        storeFinal = []
        #priceDiff will be the price of the first input divided by the second input
        header = ["dateInt","time","priceDiff"]
        storeFinal.append(header)
        m=1
        for i in range(1,length1):
            #timeCompatibilityCheck
            

            #print("this is i!"+str(i))
            #print("this is m!"+str(m))
            
            if (data1[i][1]==data2[m][1]):
                temp = []
                temp.append(data1[i][0])
                temp.append(data1[i][1])
                temp.append(float(data2[m][2])/float(data1[i][2]))
                storeFinal.append(temp)
                if (m<=length1):
                    m+=1
                else:
                    break
                
            #when time is not compatible, check the rest and change the parameter
            else:
               flag = False
               #print("ok1")
               for x in range(i-1,length1):
                   if (data1[i][1]==data2[x][1]):
                       m=x
                       flag = True
                       break
               if (flag==True):
                temp = []
                temp.append(data1[i][0])
                temp.append(data1[i][1])
                print("/////////")
                print(str(m)+"~"+str(i))
                print(data2[m][2])
                print(data1[i][2])
                temp.append(float(data2[m][2])/float(data1[i][2]))
                storeFinal.append(temp)
                if (m<=length1):
                    m+=1
                else:
                    break

        with open("量金.csv","w",newline="") as f:
            writer = csv.writer(f)
            writer.writerows(storeFinal)

        print("Results have been genereated. Please look for the result.csv file in your home directory.")

    def searchInput():
        ticker = input("Input the ticker (e.g. AU,AG...): ")
        print("")
        print("仅当天数据可供查询！现在时间是"+time.strftime('%Y%m%d %H:%M:%S',time.localtime(time.time())))
        '''
        while True:
            date = input("Input the data (e.g.20200726): ")
            if (len(date) == 8):
                break
        date = date[2:6]
        '''
        print("")
        return ticker.upper()#, date

    #using tushare
    def mainContractCheck1(self):
        a = PairTrade.searchInput() #, b 
        token = a #+b
        print("Searching for "+token + " ...")
        pro = ts.pro_api('654a110f042ca1f24eaeee5491f21510ab9f3bd31d68c2b1f99b9107')
        df = pro.fut_holding(trade_date='20181113', symbol='C', exchange='DCE')
        df.to_csv('stock.csv',encoding="utf_8_sig")

    def mainContractCheck(self):
        a = PairTrade.searchInput() #,b
        print("Searching" + " ...")
        print(" ")

        #populate the list with tickers
        list = []
        for i in range(2001,2013):
            list.append(i)
        for i in range(2101,2113):
            list.append(i)
        test = []
        for i in list:
            test.append(a+str(i))

        #search for the result and store in a dictionary
        data = dict()
        for i in test:
            url = "http://hq.sinajs.cn/list="+ i
            response = requests.get(url)
            response.encoding = 'gbk'
            result = response.text
            #if the data exists, split and store in a csv file for later usage
            if len(result)>100:
                new = result.split(",")
                temp = []
                temp.append(new[13])
                temp.append(new[14])
                temp.append(new[15])
                data[i] = temp

        #dictionary of according name and code of future exchange
        futureExchangeName = {"沪":"SHFE","连":"DCE","郑":"CZCE"}

        #compare and get the name of the item with the largest volume of transaction
        max = 0
        maxName = " "
        for i in data.keys():
            if int(data[i][0]) > max:
                max = int(data[i][0])
                maxName = i+"."+futureExchangeName[data[i][2]]
        if maxName != " ":
            print("当日判定主力合约为: "+maxName)
            print(" ")
            print("Thank you!")      
        else:
            print("输入Ticker有误！请再次尝试")
            self.mainContractCheck()



# test the functions
pairTrade = PairTrade()
#pairTrade.main()
pairTrade.mainContractCheck()

