import requests
import simplejson
import json
import base64

# 参考网址 https://www.52pojie.cn/thread-1016974-1-1.html
# https://console.faceplusplus.com.cn/dashboard
# 人脸替换技术
# Face++网址：[url]https://console.faceplusplus.com.cn/dashboard[/url]
# 第一步，获取人脸关键点
def find_face(imgpath):
    print("正在查找……")
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    # api_key 和 api_secret 获取地址
    # 在应用管理的 API Key 下（要先注册）
    # https://console.faceplusplus.com.cn/
    data = {"api_key": '自己申请',
            "api_secret": '自己申请',
            "image_url": imgpath, "return_landmark": 1}
    files = {"image_file": open(imgpath, "rb")}
    response = requests.post(http_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    req_dict = json.JSONDecoder().decode(req_con)
    this_json = simplejson.dumps(req_dict)

    this_json2 = simplejson.loads(this_json)
    print(this_json2)
    faces = this_json2['faces']
    list0 = faces[0]
    rectangle = list0['face_rectangle']
    # print(rectangle)
    return rectangle


# 第二步，换脸，其中图片的大小应不超过2M
# number表示换脸的相似度
def merge_face(image_url1, image_url2, image_url, number):
    ff1 = find_face(image_url1)
    ff2 = find_face(image_url2)

    rectangle1 = str(str(ff1['top']) + "," + str(ff1['left']) + "," + str(ff1['width']) + "," + str(ff1['height']))
    rectangle2 = str(ff2['top']) + "," + str(ff2['left']) + "," + str(ff2['width']) + "," + str(ff2['height'])
    print(rectangle2)
    url_add = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"
    f1 = open(image_url1, 'rb')
    f1_64 = base64.b64encode(f1.read())
    f1.close()
    f2 = open(image_url2, 'rb')
    f2_64 = base64.b64encode(f2.read())
    f2.close()

    data = {"api_key": '自己申请',
            "api_secret": '自己申请',
            "template_base64": f1_64, "template_rectangle": rectangle1,
            "merge_base64": f2_64, "merge_rectangle": rectangle2, "merge_rate": number}

    response = requests.post(url_add, data=data)
    req_con1 = response.content.decode('utf-8')
    # print(req_con1)
    req_dict = json.JSONDecoder().decode(req_con1)
    result = req_dict['result']
    imgdata = base64.b64decode(result)
    file = open(image_url, 'wb')
    file.write(imgdata)
    file.close()


image1 = r"E:\test\img03.jpg"
image2 = r"E:\test\img04.jpg"
image = r"E:\test\imgh2.jpg"
# 3 + 4 == 2

merge_face(image2, image1, image, 90)
