#from tokenize import String
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tkinter import *
import webbrowser


# loading the data from the csv file to a pandas dataframe
movies_data = pd.read_csv('movies.csv')

# printing the first 5 rows of the dataframe
#print(movies_data.head()) 

selected_features = ['genres','keywords','tagline','cast','director']

for feature in selected_features:
  movies_data[feature] = movies_data[feature].fillna('')

combined_features = movies_data['genres']+' '+movies_data['keywords']+' '+movies_data['tagline']+' '+movies_data['cast']+' '+movies_data['director']


#convert text to vector value
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

#checks for similarity 
similarity = cosine_similarity(feature_vectors)

mshow_features = movies_data[['title','genres','overview','director','vote_average','homepage']].copy()

fd = {
    'title':[],
    'genres':[],
    'overview':[],
    'director':[],
    'vote_average':[],
    'homepage':[],
}
fdf = pd.DataFrame(fd)

def para(inp):
    new_input = ""
    for i, letter in enumerate(inp):
        if i % 70 == 0:
            new_input += '\n'
        new_input += letter
    new_input = new_input[1:]
    return new_input

def linkcheck(link,title):
  if link == 'nan':
    tlink = title
    tlink = tlink.replace(' ','+')
    link = "https://www.google.com/search?q="+tlink+"+movie"
  return link

def quitter(window):
    window.destroy()

#movie_name = input(' Enter your favourite movie name : ')

def recommender():
  global top_30
  top_30=[]
  movie_name = mv.get()
  list_of_all_titles = movies_data['title'].tolist()

  find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)

  close_match = find_close_match[0]

  index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]

  similarity_score = list(enumerate(similarity[index_of_the_movie]))

  sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 

  print('Movies suggested for you : \n')

  i = 1

  for movie in sorted_similar_movies:
    index = movie[0]
    title_from_index = movies_data[movies_data.index==index]['title'].values[0]
    if (i<30):
      top_30.append(title_from_index)
      i+=1
  print(top_30)
  search.destroy()
  return top_30




#movie="Avatar"

def moviedata(movie):
  for m in movie:
    for i,title in enumerate(mshow_features['title']):
      if title == m: #batman is just a test case will be replaced by variable later
          #print("this works")
          #print(i) #index number of the row which matched the name
          x = i 
          fdf.loc[mshow_features.index[x]] = mshow_features.iloc[x]
  nrows = fdf.shape[0]
  number = list(range(1,nrows+1))
  fdf['number'] = number
  fdf.set_index('number',inplace = True)
  print(fdf)

def quitter():
  sresult.destroy()

  



#name = input("Enter movie name: ")
#print(recommender(name))

search = Tk()
search.geometry("2560x1440")
search.title("Movie Recommendation System")
search.attributes('-fullscreen',True)
search.config(background="#121212")
mrs = Label(search, text ="Movie Recommendation System",font=("Calibri",30),bg="#121212",fg="#61C1B0").place(relx=0.5,rely=0.3,anchor=CENTER)

def temp_text(e):
   name.delete(0,"end")
bar = PhotoImage(file='images/searchbar.png')
namebg = Label(image=bar,bg="#121212")
namebg.place(relx=0.520,rely=0.45,anchor=CENTER)
mv = StringVar()
name = Entry(search,textvariable=mv,font=("Calibri",16),borderwidth=0)
name.insert(0, "Enter movie name")
name.place(relx=0.5,rely=0.45,anchor=CENTER,width=700,height=50)
name.bind("<FocusIn>", temp_text)

simg = PhotoImage(file='images/searchbutton.png')
sbutton = Button(search,image=simg,borderwidth=0,bg="white",command=recommender).place(relx=0.8,rely=0.45,anchor=CENTER)

search.mainloop()

moviedata(top_30)
  
green = "#F07067"
dname1 = str(fdf['director'][1])
dname2 = str(fdf['director'][2])
dname3 = str(fdf['director'][3])
dname4 = str(fdf['director'][4])
rate1 = str(fdf['vote_average'][1])
rate2 = str(fdf['vote_average'][2])
rate3 = str(fdf['vote_average'][3])
rate4 = str(fdf['vote_average'][4])
bgc = "#13141F"
textbg = "#6A7BFF"
titlefont = ("Calibri",25)
ovfont = ('Calibri 15 bold')
  
sresult = Tk()
sresult.geometry("2560x1440")
sresult.title("Movie Recommendation System")
sresult.attributes('-fullscreen',True)
sresult.config(background=bgc)


l1 = Label(sresult, text = str(fdf['title'][1]) ,font=titlefont,bg=bgc,fg=green,cursor="hand2")
link1 = str(fdf['homepage'][1])
title1 = str(fdf['title'][1])
link1 = linkcheck(link1,title1)
l1.bind('<Button-1>',lambda x:webbrowser.open_new(link1))
l1.place(x=60,y=50)
ovbgca = PhotoImage(file='images/ovbgc.png')
ovbgcl = Label(image=ovbgca,bg="#121212")
ovbgcl.place(x=30,y=100)
d1 = Text(sresult,font = ovfont,bg=textbg,fg="white",height=5,width=55,borderwidth=0)
d1.insert(1.0,str(fdf['overview'][1]))
d1.config(state=DISABLED)
d1.place(x=40,y=110)
drca = PhotoImage(file='images/drc.png')
drc1 = Label(image=drca,bg=textbg,borderwidth=0)
drc1.place(x=40,y=240)


