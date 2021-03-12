#coding=utf-8
import string, re
import cn_t_2_s

rep_list = ['content=', "转发微博", "", "¤", "§", "¨", "°", "±", "·", "×", "÷", "ˉ", "—", "——", "‖", "‘", "’", "“", "”", "…", "‰", "′", "″", "※", "℃", "№", "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", "Ⅺ", "Ⅻ", "←", "↑", "→", "↓", "∏", "∑", "√", "∠", "∥", "∧", "∨", "∩", "∪", "∫", "∴", "∵", "∶ǎ", "∷", "∽", "≈", "≌", "≠", "≡", "≤", "≥", "≯", "⊙", "⊥", "⌒", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", "⑴", "⑵", "⑶", "⑷", "⑸", "⑹", "⑺", "⑻", "⑼", "⑽", "⑾", "⑿", "⒀", "⒁", "⒂", "⒃", "⒄", "⒅", "⒆", "⒇", "⒈", "⒉", "⒊", "⒋", "⒌", "⒍", "⒎", "⒏", "⒐", "⒑", "⒒", "⒓", "⒔", "⒕", "⒖", "─", "━", "┃", "┄", "┆", "┈", "┉", "┊", "┋", "┌", "┍", "┎", "┏", "┐", "┑", "┒", "┓", "└", "┕", "┖", "┗", "┘", "┙", "┚", "┛", "├", "┝", "┞", "┟", "┠", "┡", "┢", "┣", "┤", "┥", "┦", "┧", "┨", "┩", "┪", "┫", "┬", "┭", "┮", "┯", "┰", "┱", "┲", "┳", "┴", "┻", "┼", "╂", "╋", "□", "△", "◆", "◇", "○", "◎", "●", "★", "☆", "♀", "、", "。", "〃", "々", "〈", "〉", "《", "》", "「", "」", "『", "』", "【", "】", "〓", "〖", "〗", "㈠", "㈡", "㈢", "㈣", "㈤", "㈥", "㈦", "㈧", "㈨", "㈩", "︿", "￠", "￥", "\t", "\n", "\r", " ", "\x0B", "⋯", "•", "−", "‚", "«", "〜"]

class full2half:
    def __ini__(self):
        pass
    def charB2Q(self, uchar):
        if uchar == '':
            return ''
        inside_code = ord(uchar)
        if not inside_code in range(32, 127):
            return uchar
        if inside_code == 32:
            inside_code = 12288
        else:
            inside_code += 65248
        if inside_code in range(32, 127):
            return uchar
        return unichr(inside_code).encode('utf-8', 'ignore')

    #将全角字符转换成半角字符
    def charQ2B(self, uchar):
        if uchar == '':
            return ''
        inside_code = ord(uchar)
        if inside_code in range(32, 127):
            return uchar
        if inside_code == 12288:
            inside_code = 32
        else:
            inside_code -= 65248
        if not inside_code in range(32, 127):
            return uchar
        return unichr(inside_code).encode('utf-8', 'ignore')

    #将字符串中的半角转换成全角
    def StingB2Q(self, ustring):
        try:
            ustring = ustring.decode('utf-8', 'ignore')
        except:
            pass
        result = ''
        for uchar in ustring:
            try:
                uchar = uchar.encode('utf-8', 'ignore')
            except:
                pass
            try:
                inside_code = ord(uchar)
            except:
                inside_code = ''
            if inside_code:
                if inside_code in range(32, 127):
                    result += self.charB2Q(uchar)
                else:
                    result += uchar
            else:
                result += uchar
        return result

    #将字符串中的全角转换成半角
    def StingQ2B(self, ustring):
        try:
            ustring = ustring.decode('utf-8', 'ignore')
        except:
            pass
        result = ''
        for uchar in ustring:
            try:
                inside_code = ord(uchar)
            except:
                inside_code = ''
            if inside_code:
                if inside_code in range(32, 127):
                    result += uchar
                else:
                    result += self.charQ2B(uchar)
            else:
                result += uchar
        return result.encode('utf-8', 'ignore')

    #析构函数
    def __del__(self):
        pass    

fhObj = full2half()
#返回的时候就已经变成unicode
def clean_tweet(str_f):
    str_f = fhObj.StingQ2B(str_f)
    
    str_f = re.sub(r"//\@.*[:：]", " ", str_f)
    #str_f = re.sub(r"//\@.*:", " ", str_f)
        
    identify = string.maketrans('', '')
    str_f = str(str_f).translate(identify, string.punctuation)
    
    str_f = cn_t_2_s.zh_simple(str_f)
    
    for it in rep_list:
        str_f = str_f.replace(it, ' ')

    #变成unicode
    str_f = ' '.join(re.findall(ur'[\u4e00-\u9fa5,\w]+', str_f.decode('utf-8')))
    
    return str_f
