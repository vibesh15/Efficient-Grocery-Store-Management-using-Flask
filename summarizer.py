import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

from youtube_transcript_api import YouTubeTranscriptApi

import tkinter as tk
from tkinter import *
from tkinter import scrolledtext

from translate import Translator

from gtts import gTTS
import os
from threading import Timer
import sys
from PIL import Image, ImageTk

import time
import psutil

start_time = time.time()

cpu_percent = psutil.cpu_percent()
memory_info = psutil.virtual_memory()

print(f"CPU Usage: {cpu_percent}%")
print(f"Memory Usage: {memory_info.percent}%")

summary = ""
nlp = ""


def sumarize():    
    url = ytUrl.get()
    size = clicked.get()

    youtube_video = url

    video_id = youtube_video.split("=")[1]

    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    text = ""
    for i in transcript:
        text += i['text'] + ' '

    stopwords = list(STOP_WORDS)

    global nlp

    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)

    tokens = [token.text for token in doc]

    pun = punctuation + '\n' + ' '

    word_frequencies = {}

    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in pun:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_tokens = [sent for sent in doc.sents]

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]

                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]

    global summary

    from heapq import nlargest

    if size in ['Small']:
        select_length = int(len(sentence_tokens) * 0.3)


    elif size in ['Medium']:
        select_length = int(len(sentence_tokens) * 0.4)

    else:
        select_length = int(len(sentence_tokens) * 0.5)

    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)

    final_summary = [word.text for word in summary]

    summary = ' '.join(final_summary)

    sum = nlp(summary)
    summary_sentences = [sent for sent in sum.sents]
    summary_arr_len = int(len(summary_sentences))

    paragraph_one = int(summary_arr_len / 4)
    paragraph_two = int(summary_arr_len / 2)
    paragraph_three = int(3 * summary_arr_len / 4)
    paragraph_four = int(summary_arr_len - 1)

    text_area.delete('1.0', END)

    for x in range(0, paragraph_one):
        text_area.insert(tk.INSERT, summary_sentences[x])
        # text_area.insert(tk.INSERT, ". ")

    text_area.insert(tk.INSERT, "\n\n")

    for x in range(paragraph_one, paragraph_two):
        text_area.insert(tk.INSERT, summary_sentences[x])
        # text_area.insert(tk.INSERT, ". ")

    text_area.insert(tk.INSERT, "\n\n")

    for x in range(paragraph_two, paragraph_three):
        text_area.insert(tk.INSERT, summary_sentences[x])
        # text_area.insert(tk.INSERT, ". ")

    text_area.insert(tk.INSERT, "\n\n")

    for x in range(paragraph_three, paragraph_four):
        text_area.insert(tk.INSERT, summary_sentences[x])
        # text_area.insert(tk.INSERT, ". ")

    text_area.insert(tk.INSERT, "\n\n")


'''
# %%
def translateEngToSin():
    global summary

    summary_new = summary

    text_area.delete('1.0', END)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(summary_new)

    translator = Translator(to_lang="si")

    for sent in doc.sents:
        tr = sent.text
        translation = translator.translate(tr)
        text_area.insert(tk.INSERT, translation)
        text_area.insert(tk.INSERT, ". \n\n")
'''

# %%
def translateEngToTamil():
    global summary

    summary_new = summary

    text_area.delete('1.0', END)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(summary_new)

    translator = Translator(to_lang="ta")

    for sent in doc.sents:
        tr = sent.text
        translation = translator.translate(tr)
        text_area.insert(tk.INSERT, translation)
        text_area.insert(tk.INSERT, ". \n\n")


# %%
# Add English voice to the summarize text
def speakEnglish():
    global summary

    summary_new = summary

    text_area.delete('1.0', END)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(summary_new)

    eng_text = ""

    for sent in doc.sents:
        tr = sent.text
        text_area.insert(tk.INSERT, tr)
        text_area.insert(tk.INSERT, ". \n\n")
        eng_text = eng_text + tr

        audio_file_path = 'audio_cache/a.mp3'
    
    if not os.path.exists(audio_file_path):
        tts = gTTS(eng_text, lang='en')
        tts.save(audio_file_path)

    os.system(audio_file_path)

    def removeAudio():
        os.remove(audio_file_path)

    t = Timer(3600, removeAudio)
    t.start()
    exit(True)

'''
    tts = gTTS(eng_text, lang='en')
    tts.save('a.mp3')
    os.system('a.mp3')

    def removeAudio():
        os.remove('a.mp3')

    t = Timer(3600, removeAudio)
    t.start()
    exit(True)
'''    

