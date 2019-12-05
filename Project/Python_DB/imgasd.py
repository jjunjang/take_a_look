from PIL import Image
import csv
t_const = []
with open('C:\\Users\\JJunJang\\Desktop\\androidImg\\tconst.tsv') as f:
    rdr = csv.reader(f, delimiter='\t')
    for i in rdr:
        t_const.append(i[0])

print(t_const)

for i in range(len(t_const)):
    source_image = t_const[i]
    image = Image.open("C:\\Users\\JJunJang\\Desktop\\androidImg\\" + t_const[i] + ".jpg").convert('RGB')
    # resize 할 이미지 사이즈

    resize_image = image.resize((750, 1200))
    # 저장할 파일 Type : JPEG, PNG 등
    # 저장할 때 Quality 수준 : 보통 95 사용
    resize_image.save("C:\\Users\\JJunJang\\Desktop\\androidImg\\reimg\\" + t_const[i] + ".jpg", "JPEG", quality=95)