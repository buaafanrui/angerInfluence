# -*- coding: utf-8 -*-

import urllib, urllib2, cookielib
import filer_clean
import re, string
import jieba

ctg_prb = [0.2541067456797, 0.2505163839577, 0.252065046081, 0.253311824282]
stop_word_list = ['content=', "齐", "默默地", "默然", "鬻", "高低", "骞", "马上", "首先", "饱", "风雨无阻", "颇", "顿时", "顺着", "顺", "顷刻间", "顷刻之间", "顷刻", "顷", "顶多", "靠", "非得", "非徒", "非常", "非但", "零", "难道", "难说", "难怪", "难得", "隔日", "隔夜", "随着", "随", "除非", "除此而外", "除此以外", "除此之外", "除此", "除开", "除外", "除去", "除却", "除了", "除", "陡然", "陈年", "阿", "间或", "长话短说", "长线", "长此下去", "长期以来", "鉴于", "鄙人", "都", "那里", "那边", "那样", "那末", "那时", "那儿", "那会儿", "那些", "那么样", "那么些", "那么", "那个", "那", "邋", "邈", "邃", "邂", "遽", "遵照", "遴", "遨", "遢", "遛", "遒", "遑", "遐", "遄", "逶", "逵", "逯", "逭", "逦", "逢", "逡", "通过", "逖", "逑", "逍", "迳", "迮", "迫于", "迩", "迨", "迦", "迥", "迤", "迟早", "连连", "连袂", "连日来", "连日", "连声", "连同", "连", "进而", "进来", "进去", "这里", "这边", "这样", "这时", "这就是说", "这儿", "这会儿", "这些", "这么点儿", "这么样", "这么些", "这么", "这个", "这", "还有", "还是", "还", "迕", "迓", "近来", "近年来", "近几年来", "近", "过于", "过", "迄", "达旦", "边", "较比", "较之", "较为", "较", "轰然", "转发微博", "转发", "蹇", "路经", "跟", "越是", "趁着", "趁热", "趁机", "趁早", "趁势", "趁便", "趁", "起首", "起见", "起来", "起头", "起初", "起先", "起", "赶早不赶晚", "赶快", "赶", "豁然", "谨", "谁知", "谁", "诸位", "请勿", "该当", "该", "话说", "诚然", "设若", "设使", "论说", "论", "让", "譬如", "謇", "见", "要是", "要么", "要不然", "要不是", "要不", "要", "褰", "被", "蛮", "虽说", "虽然", "虽则", "虽", "蘼", "蘩", "蘧", "蘅", "藿", "藜", "藓", "藉以", "藁", "薹", "薷", "薰", "薮", "薨", "薜", "薏", "薇", "薅", "蕹", "蕨", "蕤", "蕙", "蕈", "蕃", "蔻", "蓿", "蓼", "莫非", "莫若", "莫如", "莫不", "莫", "若非", "若是", "若", "至于", "至", "臭", "自身", "自己", "自家", "自各儿", "自从", "自个儿", "自", "腾", "能", "背靠背", "背地里", "联袂", "耷", "而论", "而言", "而是", "而已", "而外", "而后", "而又", "而况", "而且", "而", "者", "老老实实", "老是", "老大", "老", "罱", "罢了", "缕缕", "综上所述", "继而", "继之", "绝顶", "绝非", "绝对", "绝不", "绝", "给", "结果", "经过", "经常", "经", "纵然", "纵使", "纵令", "纵", "纯粹", "纯", "累次", "累年", "紧接着", "精光", "粗", "管", "简言之", "简而言之", "简直", "策略地", "等等", "等到", "等", "第", "竟然", "竟", "立马", "立时", "立地", "立刻", "立", "窃", "穷年累月", "究竟", "离", "碰巧", "砰", "矣", "着呢", "着", "看起来", "看样子", "看来", "看上去", "看", "省得", "相对而言", "皆可", "的话", "的确", "的", "白白", "略微", "略加", "略为", "略", "由此可见", "由于", "由", "甯", "甭", "甫", "用", "甚至", "甚而", "甚么", "瑟瑟", "理该", "理当", "理应", "率然", "率尔", "猛然间", "猛然", "独自", "独", "牢牢", "照着", "照", "然而", "然后", "然则", "然", "焉", "灞", "灏", "瀹", "瀣", "瀛", "瀚", "濯", "濮", "濡", "濠", "濉", "濂", "澹", "澶", "澧", "漫说", "满", "活", "沿着", "沿", "没有", "没", "沙沙", "汝", "毫无保留地", "毫无例外", "毫无", "毫不", "毕竟", "比起", "比照", "比方", "比如说", "比如", "比", "每逢", "每每", "每时每刻", "每当", "每", "毋宁", "殆", "此间", "此外", "此后", "此中", "此", "正如", "次第", "概", "梆", "格外", "根据", "某些", "某个", "某", "果真", "果然", "极端", "极度", "极大", "极力", "极其", "极了", "极为", "极", "来讲", "来自", "来着", "来看", "来得及", "来不及", "来", "权时", "本身", "本着", "本人", "本", "末末", "朝着", "朝", "望", "有的", "有关", "有些", "有", "替", "更进一步", "更加", "更为", "更", "暹", "暗自", "暗地里", "暗中", "是的", "是", "昂然", "时候", "日见", "日臻", "日益", "日渐", "日复一日", "既然", "既是", "既又", "既", "无论", "无宁", "旁人", "方能", "方才", "方", "断然", "敢情", "敢于", "敢", "敞开儿", "故而", "故此", "故意", "故", "放量", "摭", "摞", "摁", "搦", "搡", "搠", "揿", "揸", "揶", "揠", "揆", "揄", "掼", "掴", "掬", "接连不断", "接着", "接下来", "掊", "捺", "捱", "据说", "据称", "据此", "据我所知", "据悉", "据实", "据", "捭", "换言之", "换句话说", "捋", "挹", "挨门逐户", "挨门挨户", "挨着", "挨次", "挨家挨户", "挨个", "按说", "按理", "按照", "按期", "按时", "按", "拿", "拶", "拮", "拦腰", "拚", "拗", "拊", "抽冷子", "抻", "抟", "抑或", "把", "扪", "打开天窗说亮话", "打从", "打", "扑通", "才能", "才", "扌", "所以", "所", "截至", "截然", "或许", "或者", "或是", "或多或少", "或", "我们", "我", "成心", "成年累月", "成年", "慢说", "愤然", "惯常", "您", "恰逢", "恰恰相反", "恰恰", "恰巧", "恰如", "恰好", "恰似", "恐怕", "恍然", "总而言之", "总的说来", "总的来说", "总的来看", "总之", "怪不得", "怪", "急匆匆", "怕", "怎样", "怎么样", "怎么办", "怎么", "怎", "忽然", "忽地", "快要", "快", "必须", "必将", "必定", "必", "微博", "得起", "得天独厚", "得", "很少", "很多", "很", "待到", "待", "往", "彼此", "彼", "彻夜", "彘", "彖", "当着", "当真", "当然", "当庭", "当头", "当场", "当口儿", "当即", "当儿", "当中", "当下", "当", "归根结底", "归根到底", "归", "弼", "弹指之间", "弭", "弩", "弗", "弈", "开始", "开外", "廾", "并非", "并肩", "并没有", "并没", "并无", "并排", "并且", "并", "年复一年", "平素", "常言道", "常言说得好", "常言说", "常常", "常", "带", "己", "差不多", "差一点", "川流不息", "岂非", "岂止", "岂但", "岂", "屮", "屣", "屡次三番", "屡次", "屡屡", "屡", "屙", "屐", "届时", "居然", "局外", "尽量", "尽管如此", "尽管", "尽然", "尽早", "尽快", "尽心竭力", "尽心尽力", "尽如人意", "尽可能", "尽", "尻", "就算", "就此", "就是说", "就是", "就地", "就", "尥", "尢", "尚且", "尔等", "尔后", "将近", "将要", "将才", "将", "对于", "对", "寰", "寤", "宸", "宥", "定", "宕", "宓", "宄", "它们", "它", "宁肯", "宁愿", "宁可", "宁", "孱", "存心", "姑且", "妪", "妩", "妍", "妃", "如若", "如此等等", "如此", "如次", "如果", "如期", "如常", "如前所述", "如其", "如何", "如今", "如下", "如上所述", "如上", "如", "妁", "好在", "她们", "她", "奚", "奘", "奋勇", "奈", "奇", "奁", "夼", "大面儿上", "大都", "大致", "大约", "大略", "大概", "大抵", "大张旗鼓", "大家", "大大", "大多", "大凡", "大体上", "大体", "大事", "大举", "大不了", "大", "够瞧的", "多次", "多年来", "多年前", "多少", "多多益善", "多多少少", "多多", "多亏", "多", "处处", "基本上", "基本", "基于", "均", "地", "在下", "在", "图片", "图", "固然", "固", "因而", "因此", "因为", "因", "回复", "四", "嘿", "嘻", "嘛", "嘘", "嘎登", "嘎嘎", "嘎", "嗳", "嗯", "嗬", "嗡嗡", "喔唷", "喏", "喂", "喀", "啪达", "啦", "啥", "啐", "啊啊", "啊哟", "啊哈", "啊呀", "啊", "唉", "哼唷", "哼", "哪里", "哪边", "哪样", "哪怕", "哪年", "哪天", "哪儿", "哪些", "哪个", "哪", "哩", "哦", "哟", "哗啦", "哗", "哎哟", "哎呀", "哎", "哉", "哈哈哈", "哈哈", "哈", "哇", "咳", "咱们", "咱", "咫", "咦", "咚", "和", "咋", "呼啦", "呼哧", "呸", "呵", "呢", "呜呼", "呜", "呗", "呕", "呐", "呆呆地", "呃", "呀", "吱", "吧哒", "吧", "否则", "吗", "吓", "向着", "向", "后来", "同时", "同", "各自", "各种", "各式", "各位", "各个", "各", "可见", "可能", "可是", "可好", "可以", "可", "叮当", "叮咚", "叫", "只限", "只要", "只有", "只是", "另行", "另方面", "另外", "另一方面", "另一个", "另", "古来", "取道", "反过来说", "反过来", "反而", "反手", "反倒是", "反倒", "反之则", "反之亦然", "反之", "及至", "及其", "及", "又", "去", "历", "即若", "即是说", "即或", "即将", "即刻", "即便", "即使", "即令", "即", "单纯", "单单", "单", "半", "千万千万", "千万", "千", "匏", "匆匆", "勃然", "动辄", "动不动", "加以", "加之", "加上", "前者", "前后", "到目前为止", "到底", "到头来", "到头", "到处", "到了儿", "到", "别说", "别的", "别人", "别", "初", "刚才", "刚巧", "刚好", "刚", "则", "切莫", "切勿", "切切", "切不可", "切", "分期分批", "分期", "分头", "出来", "出去", "出", "凭借", "凭", "几经", "几番", "几时", "几度", "几乎", "几", "凝神", "凑巧", "况且", "决非", "决不", "冲", "冒", "再说", "再者", "内", "具体说来", "具体来说", "具体地说", "其次", "其实", "其它", "其后", "其余", "其他", "其二", "其中", "其一", "其", "关于", "共总", "共", "兮", "六", "公然", "八成", "八", "全都", "全身心", "全然", "全年", "全力", "光是", "光", "充分", "充其量", "充其极", "像", "偶而", "偶尔", "偏偏", "假若", "假如", "假使", "借此", "借以", "借", "倘若", "倘然", "倘或", "倘使", "倘", "倒是", "倒不如说", "倒不如", "倍感", "倍加", "俺们", "俺", "保险", "保管", "便", "依照", "依", "例如", "使得", "你们", "你", "作为", "何须", "何苦", "何止", "何时", "何必", "何尝", "何妨", "何处", "何况", "何乐而不为", "何", "但是", "但愿", "但", "似的", "传闻", "传说", "传", "会", "伙同", "任凭", "任何", "任", "们", "以致", "以至于", "以至", "以及", "以免", "以便", "以", "他们", "他人", "他", "从重", "从速", "从轻", "从而", "从此以后", "从此", "从来", "从未", "从早到晚", "从无到有", "从新", "从小", "从宽", "从头", "从古至今", "从古到今", "从优", "从今以后", "从中", "从严", "从不", "从", "仍然", "仍旧", "仍", "仅仅", "仅", "什么样", "什么", "人家", "人人", "亲身", "亲自", "亲眼", "亲手", "亲口", "交口", "五", "互相", "互", "云云", "于是乎", "于是", "于", "二话没说", "二话不说", "二", "了", "也罢", "也好", "也", "九", "乘隙", "乘虚", "乘胜", "乘机", "乘势", "乘", "乒", "乎", "乌乎", "之类", "之所以", "之一", "之", "么", "乃至", "乃", "举凡", "为着", "为何", "为什么", "为了", "为", "临到", "临", "串行", "个人", "个", "两者", "且", "与此同时", "与否", "与其", "与", "不限", "不问", "不迭", "不过", "不起", "不论", "不要", "不至于", "不能不", "不能", "不胜", "不经意", "不管怎样", "不管", "不知不觉", "不由得", "不独", "不特", "不然的话", "不然", "不满", "不消", "不比", "不止一次", "不止", "不曾", "不是", "不时", "不日", "不料", "不择手段", "不拘", "不成", "不惟", "不怕", "不怎么", "不必", "不得已", "不得了", "不得不", "不得", "不常", "不已", "不巧", "不少", "不对", "不定", "不妨", "不如", "不大", "不外乎", "不外", "不同", "不可抗拒", "不可开交", "不只", "不单", "不力", "不再", "不免", "不光", "不但而且", "不但", "不会", "不仅而且", "不仅仅是", "不仅仅", "不仅", "不亦乐乎", "不了", "不下", "不", "上来", "上去", "上下", "上", "三番五次", "三番两次", "三天两头", "三", "万一", "七", "一般", "一样", "一来", "一旦", "一方面", "一则", "一切", "一"]