'''
# %%
# Add Sinhal voice to the summarize text
def speakSinhala():
    global summary

    summary_new = summary

    text_area.delete('1.0', END)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(summary_new)

    translator = Translator(to_lang="si")

    eng_text = ""

    for sent in doc.sents:
        tr = sent.text
        translation = translator.translate(tr)
        text_area.insert(tk.INSERT, translation)
        text_area.insert(tk.INSERT, ". \n\n")
        eng_text = eng_text + translation

    tts = gTTS(eng_text, lang='si')
    tts.save('a.mp3')
    os.system('a.mp3')

    def removeAudio():
        os.remove('a.mp3')

    t = Timer(3600.0, removeAudio)
    t.start()
    exit(True)
'''

# %%
# Add Tamil voice to the summarize text
def speakTamil():
    global summary

    summary_new = summary

    text_area.delete('1.0', END)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(summary_new)

    translator = Translator(to_lang="ta")

    eng_text = ""

    for sent in doc.sents:
        tr = sent.text
        translation = translator.translate(tr)
        text_area.insert(tk.INSERT, translation)
        text_area.insert(tk.INSERT, ". \n\n")
        eng_text = eng_text + translation

    tts = gTTS(eng_text, lang='ta')
    tts.save('a.mp3')
    os.system('a.mp3')

    def removeAudio():
        os.remove('a.mp3')

    t = Timer(3600.0, removeAudio)
    t.start()
    exit(True)


# %%
def searchWordInPara():
    global summary
    global nlp

    summary_new = summary

    word = searchWord.get()

    nlp = spacy.load('en_core_web_sm')

    doc = nlp(summary_new)

    words = [token.text for token in doc]
    for x in words:
        if word in words:
            lbl_text.delete('1.0', END)
            lbl_text.insert(tk.INSERT, "Key word that you are\nsearching, is in\nthe summary")
            break
        elif word not in words:
            lbl_text.delete('1.0', END)
            lbl_text.insert(tk.INSERT, "Key word that you are\nsearching, is not\nin the summary")
            break


# %%
root = tk.Tk()
root.title("  YouTube Transcript Summarizer")
root.iconbitmap("C:\\Users\\VarshaVibesh\\OneDrive - SRM Institute of Science and Technology\\Desktop\\project\\icon\\logo_icon_2.ico")
# root.geometry("1312x600")
root.resizable(False, False)

main_frame = tk.Frame(root, bg="#0a192f")
main_frame.grid(row=0, column=0)

frame_one = tk.Frame(main_frame, bg="#0a192f", padx=10, pady=10, bd=1)
frame_one.grid(row=0, column=0)

frame_two = tk.Frame(main_frame, bg="#0a192f", padx=10, pady=10, bd=1, highlightbackground="white",
                     highlightthickness=1)
frame_two.grid(row=0, column=1)

frame_three = tk.Frame(main_frame, bg="#0a192f", padx=10, pady=10, bd=1)
frame_three.grid(row=0, column=2)

# images for buttons

# images for translation button

global imgEnglish
'''global imgSinhala'''
global imgTamil

imgEng = Image.open("C:\\Users\\VarshaVibesh\\OneDrive - SRM Institute of Science and Technology\\Desktop\\project\\icon\\button_trans_eng.png")

resized_imageE = imgEng.resize((120, 40), Image.LANCZOS)
imgEnglish = ImageTk.PhotoImage(resized_imageE)

'''
imgSin = (Image.open("icon/button_trans_sin.png"))
resized_imageS = imgSin.resize((120, 40), Image.LANCZOS)
imgSinhala = ImageTk.PhotoImage(resized_imageS)
'''
imgTam = Image.open("C:\\Users\\VarshaVibesh\\OneDrive - SRM Institute of Science and Technology\\Desktop\\project\\icon\\button_trans_tam.png")

resized_imageT = imgTam.resize((120, 40), Image.LANCZOS)
imgTamil = ImageTk.PhotoImage(resized_imageT)

# images for voice button

global imgVoiceEng
'''global imgVoiceSin'''
global imgVoiceTam

imgVoiEng = Image.open("C:\\Users\\VarshaVibesh\\OneDrive - SRM Institute of Science and Technology\\Desktop\\project\\icon\\button_voi_eng.png")

resized_imageVoiEng = imgVoiEng.resize((120, 40), Image.LANCZOS)
imgVoiceEng = ImageTk.PhotoImage(resized_imageVoiEng)
'''
imgVoiSin = (Image.open("icon/button_voi_sin.png"))
resized_imageVoiSin = imgVoiSin.resize((120, 40), Image.LANCZOS)
imgVoiceSin = ImageTk.PhotoImage(resized_imageVoiSin)
'''
imgVoiTam = Image.open(r"C:\Users\VarshaVibesh\OneDrive - SRM Institute of Science and Technology\Desktop\project\icon\button_voi_tam.png")

