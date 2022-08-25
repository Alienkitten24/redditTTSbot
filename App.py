from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import ctypes
import os
from main import *
import validators


def SetSource(source):
    var_source.set(f"{source}")
    DrawFrame()


def DrawFrame():
    if var_source.get() == 'sub':
        label_url.grid_forget()
        entry_url.forget()

        label_subreddit.grid(row=3, column=0, columnspan=1, padx=form_padx, pady=form_pady, sticky='w')
        entry_subreddit.grid(row=3, column=1, columnspan=2, padx=form_padx, pady=form_pady, sticky='e')
        label_subSort.grid(row=4, column=0, columnspan=1, padx=form_padx, pady=10, sticky='w')
        option_subSort.grid(row=4, column=1, columnspan=2, padx=form_padx, pady=form_pady, sticky='e')
        label_timeSort.grid(row=5, column=0, columnspan=1, padx=form_padx, pady=10, sticky='w')
        option_timeSort.grid(row=5, column=1, columnspan=2, padx=form_padx, pady=form_pady, sticky='e')

    elif var_source.get() == 'url':
        label_subreddit.grid_forget()
        entry_subreddit.grid_forget()
        label_subSort.grid_forget()
        option_subSort.grid_forget()
        label_timeSort.grid_forget()
        option_timeSort.grid_forget()

        label_url.grid(row=3, column=0, columnspan=1, padx=form_padx, pady=form_pady, sticky='w')
        entry_url.grid(row=3, column=1, columnspan=2, padx=form_padx, pady=form_pady, sticky='e')

    label_commentSort.grid(row=6, column=0, columnspan=1, padx=form_padx, pady=10, sticky='w')
    option_commentSort.grid(row=6, column=1, columnspan=2, padx=form_padx, pady=form_pady, sticky='e')
    label_commentNum.grid(row=7, column=0, columnspan=1, padx=form_padx, pady=form_pady, sticky='w')
    entry_commentNum.grid(row=7, column=1, columnspan=2, padx=form_padx, pady=form_pady, sticky='e')
    label_footage.grid(row=8, column=0, columnspan=1, padx=form_padx, pady=form_pady, sticky='w')
    button_footage.grid(row=8, column=2, columnspan=1, padx=form_padx, pady=form_pady, sticky='e')
    label_footage_choice.grid(row=8, column=1, columnspan=1, padx=form_padx, pady=form_pady, sticky='e')
    button_submit.grid(row=9, column=0, columnspan=1, padx=form_padx, pady=welcome_pady, ipady=10, ipadx=30, sticky='w')


def OpenFile():
    root.filename = filedialog.askopenfilename(initialdir=f"{os.environ['USERPROFILE']}/downloads", filetypes=(
                    ("mp4 files", "*mp4"), ("mov files", "*mov"), ("all files", "*.*")))
    label_footage_choice.config(text=root.filename)


def Submit():
    var_success = "Please fill out all fields "
    try:
        if var_source.get() == 'sub':
            posts = getPosts(entry_subreddit.get().strip("r/"), var_subSort.get().lower(), 1,
                             sort_time.get(str(var_timeSort.get())))
            comments = getCommentsFromPost(posts, int(entry_commentNum.get()), var_commentSort.get().lower())
        elif var_source.get() == 'url':
            comments = getCommentsFromUrl(entry_url.get(), int(entry_commentNum.get()), var_commentSort.get().lower())


        createAudio(comments)
        var_success = "Success"
    except ConnectionError:
        print("bruh")

    label_status = Label(root, text=var_success)
    label_status.grid(row=10, column=0, columnspan=1, padx=form_padx, pady=welcome_pady, ipady=10, ipadx=30, sticky='w')




root = Tk()
root.title("Reddit TTS")
root.iconbitmap("reddit-logo.ico")
root.geometry("1200x700")
root.configure(bg='white')
Grid.columnconfigure(root, 0, weight=1)
ctypes.windll.shcore.SetProcessDpiAwareness(1)
root.tk.call('tk', 'scaling', 2.0)

welcome_padx = 20
welcome_pady = 20
form_padx = 20
form_pady = 10
bg_color = "white"

sort_sub = [
    "Top",
    "New",
    "Hot",
    "Controversial",
]

sort_comment = [
    "Top",
    "New",
    "Best",
    "Controversial",
]

sort_time = {
    "Now": "hour",
    "Today": "today",
    "Week": "week",
    "Month": "month",
    "Year": "year",
    "All Time": "all"
}


var_subSort = StringVar()
var_subSort.set(sort_sub[0])

var_commentSort = StringVar()
var_commentSort.set(sort_comment[0])

var_timeSort = StringVar()
var_timeSort.set("Today")

var_footage = StringVar()
var_footage.set("")

var_source = StringVar()
var_source.set("sub")



welcome = Label(root, text="Create Your Own Reddit TTS Video", font=("Impact", 20), background=bg_color)
welcome.grid(row=0, column=0, columnspan=3, padx=welcome_padx, pady=welcome_pady, sticky='w')

button_fromSub = Button(root, text="From Subreddit", command=lambda: SetSource('sub'))
button_fromSub.grid(row=1, column=0, columnspan=1, padx=form_padx, pady=form_pady, ipady=10, ipadx=10, sticky='w')

button_fromURL = Button(root, text="From URL", command=lambda: SetSource('url'))
button_fromURL.grid(row=2, column=0, columnspan=1, padx=form_padx, pady=form_pady, ipady=10, ipadx=17, sticky='w')

label_url = Label(root, text="URL:", font=("Helvetica", 12), background=bg_color)
entry_url = Entry(root, width=70)

label_subreddit = Label(root, text="Subreddit:", font=("Helvetica", 12), background=bg_color)
entry_subreddit = Entry(root, width=70)

label_subSort = Label(root, text="Sort Subreddit By:", font=("Helvetica", 12), background=bg_color)
option_subSort = OptionMenu(root, var_subSort, sort_sub[0], *sort_sub)

label_timeSort = Label(root, text="Sort Time By:", font=("Helvetica", 12), background=bg_color)
option_timeSort = OptionMenu(root, var_timeSort, "Today", *sort_time.keys())

label_commentSort = Label(root, text="Sort Comments By:", font=("Helvetica", 12), background=bg_color)
option_commentSort = OptionMenu(root, var_commentSort, sort_comment[0], *sort_comment)

label_commentNum = Label(root, text="Number Of Comments:", font=("Helvetica", 12), background=bg_color)
entry_commentNum = Entry(root, width=7)

label_footage = Label(root, text="Background Video:", font=("Helvetica", 12), background=bg_color)
button_footage = Button(root, text="Select A File", command=OpenFile)
label_footage_choice = Label(root, text=var_footage.get(), font=("Times New Roman", 10), background=bg_color, width=53)

button_submit = Button(root, text="Create", command=Submit)



root.mainloop()

