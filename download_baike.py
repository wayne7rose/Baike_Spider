import urllib.request
import os
import re


def url_open(url):
    try:
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}
        req = urllib.request.Request(url=url,headers=headers)
        html = urllib.request.urlopen(req).read()
        return html
    except:
        print('url_open出错啦！')
        return -1


# 百度百科里的明星名字--> 总相册网页
def find_pic_html(star_name):
    if star_name.encode('utf-8').isalpha():
        encode_name = star_name
    else:
        s = str(star_name.encode()).replace('\\x','%').upper()
        encode_name = s[2 : len(s)-1]

    html = url_open('https://baike.baidu.com/item/' + encode_name).decode('utf-8')
    number = re.search(encode_name + '/(\d+)/',html).group(1)
    pic_url = 'https://baike.baidu.com/pic/'+ encode_name + '/' + number
    return pic_url


# 总相册url--> 相册list（名字，网页）
def find_album_list(pic_url):
    album_list = []
    pic_html = url_open(pic_url).decode('utf-8')
    album_list = re.findall(r'album-cover" title="(.+)" nslog-type=".+" target="_blank" href="([^?]+)/?',pic_html)
    return album_list


# 根据相册url --> 图片的浏览地址list
def find_img(album_url):
    album_html = url_open(album_url).decode('utf-8')
    name = re.findall(r'title="(.+)" data-index',album_html)
    url = re.findall(r'href="(.+)">\n<img src',album_html)
    img_list = []
    for i in range(len(name)):
        img_list.append((name[i],'https://baike.baidu.com' + url[i]))
    return img_list

# 相册url --> 图片list --> 打开原图并保存   
def find_save_img(album_html,name_num):
    s = 0
    img_list = find_img(album_html)
    for each in img_list:        
        img_html = url_open(each[1]).decode('utf-8')
        img_addr = re.search(r'href="(.+)">原图',img_html).group(1)
        img = url_open(img_addr)
        name_num += 1
        s += 1
        f = open(each[0] + '_'+ str(name_num) + img_addr[-4:], 'wb')
        f.write(img)
        f.close()
        print(each[0] + '_'+ str(name_num))
    return s


def download_baike_img():
    print('我可以下载百度百科上任何明星的图册，你想要下载谁的图片？')
    while True:
        star_name = input('请输入要下载的明星的名字：')
        try:
            pic_url = find_pic_html(star_name)
            break
        except:
            print('输入名字有误，没有此人的百度百科，请重新输入...\n')
    album_list = find_album_list(pic_url)
    print('\n' + star_name + ' 一共有 '+ str(len(album_list))+' 个百度百科图册：')
    for each in album_list:
        print(each[0])

    if not os.path.exists(star_name):
        os.mkdir(star_name)
    os.chdir(star_name)
    i = len(album_list)
    total_img = 0
    album_sum_img = 0
    
    for each_album in album_list:
        album_name = each_album[0]
        album_url = 'https://baike.baidu.com'+ each_album[1]
        album_sum_img = 0
        i -= 1
        if not os.path.exists(album_name):
            os.mkdir(album_name)
        else:
            album_sum_img = len(os.listdir(album_name))
        os.chdir(album_name)
        
        print('\n' + album_name + ' 相册开始下载...') 
        total_img += find_save_img(album_url,album_sum_img)
        print(album_name + ' 相册已经下载完成，一共下载了 '+ str(total_img)+ ' 张图片，还有 '+ str(i)+' 个相册待下载')
        os.chdir(os.pardir)
 
if __name__ == '__main__':
    download_baike_img()
     
    
      

    
        
        