resized_imageVoiTam = imgVoiTam.resize((120, 40), Image.LANCZOS)
imgVoiceTam = ImageTk.PhotoImage(resized_imageVoiTam)

# images for summary and search button

global imgSummary
global imgSearch

imgSum = Image.open(r"C:\Users\VarshaVibesh\OneDrive - SRM Institute of Science and Technology\Desktop\project\icon\button_sum.png")

resized_imageSum = imgSum.resize((120, 40), Image.LANCZOS)
imgSummary = ImageTk.PhotoImage(resized_imageSum)

imgSer = Image.open(r"C:\Users\VarshaVibesh\OneDrive - SRM Institute of Science and Technology\Desktop\project\icon\button_search.png")

resized_imageSer = imgSer.resize((120, 40), Image.LANCZOS)
imgSearch = ImageTk.PhotoImage(resized_imageSer)

# images for hover effect

# hover translate images

global imgEnglishHover
'''global imgSinhalaHover'''
global imgTamilHover

imgEngHover = Image.open(r"C:\Users\VarshaVibesh\OneDrive - SRM Institute of Science and Technology\Desktop\project\icon\button_trans_eng_hov.png")

resized_imageEHover = imgEngHover.resize((120, 40), Image.LANCZOS)
imgEnglishHover = ImageTk.PhotoImage(resized_imageEHover)

'''imgSinHover = (Image.open("icon/button_trans_sin_hov.png"))
resized_imageSHover = imgSinHover.resize((120, 40), Image.LANCZOS)
imgSinhalaHover = ImageTk.PhotoImage(resized_imageSHover)'''

imgTamHover = Image.open(r"C:\Users\VarshaVibesh\OneDrive - SRM Institute of Science and Technology\Desktop\project\icon\button_trans_tam_hov.png")

resized_imageTHover = imgTamHover.resize((120, 40), Image.LANCZOS)
imgTamilHover = ImageTk.PhotoImage(resized_imageTHover)

# hover voice images

global imgVoiceEngHover
'''global imgVoiceSinHover'''
global imgVoiceTamHover

imgVoiEngHover = Image.open(r"C:\Users\VarshaVibesh\OneDrive - SRM Institute of Science and Technology\Desktop\project\icon\button_voi_eng_hov.png")

resized_imageVoiEngHover = imgVoiEngHover.resize((120, 40), Image.LANCZOS)
imgVoiceEngHover = ImageTk.PhotoImage(resized_imageVoiEngHover)

'''imgVoiSinHover = (Image.open("icon/button_voi_sin_hov.png"))
resized_imageVoiSinHover = imgVoiSinHover.resize((120, 40), Image.LANCZOS)
imgVoiceSinHover = ImageTk.PhotoImage(resized_imageVoiSinHover)'''

imgVoiTamHover = Image.open(r"C:\Users\VarshaVibesh\OneDrive - SRM Institute of Science and Technology\Desktop\project\icon\button_voi_tam_hov.png")

resized_imageVoiTamHover = imgVoiTamHover.resize((120, 40), Image.LANCZOS)
imgVoiceTamHover = ImageTk.PhotoImage(resized_imageVoiTamHover)

# hover serach and summary button

global imgSummaryHover
global imgSearchHover

imgSumHover = Image.open(r"C:\Users\VarshaVibesh\OneDrive - SRM Institute of Science and Technology\Desktop\project\icon\button_sum_hov.png")

resized_imageSumHover = imgSumHover.resize((120, 40), Image.LANCZOS)
imgSummaryHover = ImageTk.PhotoImage(resized_imageSumHover)

imgSerHover = Image.open(r"C:\Users\VarshaVibesh\OneDrive - SRM Institute of Science and Technology\Desktop\project\icon\button_search_hov.png")

resized_imageSerHover = imgSerHover.resize((120, 40), Image.LANCZOS)
imgSearchHover = ImageTk.PhotoImage(resized_imageSerHover)

# image for logo
imgLogo = Image.open(r"C:\Users\VarshaVibesh\OneDrive - SRM Institute of Science and Technology\Desktop\project\icon\logo_img_4.png")

resized_imageL = imgLogo.resize((300, 200), Image.LANCZOS)
imgLogo = ImageTk.PhotoImage(resized_imageL)

# Frame One

# logo image
logo = Label(frame_one, image=imgLogo, bd=0)
logo.grid(row=0, column=0)

