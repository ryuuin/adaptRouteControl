destination = ["E3", "E4", "W3", "W4", "N3", "N4", "S3", "S4"]
destin_junction = [str(7)+str(3), str(7)+str(3), str(0)+str(3), str(0)+str(4), str(3) + str(0), str(4) + str(0),
                       str(3) + str(7), str(4) + str(7)]
destin_dic = dict.fromkeys(destination)
for k in xrange(0, 8):
            destin_dic[destination[k]] = destin_junction[k]
print(destin_dic)