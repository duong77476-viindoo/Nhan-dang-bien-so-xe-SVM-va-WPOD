
import cv2
import numpy as np
from lib_detection import load_model, detect_lp, im2single

# Dinh nghia cac ky tu tren bien so
char_list =  '0123456789ABCDEFGHKLMNPRSTUVXYZ'

# Cau hinh tham so cho model SVM
digit_w = 30 # Kich thuoc ki tu
digit_h = 60 # Kich thuoc ki tu

 # Kích thước lớn nhất và nhỏ nhất của 1 chiều ảnh
Dmax = 608
Dmin = 288

model_svm = cv2.ml.SVM_load('svm.xml')

# Đường dẫn ảnh, các bạn đổi tên file tại đây để thử nhé
#img_path = "test/bien_vuong1.jpg"
    
# Load model LP detection
wpod_net_path = "wpod-net_update1.json"
wpod_net = load_model(wpod_net_path)

def main(img):
   
    
    # Đọc file ảnh đầu vào
    Ivehicle = cv2.imread(img)
    
    
    # Lấy tỷ lệ giữa W và H của ảnh và tìm ra chiều nhỏ nhất
    ratio = float(max(Ivehicle.shape[:2])) / min(Ivehicle.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    
    _ , LpImg, lp_type = detect_lp(wpod_net, im2single(Ivehicle), bound_dim, lp_threshold=0.5)
    
    #print(lp_type)
    
    if (len(LpImg)):
         # Chuyen doi anh bien so
        LpImg[0] = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))
        
        gray_plate = cv2.cvtColor( LpImg[0], cv2.COLOR_BGR2GRAY)
        
        blurred=cv2.GaussianBlur(gray_plate, (7, 7), 0)
        thres = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)
        
        #thres = cv2.threshold(gray_plate, 172, 255,
        #                     cv2.THRESH_BINARY_INV)[1]
        
        #thres = cv2.adaptiveThreshold(gray_plate, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10)
        
        roi_plate = LpImg[0]
        
        
        cv2.imshow("Anh bien so sau threshold", thres)
        cv2.waitKey()
        
        cv2.imshow("Bien so tim duoc", roi_plate)
        cv2.waitKey()
        if lp_type==1:#biển dọc
            plate_info = detect_plate_doc(LpImg[0])
        elif lp_type==2:
            plate_info = detect_plate_vuong(LpImg[0])
            
        # Viet bien so len anh
        cv2.putText(Ivehicle,fine_tune(plate_info),(50, 50), cv2.FONT_HERSHEY_PLAIN, 3.0, (0, 0, 255), lineType=cv2.LINE_AA)
        
        # Hien thi anh
        print("Bien so=", plate_info)
        cv2.imshow("Hinh anh output",Ivehicle)
        cv2.waitKey()
        return plate_info, LpImg[0] #trả về ảnh gốc, ảnh biển số, và thông tin biển số
        cv2.destroyAllWindows()

def detect_plate_doc(plate_img):
    plate_info = reconize_chars_from_plate(plate_img)
    return plate_info
    
def detect_plate_vuong(plate_img):
    plate_top, plate_bot = split_plate(plate_img)
        
    plate_info = reconize_chars_from_plate(plate_top) + reconize_chars_from_plate(plate_bot)
    return plate_info
    

    

#hàm tách biển số thành 2 dòng trong trường hợp biển vuông:
def split_plate(plate):
    height, width = plate.shape[:2]
    #print (image.shape)
    
    # Let's get the starting pixel coordiantes (top left of cropped top)
    start_row, start_col = int(0), int(0)
    # Let's get the ending pixel coordinates (bottom right of cropped top)
    end_row, end_col = int(height * .5), int(width)
    cropped_top = plate[start_row:end_row , start_col:end_col]
    #print (start_row, end_row) 
    #print (start_col, end_col)
    
    '''cv2.imshow("Cropped Top", cropped_top) 
    cv2.waitKey(0) 
    cv2.destroyAllWindows()'''
    
    # Let's get the starting pixel coordiantes (top left of cropped bottom)
    start_row, start_col = int(height * .5), int(0)
    # Let's get the ending pixel coordinates (bottom right of cropped bottom)
    end_row, end_col = int(height), int(width)
    cropped_bot = plate[start_row:end_row , start_col:end_col]
    #print (start_row, end_row) 
    #print (start_col, end_col)
    
    '''cv2.imshow("Cropped Bot", cropped_bot) 
    cv2.waitKey(0) 
    cv2.destroyAllWindows()'''
    return cropped_top, cropped_bot    

# Ham sap xep contour tu trai sang phai
def sort_contours(cnts):

    reverse = False
    i = 0
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return cnts



# Ham fine tune bien so, loai bo cac ki tu khong hop ly
def fine_tune(lp):
    newString = ""
    for i in range(len(lp)):
        if lp[i] in char_list:
            newString += lp[i]
    return newString


#hàm nhận diện ký tự từ biển số
def reconize_chars_from_plate(plate_img):
    roi = plate_img

    gray = cv2.cvtColor( plate_img, cv2.COLOR_BGR2GRAY)


    # Ap dung threshold de phan tach so va nen
    #binary = cv2.threshold(gray, 167, 255,
    #                    cv2.THRESH_BINARY_INV)[1]
    blurred=cv2.GaussianBlur(gray, (7, 7), 0)
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    

    # Segment kí tự
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)
    cont, _  = cv2.findContours(thre_mor, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    plate_info = ""
    for c in sort_contours(cont):
        (x, y, w, h) = cv2.boundingRect(c)
        ratio = (h/w)
        if 1.5<=ratio<=3.5: # Chon cac contour dam bao ve ratio w/h
            if h/roi.shape[0]>=0.6: # Chon cac contour cao tu 60% bien so tro len

                # Ve khung chu nhat quanh so
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Tach so va predict
                curr_num = thre_mor[y:y+h,x:x+w]
                curr_num = cv2.resize(curr_num, dsize=(digit_w, digit_h))
                _, curr_num = cv2.threshold(curr_num, 30, 255, cv2.THRESH_BINARY)
                curr_num = np.array(curr_num,dtype=np.float32)
                curr_num = curr_num.reshape(-1, digit_w * digit_h)

                # Dua vao model SVM
                result = model_svm.predict(curr_num)[1]
                result = int(result[0, 0])

                if result<=9: # Neu la so thi hien thi luon
                    result = str(result)
                else: #Neu la chu thi chuyen bang ASCII
                    result = chr(result)

                plate_info +=result
    return plate_info
def draw_contours(plate_img):
    roi = plate_img

    # Chuyen anh bien so ve gray
    gray = cv2.cvtColor( plate_img, cv2.COLOR_BGR2GRAY)


    # Ap dung threshold de phan tach so va nen
    #binary = cv2.threshold(gray, 167, 255,
    #                    cv2.THRESH_BINARY_INV)[1]
    blurred=cv2.GaussianBlur(gray, (7, 7), 0)
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    
    cv2.imshow("plate top threshold: ",binary)
    cv2.waitKey()
    

    # Segment kí tự
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)
    cont, _  = cv2.findContours(thre_mor, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) 
    
    for c in sort_contours(cont):
        (x, y, w, h) = cv2.boundingRect(c)
        ratio = (h/w)
        if 1.5<=ratio<=3.5: # Chon cac contour dam bao ve ratio w/h
            if h/roi.shape[0]>=0.6: # Chon cac contour cao tu 60% bien so tro len

                # Ve khung chu nhat quanh so
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return roi
if __name__ == "__main__":
    main()