lbl = Label(frame_one, text="", bg="#0a192f", padx=20, pady=20)
lbl.grid(row=1, column=0)

lbl = Label(frame_one, text="Translate the summarized\nparagraph to your\nnative language",
            font=("Arial", 18, "bold"), bg="#0a192f", fg="#FFB700")
lbl.grid(row=2, column=0)

lbl = Label(frame_one, text="", bg="#0a192f")
lbl.grid(row=3, column=0)

btn_en_f1 = tk.Button(frame_one, image=imgEnglish, bg="#0a192f", borderwidth=0, command=sumarize)
btn_en_f1.grid(row=4, column=0)

lbl = Label(frame_one, text="", bg="#0a192f")
lbl.grid(row=5, column=0)

'''btn_sin_f1 = tk.Button(frame_one, image=imgSinhala, bg="#0a192f", borderwidth=0, command=translateEngToSin)
btn_sin_f1.grid(row=6, column=0)'''

lbl = Label(frame_one, text="", bg="#0a192f")
lbl.grid(row=7, column=0)

btn_tam_f1 = tk.Button(frame_one, image=imgTamil, bg="#0a192f", borderwidth=0, command=translateEngToTamil)
btn_tam_f1.grid(row=8, column=0)

lbl = Label(frame_one, text="", bg="#0a192f")
lbl.grid(row=9, column=0)

# Frame Two

lbl = Label(frame_two, text="Enter the url of the YouTube video",
            font=("Arial", 18, "bold"), bg="#0a192f", fg="#FFB700", padx=10, pady=2)
lbl.grid(row=0, column=0)

# url entry box
ytUrl = Entry(frame_two, font=("Arial", 15), width=50, bd=0)
ytUrl.config(bg="#124c82", bd=0, fg="white")
ytUrl.grid(row=1, column=0, padx=15, pady=15)

# dropdown menu
clicked = StringVar()
clicked.set("Small")

drop = OptionMenu(frame_two, clicked, "Small", "Medium", "Large")
drop.config(bg="lightblue", bd=0, fg="black", activeforeground="white", activebackground="#3f60f4",
            font=("Arial", 10, "bold"))
drop.grid(row=2, column=0)

lbl = Label(frame_two, text="", bg="#0a192f")
lbl.grid(row=3, column=0)

# Summarize button
btn_summ = tk.Button(frame_two, image=imgSummary, bg="#0a192f", bd=0, borderwidth=0, command=sumarize)
btn_summ.grid(row=4, column=0)

lbl = Label(frame_two, text="", bg="#0a192f")
lbl.grid(row=5, column=0)

# summarize text field
text_area = scrolledtext.ScrolledText(frame_two, fg="white", wrap=tk.WORD, font=("Arial", 13),
                                      width=70, height=20, padx=20, pady=20, bg="#124c82")
text_area.grid(row=6, column=0)

lbl = Label(frame_two, text="", bg="#0a192f")
lbl.grid(row=7, column=0)

# Frame Three

lbl = Label(frame_three, text="", bg="#0a192f")
lbl.grid(row=0, column=0)

lbl = Label(frame_three, text="Search the words\nthat you looking for", font=("Arial", 18, "bold"), bg="#0a192f",
            fg="#FFB700")
lbl.grid(row=1, column=0)

searchWord = Entry(frame_three, font=("Arial", 13), width=20)
searchWord.config(bg="#124c82", bd=0, fg="white")
searchWord.grid(row=2, column=0, padx=15, pady=15)

btn_search = tk.Button(frame_three, image=imgSearch, bg="#0a192f", borderwidth=0, command=searchWordInPara)
btn_search.grid(row=3, column=0)

lbl = Label(frame_three, text="", bg="#0a192f")
lbl.grid(row=4, column=0)

lbl_text = Text(frame_three, padx=12, pady=12, width=20, fg="white", height=3, bd=0, bg="#124c82", font=("Arial", 12))
lbl_text.grid(row=5, column=0)

lbl = Label(frame_three, text="", bg="#0a192f", padx=20, pady=0)
lbl.grid(row=6, column=0)

lbl = Label(frame_three, text="You can listen to the\nsummarized paragraph", font=("Arial", 18, "bold"),
            bg="#0a192f", fg="#FFB700")
lbl.grid(row=7, column=0)

lbl = Label(frame_three, text="", bg="#0a192f")
lbl.grid(row=8, column=0)

btn_en_f3 = tk.Button(frame_three, image=imgVoiceEng, text="", padx=10, pady=5, bg="#0a192f", bd=0,
                      command=speakEnglish)
btn_en_f3.grid(row=9, column=0)

