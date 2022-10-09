import os
from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
import pandas as pd
# hostname = "0.0.0.0"
hostname = "localhost"
portnumber = 8090
publish_this = ""

class servername(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        h = open("home.html", "rb")
        self.wfile.write(h.read())
        self.wfile.write(bytes("<html><head><title>Title goes here.</title></head>/html>","utf-8"))
        
        # self.wfile.write(bytes("<html><head><title>E-commerce Site</title></head>", "utf-8"))

        # global publish_this

        try:
            
            # if self.path.endswith('/home'):
            #     self.send_header("Content-type","home/html")

            if parse_qs(urlparse(self.path).query)['price'][0] == "find":
                the_product = parse_qs(urlparse(self.path).query)['product'][0]
                the_prod = the_product.lower()
                df = pd.read_csv('Inventory.csv')
                a = df[df['Product']==the_prod]['Price']
                print (a.iloc[0])   
                self.wfile.write(bytes("<br> The amount for product %s is: #%s"%(the_product,a.iloc[0]),"utf-8"))
                

            # elif self.path.endswith('/home'):
            #     self.wfile.write("home.html","utf-8")


            elif parse_qs(urlparse(self.path).query)['product'][0] == "locate":
                the_price = int(parse_qs(urlparse(self.path).query)['price'][0])
                df = pd.read_csv('Inventory.csv')
                a = df[df['Price']==the_price]['Product']
                t = a.values
                lst = t.tolist()
                self.wfile.write(bytes("<br> \n Product(s) worth #%s are:  <br> "%(the_price),"utf-8"))
                enum = enumerate(lst,start=1)
                for i,r in enum:
                    self.wfile.write(bytes(" <br> \n %s.) %s"%(i,r),"utf-8"))    

            elif parse_qs(urlparse(self.path).query)['price'][0] == "locate" or parse_qs(urlparse(self.path).query)['product'][0] == "find":
                print ("No command")  
                self.wfile.write(bytes("Command not found","utf-8"))

            elif parse_qs(urlparse(self.path).query)['key'][0] == 'five':
            # parse_qs(urlparse(self.path).query)['key'][0] == '5':
                the_product = parse_qs(urlparse(self.path).query)['product'][0].lower()
                the_price = parse_qs(urlparse(self.path).query)['price'][0].lower()
            
            # save entire query which is a dictionary
            # df = pd.DataFrame(parse_qs(urlparse(self.path).query))
                df_new = pd.DataFrame(data = [[the_product,the_price]],columns=['Product','Price'])
                if os.path.exists('Inventory.csv'):
                    df = pd.read_csv('Inventory.csv')
                    df = pd.concat([df,df_new],axis = 0)
                    df.to_csv('Inventory.csv',index=False)
                else:    
                    df_new.to_csv('Inventory.csv',index=False)
                self.wfile.write(bytes("Product name: %s , successfully added to inventory." %(the_product),"utf-8"))

            else:  
                self.wfile.write(bytes("Access denied","utf-8"))  


            # with open('server.csv','a') as f:
            #     f.writelines(f'{the_name},{the_gender},{the_cohort},{the_food}')
        except KeyError:
           pass



if __name__ == "__main__":
    webserver = HTTPServer((hostname, portnumber),servername)
    print("Web server running as http://%s:%s" % (hostname, portnumber))

    try : 
        webserver.serve_forever()

    except KeyboardInterrupt:
        pass
webserver.server_close()    
print("Hey looks like you have stopped the server from running. Nice try")
