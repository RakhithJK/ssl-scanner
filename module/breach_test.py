from java.net import URL
from java.io import InputStream, InputStreamReader, BufferedReader 
from javax.net.ssl import HttpsURLConnection, HostnameVerifier, TrustManager, X509TrustManager, SSLContext, SSLSession
from java.security.cert import X509Certificate
from java.security import SecureRandom

class BreachTest :
    def __init__(self, result, host, port) :
        self._result = result
        self._host = host
        self._port = port
    
    def testPage(self, page) :

        class MyTrustManager(X509TrustManager) :
            def getAcceptedIssuers(self) :
                return None
            
            def checkClientTrusted(self, certs, auth) :
                pass
            
            def checkServerTrusted(self, certs, auth) :
                pass

        trustAllCerts = [MyTrustManager()]

        sc = SSLContext.getInstance("SSL")
        sc.init(None, trustAllCerts, SecureRandom())
        HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory())

        class MyHostnameVerifier (HostnameVerifier) :
            def verify(self, host, sess) :
                return True

        HttpsURLConnection.setDefaultHostnameVerifier(MyHostnameVerifier())

        httpsURL = 'https://%s:%s/%s' % (self._host, self._port, page)
        url = URL(httpsURL)
        conn = url.openConnection()
        conn.setRequestProperty("Accept-encoding", 'gzip,deflate,compress')
        conn.setRequestProperty("User-agent", 'https://google.com/' if 'google' not in self._host else 'https://yandex.ru/') # Use foreign referer

        #ist = conn.getInputStream()
        #isr = InputStreamReader(ist)
        #br = BufferedReader(isr)
        print("[BREACH] Received response: %d" % conn.getResponseCode())
        if conn.getContentEncoding() != None :
            print("[BREACH] Received Content-encoding: %s" % (conn.getContentEncoding()))
            return True
        return False

    def start(self, callback, helpers) : # Need HTTP service from Burp

        self._result.addResult('breach', self.testPage('/'))
        if self._result.getResult('breach') :
            # Use HTTP Compression
            self._result.addVulnerability('breach')

