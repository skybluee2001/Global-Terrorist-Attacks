from flask import Flask,send_file,render_template
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np1
import pandas as pd
import csv
data=pd.read_csv('./globalterrorismdb_0718dist.csv',encoding = "ISO-8859-1")

plt.subplots(figsize=(17,8))
attack=data['country_txt'].value_counts()[:40].reset_index()
attack.columns=['Country','Total Attacks']
sns.barplot(x=attack['Country'],y= attack['Total Attacks'], palette = 'rocket')
plt.xticks(rotation=90)
plt.ylabel('Total Attacks')
plt.xlabel('Country')
plt.title('Total Attacks in Each Country',fontdict={'fontsize':17,'fontweight':'bold'})
plt.savefig('static/images/plot.png')

plt.subplots(figsize=(17,8))
attack1=data['country_txt'].value_counts()[:20].reset_index()
attack1.columns=['Country','Total Attacks']
plt.bar(attack1['Country'], attack1['Total Attacks'])
plt.xticks(rotation=90)
plt.ylabel('Total Attacks',fontdict={'fontsize':13,'fontweight':"bold"})
plt.xlabel('Country',fontdict={'fontsize':13,'fontweight':"bold"})
plt.title('Total Attacks in Each Country',fontdict={'fontsize':17,'fontweight':"bold"})
plt.savefig('static/images/plot1.png')

data.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','region_txt':'Region','attacktype1_txt':'Attack_Type','target1':'Target','nkill':'Killed','nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type','weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)
data=data[['Year','Month','Day','Country','Region','city','latitude','longitude','Attack_Type','Killed','Wounded','Target','Summary','Group','Target_type','Weapon_type','Motive']]
data['Casualities']=data['Killed']+data['Wounded']

casu=data.groupby('Country').Casualities.count().reset_index().sort_values('Casualities', ascending=False)[:40]
plt.subplots(figsize=(17,8))
plt.plot(casu.Country,casu.Casualities,linestyle='dashed',linewidth = 2, color='red', marker="o",markerfacecolor='blue', markersize=8)
plt.xticks(rotation=90)
plt.title('Total Casualties in Each Country',fontdict={'fontsize':20,'fontweight':'bold'})
plt.xlabel('Country',fontdict={'fontsize':13,'fontweight':"bold"})
plt.ylabel("Total Casualties",fontdict={'fontsize':13,'fontweight':"bold"})
plt.grid(color='black', linestyle='-', linewidth=0.2)
plt.savefig('static/images/plot3.png')

plt.subplots(figsize=(17,8))
sns.countplot('Year',data=data,palette='RdYlGn_r',edgecolor=sns.color_palette('dark',7))
plt.xticks(rotation=90)
plt.title('Number Of Terrorist Activities Each Year',fontdict={'fontsize':20,'fontweight':"bold"})
plt.ylabel("Total Attacks",fontdict={'fontsize':13,'fontweight':"bold"})
plt.xlabel("Year",fontdict={'fontsize':13,'fontweight':"bold"})
plt.savefig('static/images/plot4.png')

n=data.groupby(data['Attack_Type']).Casualities.count().reset_index()
n.columns=['Attack_Type','Casualities']
fig = plt.figure(figsize=[8, 8])
ax = fig.add_subplot(111)
ax.pie(n.Casualities,autopct='%.2f%%', startangle=90)
ax.set_title("Types of Attack that caused Casualties",fontdict={'fontsize':20,'fontweight':"bold"});
ax.legend(labels=n.Attack_Type,loc='upper right')
plt.savefig('static/images/plot2.png')

india_df=data[data.Country=='India']
city_attacks = india_df.city.value_counts().to_frame().reset_index()
city_attacks.columns = ['City', 'Total Attacks']
city_cas = india_df.groupby('city').Casualities.count().to_frame().reset_index()
city_cas.columns = ['City', 'Casualities']
city_tot = pd.merge(city_attacks, city_cas, how='left', on='City').sort_values('Total Attacks', ascending=False)[:21]
sns.set_palette('RdBu')
# plt.figure(figsize=(20,15))
city_tot.plot.bar(x='City', width=0.8)
plt.xticks(rotation=90)
plt.title('Number Of Total Attacks and Casualties by City in India')
plt.xlabel('Cities',fontdict={'fontsize':10,'fontweight':'bold'})
plt.ylabel('Total Attacks/Casualties',fontdict={'fontsize':10,'fontweight':'bold'})
plt.title('Number Of Total Attacks and Casualties by City in India',fontdict={'fontsize':10,'fontweight':'bold'})
# fig = plt.gcf()
fig.set_size_inches(15,15)
plt.savefig('static/images/plot5.png')

ind=india_df.groupby('Year').count().reset_index()
plt.figure(figsize=(17,8))
sns.barplot(x=ind['Year'],y=ind['Casualities'],palette='viridis')
plt.xticks(rotation=90)
plt.title('Total Number of Casualities per Year',fontdict={'fontsize':17,'fontweight':'bold'})
plt.xlabel('Year',fontdict={'fontsize':13,'fontweight':'bold'})
plt.ylabel('Casualties',fontdict={'fontsize':13,'fontweight':'bold'})
plt.savefig('static/images/plot6.png')

india_df['Casualities'] = india_df['Casualities'].fillna(0).astype(int)
india_df = india_df.sort_values(by='Casualities',ascending=False)[:60]
heat=india_df.pivot_table(index='city',columns='Year',values='Casualities')
plt.figure(figsize=(15,8))
heat.fillna(0,inplace=True)
sns.heatmap(heat,robust = True,linewidths=1,cmap='BuPu')
plt.xlabel('Year',fontdict={'fontsize':13,'fontweight':'bold'})
plt.ylabel('Cities',fontdict={'fontsize':13,'fontweight':'bold'})
plt.title('Casualties for a particular Year & City in India',fontdict={'fontsize':20,'fontweight':'bold'})
plt.savefig('static/images/plot7.png')

ind=india_df.groupby('Year').count().reset_index()
plt.figure(figsize=(17,9))
sns.barplot(x=ind.Year,y=ind['Casualities'],palette='Blues_d')
plt.ylabel('Casualties in India',fontdict={'fontsize':13,'fontweight':'bold'})
plt.xlabel('Year',fontdict={'fontsize':13,'fontweight':'bold'})
plt.title('Total Number of Casualties in India',fontdict={'fontsize':20,'fontweight':'bold'})
plt.savefig('static/images/plot8.png')

plt.figure(figsize=(20,8))
sns.barplot(x=india_df.Target.value_counts(), y=india_df.Target.value_counts().index,order = india_df.Target.value_counts().iloc[1:25].index,palette="viridis")
plt.title("Target Types of the attacks in India",fontdict={'fontsize':13,'fontweight':'bold'})
plt.savefig('static/images/plot9.png')

import folium
from folium.plugins import MarkerCluster
filyr = data.Year == 1991
fildata = data[filyr]
reqFildata = fildata.loc[:,'city':'longitude']
reqFildata = reqFildata.dropna()
reqList = reqFildata.values.tolist()

mp = folium.Map(location = [0, 15], tiles='CartoDB positron', zoom_start=5)
markerCluster = folium.plugins.MarkerCluster().add_to(mp)
for point in range(0, len(reqList)):
    folium.Marker(location=[reqList[point][1],reqList[point][2]],popup = reqList[point][0]).add_to(markerCluster)



a=[]
for i in range(1,21):
    t=data.iloc[i];
    a.append(t)

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',headings=data.columns[:12],data=a)

if __name__ == "__main__":
    app.run(debug=True)


