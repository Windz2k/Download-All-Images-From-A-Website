import requests, bs4, os, sys

class WebScraper:

    def __init__(self, user_agent):
        self.__websites = {}
        self.__user_agent = {"User-Agent": user_agent.strip()}
        self.__image_counter = 0;

    # Creating a Callable Object
    # Adds Website and Name To self.__websites dictionary
    def __call__(self, website, websiteName):
        if websiteName not in self.__websites:
            r = requests.get(website, headers=self.__user_agent)
            r.raise_for_status()
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            self.__websites[websiteName] = soup
            self.get_images(websiteName, website)

    def get_websites(self):
        return self.__websites

    # Will Run Through img tags and download them
    def get_images(self, websiteName, website):
        # rename this to be the folder where all the images are saved
        location = "myimages"
        
        if not os.path.isdir(location):
            os.mkdir(os.getcwd() + "/" + location)
        
        os.chdir(location)
        
        try:
            os.mkdir(os.getcwd() +"/" + websiteName.strip())
        except Exception:
            None
        os.chdir(os.getcwd() + "/" + websiteName.strip())
        
        soupObj = self.__websites[websiteName]
        all_images = soupObj.find_all("img")
        
        links = list(map(lambda x :x.attrs["src"] if "src" in x.attrs else None, all_images))

        # Runs Through All The Images on The Website
        # And Attempts to Download Images Will Not Work with AWS Images
        for link in links:
            
            if link is not None:
            
                with open("image%s.jpg" % (self.__image_counter), mode="wb") as file:
                    try:
                        response = None
                        if "https:" in link:
                            response = requests.get(link)
                            response.raise_for_status()
                        else:
                            response = requests.get(website+link)
                            response.raise_for_status()
                        for x in response.iter_content(100000):
                            file.write(x)
                    except IOError:
                        print(link + "\nRestricts us from downloading the image")
                        continue
                    except Exception:
                        print("There was an error with this file")
                        continue

                self.__image_counter += 1


my_user_agent = ""

w = WebScraper(my_user_agent)

answer = input("Enter Yes If You Would Like To Websrape a Website: ")
while answer.upper() == "YES":   
    name_of_website = input("Enter the name of the website: ")
    url_of_website = input("Enter the url of the website: ")
    w(url_of_website, name_of_website)
    print("\n")
    answer = input("Enter Y If You Would Like To Websrape a Website: ")
    
print("Thanks For Using My Service :) \n")
sys.exit()