from datetime import *
name = ["吴斌","赵一飞","郭茹萍","王帅宇","顾珍桢","姚鑫玉","包智超","王朔","苏永甫","谢万超","徐铮"]
email = ["18110240013@fudan.edu.cn","19110240026@fudan.edu.cn","20212010126@fudan.edu.cn","20212010031@fudan.edu.cn","20210240352@fudan.edu.cn","20210240125@fudan.edu.cn","21210240113@m.fudan.edu.cn","21210240340@m.fudan.edu.cn","22210240271@m.fudan.edu.cn","22210240325@m.fudan.edu.cn","22210240335@m.fudan.edu.cn"]

def nameemail(namelist):
    nameres = []
    emailres = []
    for a in namelist:
        if a in name:
            index = name.index(a)
            nameres.append(name[index])
            emailres.append(email[index])
    return nameres, emailres

lable = {}
lable[2] = 0
print(1)