# coding:utf-8 
import urllib2
import re
import urlparse
import time
import codecs


class target_url_manager (object): 
    def __init__(self):
        self.target_urls=set()
        self.old_urls=set() 
    
    def add_new_url(self,i):
        self.target_urls.add('http://guba.eastmoney.com/list,szzs,f_%d.html'%i)
        return
       
        
    def add_new_urls(self,n):
        for i in range(1,n+1):
            self.add_new_url(i)
        return
        
    def has_target_url(self): 
        return len(self.target_urls)!=0
    
    def get_new_url(self):
        new_url = self.target_urls.pop()
        self.old_urls.add(new_url)
        return new_url

class find_comment(object):
    def parse(self,page_url):
       self.new_comment_urls=set()
       urls2=set()  
       html_cont=urllib2.urlopen(page_url).read()
       new_comment_urls=re.findall('/news\S+html',html_cont)
       for comment_url in new_comment_urls :
            fu_url=urlparse.urljoin(page_url,comment_url)
            urls2.add(fu_url)
       return urls2
   



class htmldownloader(object):
    def open_url(self,url):
        return urllib2.urlopen(url).read()

    def download(self,url):
        html_cont1=self.open_url(url)
        com_cont=re.compile(r'stockcodec.+zwconbtns clearfix',re.DOTALL)
        print com_cont
        cont=com_cont.search(html_cont1).group()
        return cont
       
    def find_time(self,url):
        html_cont2=self.open_url(url)
        tar_time=re.search('\d\d\d\d-\d\d-\d\d',html_cont2).group()
        return tar_time 




class output_txt(object):
     def out_txt(self,conts):
        i=0
        for cont in conts:
            i=i+1
            name= "cont%d.txt"%i
            f=codecs.open(name,'w+','utf-8')
            f.write(cont.decode('utf-8'))
            f.close()
        return 
        
class spidermain(object):
    def __init__(self):
        self.target_urls=target_url_manager()
        self.parser=find_comment()
        self.downloader=htmldownloader()
        self.outputer=output_txt()
      
    
    def craw(self,sumpage):
        conts=set()
        error_time=0
        true_time=0
        time_start=time.strftime("%Y-%m-%d",time.localtime(time.time()))
        self.target_urls.add_new_urls(sumpage)
        while self.target_urls.has_target_url():
             new_url=self.target_urls.get_new_url()
             urls2=self.parser.parse(new_url)
             for url in urls2:
                if self.downloader.find_time(url) ==  time_start :
                   cont=self.downloader.download(url)
                   print  cont
                   conts.add(cont)
                   true_time=true_time+1
                   error_time=0
                else:
                   error_time=error_time+1
                   if error_time >= 10 :
                       break
                print '%s has a sum of %d comments'%(time_start ,true_time)
                self.outputer.out_txt(conts)        
             return

      
if __name__=='__main__':
    sumpage=1
    obj_spider=spidermain()
    obj_spider.craw(sumpage)
