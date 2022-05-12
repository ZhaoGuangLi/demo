import ctypes
import inspect
import os
import threading
from django.http import HttpResponse
from django.shortcuts import render


def search_form(request):
    return render(request, 'lipai_api.html')


def allure_serve():
    os.system("allure serve ./lipaiapi/temp -p 8002")


def allure(request):
    t1 = threading.Thread(target=allure_serve())
    t1.start()
    return render(request, "allure_report.html")


def kill_port(port):
    result = os.popen("netstat -ano | findstr {}".format(port))
    readStr = result.readlines()
    if not readStr:
        print("没有找到你要杀死的端口")
    pids = set()
    for st in readStr:
        arr = st.split()
        pid = arr[4]
        pids.add(pid)
    for pid in pids:
        if pid != '0':
            res = os.popen("taskkill /f /pid " + pid)
            print("脚本执行成功，杀死端口=%s，进程pid=%s" % (port, pid))


# 接收请求数据
def lipai(request):
    request.encoding = 'utf-8'
    if 'p' and 'u' in request.POST and request.POST['p'] == "123456" and request.POST['u'] == "admin":
        os.system("python lipaiapi/testcase/testapi.py")
        kill_port(8002)
        return render(request, "result.html")
    else:
        message = '你输入的账号或者密码不正确'
        return HttpResponse(message)

