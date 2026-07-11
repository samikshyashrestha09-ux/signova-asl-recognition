import os

image_folder = "images/train"
label_folder = "labels/train"

os.makedirs(label_folder, exist_ok=True)

classes = {
"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9,
"K":10,"L":11,"M":12,"N":13,"O":14,"P":15,"Q":16,"R":17,"S":18,"T":19,
"U":20,"V":21,"W":22,"X":23,"Y":24,"Z":25,
"0":26,"1":27,"2":28,"3":29,"4":30,"5":31,"6":32,"7":33,"8":34,"9":35
}

for img in os.listdir(image_folder):

    if img.endswith(".jpg") or img.endswith(".png"):

        parts = img.split("_")

        if len(parts) >= 3:
            label = parts[1]   # this extracts A or 0

            if label in classes:
                class_id = classes[label]

                txt_name = img.replace(".jpg",".txt").replace(".png",".txt")
                txt_path = os.path.join(label_folder, txt_name)

                with open(txt_path,"w") as f:
                    f.write(f"{class_id} 0.5 0.5 1 1")

print("Labels created successfully")