cookie_suport = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_suport, urllib2.HTTPHandler)
urllib2.install_opener(opener)

def divide_unicode_str(str_f):
	global stop_word_set
	
	str_f_gbk = str_f.encode('gbk')
	postData = urllib.urlencode({'content':str_f_gbk})
	req = urllib2.Request(url='http://218.241.236.108:1985', data=postData)
	req.add_header('Cookie', 'foo=bar')
	req.add_header('Content-Type', 'application/x-www-form-urlencoded')
	result = urllib2.urlopen(req).read().decode('gbk').encode('utf-8').strip()
	divide_rst_arr_t = result.split(' ')
	divide_rst_arr = []
	for wd_it in divide_rst_arr_t:
		wd_it = wd_it.strip().replace('content=', '')
		if (not stop_word_set.__contains__(wd_it)) and len(wd_it) > 0:
			divide_rst_arr.append(wd_it)
	return divide_rst_arr

def divide_unicode_str_jieba(str_f):
	global stop_word_set
	divide_rst_arr_t = jieba.cut(str_f, cut_all=False)
	divide_rst_arr = []
	for wd_it in divide_rst_arr_t:
		wd_it = wd_it.encode('utf-8')
		if (not stop_word_set.__contains__(wd_it)) and len(wd_it) > 0:
			divide_rst_arr.append(wd_it)
	return divide_rst_arr

