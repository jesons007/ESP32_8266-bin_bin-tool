import sys


#eg:    python3 bin-to-bin.py 0x0000 bootloader.bin 0x10000 hello-world.bin 0x8000 partitions_singleapp.bin

cmd_Parameters = sys.argv  #命令行传递参数
file_num = int((cmd_Parameters.__len__()-1)/2)



if file_num != 0:

    ls_addr = cmd_Parameters[1::2]
    ls_file = cmd_Parameters[2::2]

    for i in range(file_num):
        ls_addr[i] = eval(ls_addr[i])

    # f1_name = "bootloader.bin"        
    # f2_name = "hello-world.bin"        
    # f3_name = "partitions_singleapp.bin"         

    # f1_start_addr = 0x0000          #0x0000   /root/esp8266/hello_world/build/bootloader/bootloader.bin   0~32k
    # f2_start_addr = 0x10000         #0x10000  /root/esp8266/hello_world/build/hello-world.bin             0~
    # f3_start_addr = 0x8000          #0x8000   /root/esp8266/hello_world/build/partitions_singleapp.bin    0~32k

    ls_f_handle = []    #存放文件句柄，数量等于文件个数
    for i in range(file_num):
        ls_f_handle.append(open(ls_file[i],"rb"))

    fout = open("out.bin", "wb") #二进制读取，覆盖写，不存在则创建
    fout.seek(0)

    ls_f_read = []     #存放文件读取内容
    ls_f_len  = []     #存放文件内容长度
    for i in range(file_num):
        ls_f_handle[i].seek(0)
        ls_f_read.append(ls_f_handle[i].read())
        ls_f_len.append(ls_f_read[i].__len__())

    outbin_len = max(ls_addr) + ls_f_len[ls_addr.index(max(ls_addr))]
    
    try:
        #开辟缓冲区
        buff_bin  = bytearray(outbin_len)  #文件长度
        for i in range(outbin_len):
            buff_bin[i] = 0xFF
    except:
        print("------error------:the memory is not enough!!!")
    print("the Firmware size: ",buff_bin.__len__()/1024,"KB!")

    #print(ls_addr)
    #print(ls_file)
    #print(ls_f_handle)
    #print(ls_f_len)
    #print(outbin_len)


    for i in range(file_num):
        for j in range(ls_f_len[i]):
            buff_bin[ls_addr[i] + j] = ls_f_read[i][j]
    
    try:
        fout.write(buff_bin)
        print("file write successfully!")
    except:
        print("----error----:file write failed!")

    for i in range(file_num):
        ls_f_handle[i].close()

    fout.close()
    print("The Binary file Merger OK!")
else:
    print("input file error....")
