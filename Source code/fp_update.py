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

def fp_update():
    myserial = serial.Serial('/dev/ttyUSB0', 57600,)  #/dev/ttyUSB0
    if myserial.isOpen() :
        print("open success")
    else :
        print("open failed")
    while True:
        a = 'EF 01 FF FF FF FF 01 00 03 11 00 15'
        d = bytes.fromhex(a)
        myserial.write(d)
        time.sleep(1)
        data =recv(myserial)
        if data != b'' :
            data_con = str(binascii.b2a_hex(data))[20:22]
            if(data_con == '00'):
                print("更新成功")
                data_con1 = str(binascii.b2a_hex(data))[22:26]
                print(data_con1)
                data_con2 = str(binascii.b2a_hex(data))[26:30]
                print("新的得分为：")
                print(data_con2)
                myserial.close()
                return data_con1 + "号用户指纹更新成功， 新指纹得分为" + data_con2
            elif data_con != '03':
                return "指纹更新失败"

if __name__ == '__main__':
    fp_update()