#输入进来的str_f是unicode编码
def nb_cls(str_f, div_arr=None):
	global word_map, stop_word_set
	
	if len(str_f) <= 5:
		return -1
	#divide to words
	if div_arr == None:
		divide_rst_arr = divide_unicode_str(str_f)
	else:
		divide_rst_arr = div_arr
	#start to cal
	c_prb_rst = [0.0, 0.0, 0.0, 0.0]
	if len(divide_rst_arr) > 0:
		for it_c in range(1, 4 + 1):
			for it_word in divide_rst_arr:
				if word_map.has_key(it_word):
					c_prb_rst[it_c - 1] += float(word_map[it_word][it_c - 1]) * float(ctg_prb[it_c - 1])
		if (sum(c_prb_rst)) == 0:
			return -1
		else:
			max_idx = 0
			for i in range(1, 4):
				if c_prb_rst[i] > c_prb_rst[max_idx]:
					max_idx = i
			return max_idx
	else:
		return -1
	
word_map = {} 
def rd_in_word_map(path_word_map='words_map_prior_probability_r_4.txt'):
	global word_map, stop_word_set
	
	f_in = open(path_word_map, 'r')
	for line in f_in:
		arr = line.strip().split('\t')
		word_map[arr[0]] = (float(arr[1]), float(arr[2]), float(arr[3]), float(arr[4]))
	f_in.close()
	stop_word_set = set(stop_word_list)

rd_in_word_map()