lbl = Label(frame_three, text="", bg="#0a192f")
lbl.grid(row=10, column=0)

'''btn_sin_f3 = tk.Button(frame_three, image=imgVoiceSin, text="", padx=10, pady=5, bg="#0a192f", bd=0,
                       command=speakSinhala)
btn_sin_f3.grid(row=11, column=0)'''

lbl = Label(frame_three, text="", bg="#0a192f")
lbl.grid(row=12, column=0)

btn_tam_f3 = tk.Button(frame_three, image=imgVoiceTam, text="", padx=10, pady=5, bg="#0a192f", bd=0, command=speakTamil)
btn_tam_f3.grid(row=13, column=0)

lbl = Label(frame_three, text="", bg="#0a192f")
lbl.grid(row=14, column=0)


# Hover effect on buttons

# btn_en_f1
def on_enter_btn_en_f1(e):
    global imgEnglishHover
    btn_en_f1.config(image=imgEnglishHover)


def on_leave_btn_en_f1(e):
    global imgEnglish
    btn_en_f1.config(image=imgEnglish)


btn_en_f1.bind("<Enter>", on_enter_btn_en_f1)
btn_en_f1.bind("<Leave>", on_leave_btn_en_f1)

'''
# btn_sin_f1
def on_enter_btn_sin_f1(e):
    global imgSinhalaHover
    btn_sin_f1.config(image=imgSinhalaHover)


def on_leave_btn_sin_f1(e):
    global imgSinhala
    btn_sin_f1.config(image=imgSinhala)


btn_sin_f1.bind("<Enter>", on_enter_btn_sin_f1)
btn_sin_f1.bind("<Leave>", on_leave_btn_sin_f1)
'''

# btn_tam_f1
def on_enter_btn_tam_f1(e):
    global imgTamilHover
    btn_tam_f1.config(image=imgTamilHover)


def on_leave_btn_tam_f1(e):
    global imgTamil
    btn_tam_f1.config(image=imgTamil)


btn_tam_f1.bind("<Enter>", on_enter_btn_tam_f1)
btn_tam_f1.bind("<Leave>", on_leave_btn_tam_f1)


# btn_en_f3
def on_enter_btn_en_f3(e):
    global imgVoiceEngHover
    btn_en_f3.config(image=imgVoiceEngHover)


def on_leave_btn_en_f3(e):
    global imgVoiceEng
    btn_en_f3.config(image=imgVoiceEng)


btn_en_f3.bind("<Enter>", on_enter_btn_en_f3)
btn_en_f3.bind("<Leave>", on_leave_btn_en_f3)

'''
# btn_sin_f3
def on_enter_btn_sin_f3(e):
    global imgVoiceSinHover
    btn_sin_f3.config(image=imgVoiceSinHover)


def on_leave_btn_sin_f3(e):
    global imgVoiceSin
    btn_sin_f3.config(image=imgVoiceSin)


btn_sin_f3.bind("<Enter>", on_enter_btn_sin_f3)
btn_sin_f3.bind("<Leave>", on_leave_btn_sin_f3)
'''

# btn_tam_f3
def on_enter_btn_tam_f3(e):
    global imgVoiceTamHover
    btn_tam_f3.config(image=imgVoiceTamHover)


def on_leave_btn_tam_f3(e):
    global imgVoiceTam
    btn_tam_f3.config(image=imgVoiceTam)


btn_tam_f3.bind("<Enter>", on_enter_btn_tam_f3)
btn_tam_f3.bind("<Leave>", on_leave_btn_tam_f3)


# btn_summary_f2
def on_enter_btn_summary_f2(e):
    global imgSummaryHover
    btn_summ.config(image=imgSummaryHover)


def on_leave_btn_summary_f2(e):
    global imgSummary
    btn_summ.config(image=imgSummary)


btn_summ.bind("<Enter>", on_enter_btn_summary_f2)
btn_summ.bind("<Leave>", on_leave_btn_summary_f2)


# btn_serch_f3
def on_enter_btn_serch_f33(e):
    global imgSearchHover
    btn_search.config(image=imgSearchHover)


def on_leave_btn_serch_f3(e):
    global imgSearch
    btn_search.config(image=imgSearch)


btn_search.bind("<Enter>", on_enter_btn_serch_f33)
btn_search.bind("<Leave>", on_leave_btn_serch_f3)


# https://www.youtube.com/watch?v=ob6IlbV13IM&t=82s
# %%
# https://www.youtube.com/watch?v=cisZV4LTvFE
# %%
root.mainloop()

end_time = time.time()

execution_time = end_time - start_time
print(f"Summarization completed in {execution_time:.2f} seconds")
