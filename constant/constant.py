import pandas as pd

UNIVERSITY_INFO = {
    'scu': ['四川大学', '985', '四川', '成都'],
    'sufe': ['上海财经大学', '211', '上海', '上海'],
    'cufe': ['中央财经大学', '211', '北京', '北京'],
    'fdu': ['复旦大学', 'C9', '上海', '上海'],
    'nju': ['南京大学', 'C9', '江苏', '南京'],
    'hit': ['哈尔滨工业大学', 'C9', '黑龙江', '哈尔滨'],
    'pku': ['北京大学', 'C9', '北京', '北京'],
    'thu': ['清华大学', 'C9', '北京', '北京'],
    'ustc': ['中国科学技术大学', 'C9', '安徽', '合肥'],
    'zju': ['浙江大学', 'C9', '浙江', '杭州'],
    'xjtu': ['西安交通大学', 'C9', '陕西', '西安'],
    'sjtu': ['上海交通大学', 'C9', '上海', '上海'],
    'cqu': ['重庆大学', '985', '重庆', '重庆'],
    'csu': ['中南大学', '985', '湖南', '长沙'],
    'HUST': ['华中科技大学', '985', '湖北', '武汉'],
    'lzu': ['兰州大学', '985', '甘肃', '兰州'],
    'uestc': ['电子科技大学', '985', '四川', '成都'],
    'bipt': ['北京石油化工学院', '二本', '北京', '北京'],
    'cuit': ['成都信息工程大学', '二本', '四川', '成都'],
    'jhu': ['江汉大学', '二本', '湖北', '武汉'],
    'jcxy': ['四川大学锦城学院', '二本', '四川', '成都'],
    'scc': ['上海海关学院', '二本', '上海', '上海'],
    'tjpu': ['天津工业大学', '二本', '天津', '天津'],
    'ytu': ['烟台大学', '二本', '山东', '烟台'],
    'wzu': ['温州大学', '二本', '浙江', '温州'],
    'ustbr': ['北京科技大学', '211', '北京', '北京'],
    'njupt': ['南京邮电大学', '211', '江苏', '南京'],
    'ncepu': ['华北电力大学', '一本', '北京', '北京'],
    'ysu': ['燕山大学', '一本', '河北', '秦皇岛'],
    'ncut': ['北方工业大学', '一本', '北京', '北京'],
    'hznu': ['杭州师范大学', '一本', '浙江', '杭州'],
    'hqu': ['华侨大学', '一本', '福建', '厦门'],
    'nku': ['南开大学', '985', '天津', '天津'],
    'scut': ['华南理工大学', '985', '广东', '广州'],
    'ouc': ['中国海洋大学', '985', '山东', '青岛'],
    'wust': ['武汉科技大学', '一本', '湖北', '武汉'],
    'cueb': ['首都经济贸易大学', '一本', '北京', '北京'],
    'hbu': ['河北大学', '一本', '河北', '保定'],
    'gzu': ['贵州大学', '211', '贵州', '贵州'],
    'cau': ['长安大学', '211', '陕西', '西安'],
    'swu': ['西南大学', '211', '重庆', '重庆'],
    'hnu1': ['海南大学', '211', '海南', '海口'],
    'zzu': ['郑州大学', '211', '河南', '郑州'],
    'shzu': ['石河子大学', '211', '新疆', '石河子'],
    'zucc': ['浙江大学城市学院', '二本', '浙江', '杭州'],
    'nwafu': ['西北农林科技大学', '985', '陕西', '咸阳'],
    'bhu': ['北京航空航天大学', '985', '北京', '北京'],
    'jlu': ['吉林大学', '985', '吉林', '长春'],
    'HNU': ['湖南大学', '985', '湖南', '长沙'],
    'bnu': ['北京师范大学', '985', '北京', '北京'],
    'sxu': ['山西大学', '一本', '山西', '太原'],
    'lnu': ['辽宁大学', '211', '辽宁', '沈阳'],
    'anu': ['安徽师范大学', '一本', '安徽', '芜湖'],
    'lmu': ['内蒙古大学', '211', '内蒙古', '呼和浩特'],
    'muc': ['中央民族大学', '985', '北京', '北京'],
    'dlut': ['大连理工大学', '985', '辽宁', '大连'],
    'ccnu': ['华中师范大学', '211', '湖北', '武汉'],
    'ecnu': ['华东师范大学', '985', '上海', '上海'],
    'tju': ['天津大学', '985', '天津', '天津'],
    'ruc': ['中国人民大学', '985', '北京', '北京'],
    'tyut': ['太原工业大学', '211', '山西', '太原'],
    'CAU': ['中国农业大学', '985', '北京', '北京'],
    'gdut': ['广东工业大学', '一本', '广东', '广州'],
    'lut': ['兰州理工大学', '二本', '甘肃', '兰州'],
    'yangtzeu': ['长江大学', '二本', '湖北', '武汉'],
    'szu': ['深圳大学', '一本', '广东', '深圳'],
    'xju': ['新疆大学', '211', '新疆', '乌鲁木齐'],
    'ynu':['云南大学', '211', '云南', '昆明'],
    'nxu':['宁夏大学', '211', '宁夏', '银川']
}

p985 = []
p211 = []
top = []
basic = []
c9 = []
print(len(UNIVERSITY_INFO))
for item in UNIVERSITY_INFO.values():
    if item[1] == '985':
        p985.append(item)
    elif item[1] == '211':
        p211.append(item)
    elif item[1] == '一本':
        top.append(item)
    elif item[1] == '二本':
        basic.append(item)
    elif item[1] == 'C9':
        c9.append(item)
print('c9:' + str(len(c9)))
print('985:' + str(len(p985)))
print('211:' + str(len(p211)))
print('一本:' + str(len(top)))
print('二本:' + str(len(basic)))


data_df = pd.DataFrame(UNIVERSITY_INFO)

COMPANY_WASTE_WORDS = ['控股', '股份', '有限公司', '有限', '公司', '集团', '（', '）', '资产管理', '通信', '集团股份',
                       '电子商务', '商城', '矿业集团', '信息产业', '发展股份', '控股集团', '(', ')',
                       '企业', '&', '综合', '管理', '咨询', '管理咨询']
