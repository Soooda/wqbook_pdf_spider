from PIL import Image

PAGES = 320 #总页数
SPLIT = 6 #等分数
sub_image_dir = 'temp/' #爬下的子图所在的文件夹路径

def get_file_names(page_number, split=SPLIT):
    '''
    按从左到右顺序生成当前页数正确的文件名，例如[1.webp, 1 (1).webp, 1 (2).webp, ...]
    page_number: 当前页数
    split: 图片的等分数
    '''
    ret = []
    ret.append(f'{page_number}.webp')

    for i in range(1, split):
        ret.append(f'{page_number} ({i}).webp')
    
    return ret

def merge(image_list):
    '''
    将子图从左到右合并。
    image_list: 装有子图的列表，按顺序从左到右
    '''
    w = 0
    h = 0

    for image in image_list:
        w += image.size[0]
        h = max(image.size[1], h)

    ret = Image.new("RGBA", (w, h))
    width = 0
    for i in range(len(image_list)):
        ret.paste(image_list[i], (width, 0))
        width += image_list[i].size[0]

    return ret


image_list = []

for page_number in range(1, PAGES + 1):
    names = get_file_names(page_number)
    image_list.clear()

    for file_name in names:
        image_list.append(Image.open(sub_image_dir + file_name))

    merged_image = merge(image_list)
    merged_image.save(f'{page_number}.png')
