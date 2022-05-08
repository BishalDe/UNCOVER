from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time


window = Tk()
window.geometry("600x400")
window.title("Speed Tracker")
window.configure(background='white')
window.resizable(0, 0)


def dowloader(search):
    PATH = "/usr/bin/chromedriver"
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    wd = webdriver.Chrome(PATH,options=option)

    def get_images_from_google(wd, delay, max_images):
        def scroll_down(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(delay)

        url = "https://www.google.com/search?q="+search+"&tbm=isch&ved=2ahUKEwjykJ779tbzAhXhgnIEHSVQBksQ2-cCegQIABAA&oq=cats&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzoHCCMQ7wMQJ1C_31NYvOJTYPbjU2gCcAB4AIABa4gBzQSSAQMzLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=7vZuYfLhOeGFytMPpaCZ2AQ&bih=817&biw=1707&rlz=1C1CHBF_enCA918CA918"
        wd.get(url)

        image_urls = set()
        skips = 0
        turns=0

        while len(image_urls) + skips < max_images:
            scroll_down(wd)

            thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

            for img in thumbnails[len(image_urls) + skips:max_images]:
                try:
                    img.click()
                    time.sleep(delay)
                except:
                    continue

                images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
                for image in images:
                    if image.get_attribute('src') in image_urls:
                        max_images += 1
                        skips += 1
                        break

                    if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                        image_urls.add(image.get_attribute('src'))
                        st=f"Found {len(image_urls)}"
                        print(st)

                        download_image("images/",image.get_attribute('src'),str(turns) + ".jpg",totalimages)
                        progress(totalimages)

                        stalab.config(text=st)
                        turns+=1

        return image_urls


    def download_image(download_path, url, file_name,totalImages):
        try:
            image_content = requests.get(url).content
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file)
            file_path = download_path + file_name

            with open(file_path, "wb") as f:
                image.save(f, "JPEG")

            print("Success")
            
        except Exception as e:
            print('FAILED -', e)
    totalimages=int(input("Enter the number of images :-"))
    urls = get_images_from_google(wd, 1, totalimages)

    wd.quit()

logo= Label(window, font=('KaiTi', 30, 'bold'), bg="white",fg='RED', text="Rudra")
logo.place(x=220, y=20)

imagelab = Label(window, font=('Aerial', 20, 'bold'), bg="white",
               foreground='Blue', text="Search For Image")
imagelab.place(x=140, y=100)



imagevalue=Entry(window, width=30,bg="silver", font=("Arial",15), fg="red")
imagevalue.place(x=90, y=150)

sreachbutton = Button(window, text="Search",bg="green",fg="white" ,cursor="hand2",font=("Arial",13),bd=0,command=lambda: dowloader(imagevalue.get()))
sreachbutton.place(x=200, y=200)

cancelbutton = Button(window, text="Cancel",bg="red",fg="white" ,cursor="hand2",font=("Arial",13),bd=0)
cancelbutton.place(x=300, y=200)

stalab = Label(window, font=('Aerial', 10, 'bold'), bg="white",
               foreground='Blue', text="")
stalab.place(x=300, y=300)

def update_progress_label():
    return f"Current Progress: {pb['value']}"


def progress(totalimages):
    if pb['value'] < totalimages:
        pb['value'] += 1
        value_label['text'] = update_progress_label()
    else:
        showinfo(message='The progress completed!')


def stop():
    pb.stop()
    value_label['text'] = update_progress_label()


# progressbar
pb = ttk.Progressbar(
    window,
    orient='horizontal',
    mode='determinate',
    length=280
)
# place the progressbar
pb.place(x=160,y=250)

# label
value_label = Label(window, text=update_progress_label())
value_label.place(x=220,y=280)
stop_button = ttk.Button(
    window,
    text='Cancel',
    command=stop
)
stop_button.place(x=260,y=320)

window.mainloop()