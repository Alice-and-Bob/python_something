#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import getopt
import sys
import re
import os
from concurrent.futures import ThreadPoolExecutor


def tcp_scan(ip, port):
    """
    TCP scan
    :param ip: target ip
    :param port: target port
    :return: null
    """
    # 建立TCP连接
    tcp_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_skt.settimeout(3)
    log = ip + "的TCP" + str(port) + "端口打开"
    flag = 1
    try:
        tcp_skt.connect((ip, int(port)))
        msg = tcp_skt.recv(4096)
        if msg is '':
            raise ValueError
        else:
            print(log)
    except ValueError as v:
        log = ip + "的TCP" + str(port) + "端口打开，但是没有可用信息"
        flag = 2
        print(log)
    except Exception as e:
        log = ip + "的TCP" + str(port) + "端口未打开"
        flag = 0
        print(log)
    finally:
        tcp_skt.close()
        result.append((port, flag, log))


def udp_scan(ip, port):
    """
    UDP scan
    :param ip: target ip
    :param port: target ip
    :return: null
    """
    udp_skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_skt.settimeout(3)
    log = ip + "的UDP" + str(port) + "端口打开"
    flag = 1
    try:
        udp_skt.sendto("114514".encode("utf-8"), (ip, port))
        # print("!!!!!!!!!!!!!!!!")
        msg, addr = udp_skt.recvfrom(4096)
        if msg is '':
            raise ValueError
        else:
            print(log)
    except ValueError as v:
        log = ip + "的UDP" + str(port) + "端口打开，但是没有可用信息"
        flag = 2
        print(log)
    except Exception as e:
        log = ip + "的UDP" + str(port) + "端口未打开"
        flag = 0
        print(log)
    finally:
        udp_skt.close()
        result.append((port, flag, log))


def main(argv):
    # print(default_ip)
    # 初始化参数默认值
    target_ip = default_ip
    scan_mod = default_socket_mod
    ports = default_ports

    # 使用命令行参数启动扫描
    try:
        opts, args = getopt.getopt(argv, "ht:m:p:P:", ["help", "target_ip=", "scan_mod=", "port=",
                                                       "ports="])
    except getopt.GetoptError:
        print('Unexpected input!')
        print("Usage: xxx.py -t <target_ip> [-m <tcp/udp>] [-p <port> / -P <ports>]")
        print("       xxx.py --target=<target_ip> [--scan_mod=<tcp/udp>] [--port=<target_port> / \
                          --ports=<target_ports>]")
        sys.exit(2)

    # 解析命令行参数
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print("Usage: xxx.py -t <target_ip> [-m <tcp/udp>] [-p <port(80)> / -P <ports(1-65535)>]")
            print("       xxx.py --target=<target_ip> [--scan_mod=<tcp/udp>] [--port=<target_port(80)> / \
                  --ports=<target_ports(1-65535)>]")
        elif opt in ('-t', '--target_ip'):
            for num in arg.split('.'):
                if re.match(r'[0-9]{3}|[0-9]{2}|[0-9]', num):  # FIXME:匹配检测不全
                    target_ip = arg
                else:
                    print('Unexpected input! Critical error, exit!')
                    sys.exit(2)
        elif opt in ('-m', '--scan_mod'):
            if arg in ('tcp', 'TCP', 'udp', 'UDP'):
                scan_mod = arg
            else:
                print('Unexpected input! Use default parameter: tcp')
        elif opt in ('-p', '--port'):  # 扫描单个端口
            ports = [int(arg)]
        elif opt in ('-P', '--ports'):  # 扫描端口段
            a, b = str(arg).split('-')
            temp = []
            a = int(a)
            b = int(b)
            for ii in range(a, b + 1):
                temp.append(int(ii))
            ports = temp


    # 检查配置，准备启动
    print("target_ip=" + str(target_ip))
    print("target_ports=" + str(ports))
    print("scan_mode=" + str(scan_mod))
    
    raw_input("Check your parameters, press any key to continue if nothing wrong")

    # 分配线程池开始多线程扫描
    with ThreadPoolExecutor() as thread_pool:
        if scan_mod in ('udp' or 'UDP'):
            for port in ports:
                thread_pool.submit(udp_scan, target_ip, port)
        else:
            for port in ports:
                thread_pool.submit(tcp_scan, target_ip, port)
  


if __name__ == '__main__':
    # 默认IP地址
    default_ip = "127.0.0.1"
    # 默认socket连接方式
    default_socket_mod = "tcp"
    # 生成默认端口范围
    default_ports = []
    for i in range(1024):
        default_ports.append(int(i))
    # 扫描结果
    result = []

    main(sys.argv[1:])
    result.sort(key=lambda result: result[0])
    print("********打开的端口******")
    for aaa in result:
        if aaa[1]:
            print(str(aaa[2]))
