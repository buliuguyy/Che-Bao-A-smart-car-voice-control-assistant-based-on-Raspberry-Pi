import binascii
import serial
import serial.tools.list_ports
import time
# volatile unsigned char FPM10A_RECEICE_BUFFER[32];        //定义接收缓存区
# code unsigned char FPM10A_Pack_Head[6] = {0xEF,0x01,0xFF,0xFF,0xFF,0xFF};  //协议包头
# code unsigned char FPM10A_Get_Img[6] = {0x01,0x00,0x03,0x01,0x00,0x05};    //获得指纹图像
# code unsigned char FPM10A_Img_To_Buffer1[7]={0x01,0x00,0x04,0x02,0x01,0x00,0x08}; //将图像放入到BUFFER1
# code unsigned char FPM10A_Search[11]={0x01,0x00,0x08,0x04,0x01,0x00,0x00,0x00,0x64,0x00,0x72}; //搜索指纹搜索范围0 - 999,使用BUFFER1中的特征码搜索

def recv(serial):
    while True:
        data = serial.read_all()
        if data == '':
            continue
        else:
            break
    return data

def fp_add():
    myserial = serial.Serial('/dev/ttyUSB0', 57600, timeout=0.5)  #/dev/ttyUSB0
    if myserial.isOpen() :
        print("open success")
    else :
        print("open failed")
    while True:
        a = 'EF 01 FF FF FF FF 01 00 03 10 00 14'
        d = bytes.fromhex(a)
        myserial.write(d)
        time.sleep(1)
        data =recv(myserial)
        if data != b'' :
            data_con = str(binascii.b2a_hex(data))[20:22]
            if(data_con == '00'):
                print("注册成功")
                data_con = str(binascii.b2a_hex(data))[22:26]
                print(data_con)
                myserial.close()
                return data_con + "号用户指纹注册成功"
            elif data_con != '03':
                return "指纹注册失败"

if __name__ == '__main__':
    print(fp_add())