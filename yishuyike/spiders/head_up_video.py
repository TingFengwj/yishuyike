import os


def listdir(path, out_path_final):
    """
    :param path: 文件download路径
    :return: None
    """
    for file in os.listdir(path):
        file_name = file
        # print(type(file))
        file_path = os.path.join(path, file)
        # print(file_path)
        if os.path.isdir(file_path):
            target_content = []
            for video in os.listdir(file_path):
                target_content.append(video)
            out_path = u"%s\%s.mp4" % (out_path_final, file_name)  # 输出文件夹目录
            # print(out_path)
            f = open(out_path, 'wb+')
            try:
                for i in range(len(target_content)):
                    new_path = r'C:\Users\EDZ\Desktop\video\%s\%s%d.mp4' % (file_name, file_name, i)
                    print(new_path)
                    for line in open(new_path, 'rb'):
                        f.write(line)
                    f.flush()
            except:
                print('不完整的%s' % file_name)
                pass


file_dir = r"C:\Users\EDZ\Desktop\video"  # ts文件的保存路径  video文件夹需要新建,注意配置23行new_path
out_path_final = r'C:\Users\EDZ\Desktop\final'  # 最终文件输出路径：final文件夹需要新建
listdir(file_dir, out_path_final)