# coding: utf-8

import em_cal
import filer_clean

# present_text = "我爱北京天安门"
mood_labels = {0: "愤怒", 1: "厌恶", 2: "高兴", 3: "悲伤", -1: "无"}
texts = ["我爱北京美食", "这个人真讨厌", "今天下雨了，心情不好躲在家里", "怎么会有这样的人", "考试又挂了，怎么跟家里交代啊"]
for text in texts:
    filtered_text = filer_clean.clean_tweet(text)
    div_arr = em_cal.divide_unicode_str_jieba(filtered_text)
    mood = em_cal.nb_cls(filtered_text, div_arr)
    print text, ":", mood_labels[mood]
