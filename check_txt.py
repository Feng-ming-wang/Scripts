# f1 路径下文件更多一些
f1 = open("full.txt","r")
f2 = open("1.txt","r")

# 读取两个txt文件
txt1 = f1.read()
txt2 = f2.read()
# 按行的方式读取txt文件
#txt1 = f1.readline()
#txt2 = f2.readline()

# 释放两个文件进程
f1.close()
f2.close()

# 将两个文件中内容按空格分隔开
line1 = txt1.split()
line2 = txt2.split()

# 以读取方式打开 diff.txt 文件
outfile = open("diff.txt", "w")

# 循环遍历1号文件中的元素
for i in line1:
	# 查看1中文件是否在2中存在
	if i not in line2:
		outfile.write(i + "\n")
outfile.write("Above content in 1. But not in 2." + "\n")
# for j in line2:
# 	# 查看2中文件是否在1中存在
# 	if j not in line1:
# 		outfile.write(j)
# outfile.write("Above content in 2. But not in 1.")
print("核对结束")