director = Label(sresult, text = "Director: ",font=ovfont,bg=green,fg='white').place(x=50,y=250)
director_name = Label(sresult,text=dname1,font=ovfont,bg=green,fg='white').place(x=120,y=250)
rating = Label(sresult,text="Rating: ",font=ovfont,bg=green,fg='white').place(x=50,y=280)
rate_name = Label(sresult, text = rate1,font=ovfont,bg=green,fg='white').place(x=110,y=280) 

l2 = Label(sresult, text = str(fdf['title'][2]),font=titlefont,bg=bgc,fg=green,cursor="hand2")
link2 = str(fdf['homepage'][2])
title2 = str(fdf['title'][2])
link2 = linkcheck(link2,title2)
l2.bind('<Button-1>',lambda x:webbrowser.open_new(link2))
l2.place(x=60,y=370)
ovbgcb = PhotoImage(file='images/ovbgc.png')
ovbgc2 = Label(image=ovbgcb,bg="#121212")
ovbgc2.place(x=30,y=420)
d2 = Text(sresult, font = ovfont,bg=textbg,fg="white",height=5,width=55,borderwidth=0)
d2.insert(1.0,str(fdf['overview'][2]))
d2.config(state=DISABLED)
d2.place(x=40,y=430)
drcb = PhotoImage(file='images/drc.png')
drc2 = Label(image=drcb,bg=textbg,borderwidth=0)
drc2.place(x=40,y=560)
director = Label(sresult, text = "Director: ",font=ovfont,bg=green,fg='white').place(x=50,y=570)
director_name = Label(sresult,text=dname2,font=ovfont,bg=green,fg='white').place(x=130,y=570)
rating = Label(sresult,text="Rating: ",font=ovfont,bg=green,fg='white').place(x=50,y=600)
rate_name = Label(sresult, text = rate2,font=ovfont,bg=green,fg='white').place(x=110,y=600)

l3 = Label(sresult, text = str(fdf['title'][3]),font=titlefont,bg=bgc,fg=green,cursor="hand2")
link3 = str(fdf['homepage'][3])
title3 = str(fdf['title'][3])
link3 = linkcheck(link3,title3)
l3.bind('<Button-1>',lambda x:webbrowser.open_new(link3))
l3.place(x=660,y=50)
ovbgcc = PhotoImage(file='images/ovbgc.png')
ovbgc3 = Label(image=ovbgcc,bg="#121212")
ovbgc3.place(x=630,y=100)
d3 = Text(sresult,font = ovfont,bg=textbg,fg="white",height=5,width=55,borderwidth=0)
d3.insert(1.0,str(fdf['overview'][3]))
d3.config(state=DISABLED)
d3.place(x=640,y=110)
drcac = PhotoImage(file='images/drc.png')
drc3 = Label(image=drcac,bg=textbg,borderwidth=0)
drc3.place(x=640,y=240)
director = Label(sresult, text = "Director: ",font=ovfont,bg=green,fg='white').place(x=650,y=250)
director_name = Label(sresult,text=dname3,font=ovfont,bg=green,fg='white').place(x=720,y=250)
rating = Label(sresult,text="Rating: ",font=ovfont,bg=green,fg='white').place(x=650,y=280)
rate_name = Label(sresult, text = rate3,font=ovfont,bg=green,fg='white').place(x=710,y=280)

l4 = Label(sresult, text = str(fdf['title'][4]),font=titlefont,bg=bgc,fg=green,cursor="hand2")
link4 = str(fdf['homepage'][4])
title4 = str(fdf['title'][4])
link4 = linkcheck(link4,title4)
l4.bind('<Button-1>',lambda x:webbrowser.open_new(link4))
l4.place(x=660,y=370)
ovbgcd = PhotoImage(file='images/ovbgc.png')
ovbgc4 = Label(image=ovbgcd,bg="#121212")
ovbgc4.place(x=630,y=420)
d4 = Text(sresult, font = ovfont,bg=textbg,fg="white",height=5,width=55,borderwidth=0)
d4.insert(1.0,str(fdf['overview'][4]))
d4.config(state=DISABLED)
d4.place(x=640,y=430)
drcd = PhotoImage(file='images/drc.png')
drc4 = Label(image=drcd,bg=textbg,borderwidth=0)
drc4.place(x=640,y=560)
director = Label(sresult, text = "Director: ",font=ovfont,bg=green,fg='white').place(x=650,y=570)
director_name = Label(sresult,text=dname4,font=ovfont,bg=green,fg='white').place(x=720,y=570)
rating = Label(sresult,text="Rating: ",font=ovfont,bg=green,fg='white').place(x=650,y=600)
rate_name = Label(sresult, text = rate4,font=ovfont,bg=green,fg='white').place(x=710,y=600)

bye = PhotoImage(file='images/exit.png')
byebutton = Button(sresult,image=bye,borderwidth=0,bg="white",command=quitter,background=bgc).place(x=1100,y=650)

sresult.mainloop()
