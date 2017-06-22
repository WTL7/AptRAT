
import urllib2 # Used to read the html document
import csv
from bs4 import BeautifulSoup
from twilio.rest import Client

# Find these keys at https://twilio.com/user/account
account_sid = " "
auth_token = " "
client = Client(account_sid, auth_token)

target_type = 'Sunrise'

old_list = []
old_apt_id = []

# read old file to a list
with open('apt_mining_previous.csv', 'rb') as csvfile:
    origin_file = csv.reader(csvfile)
    for a in origin_file:
        old_list.append(' '.join(a))
        old_apt_id.append(a[0])
        
with open('apt_mining_previous.csv', 'rb') as csvfile:
    origin_file = csv.reader(csvfile)        
    old_traget_unit = [i[0] for i in origin_file if target_type in i[4]]        
        
url = 'https://bhmanagement-reslisting.securecafe.com/\
onlineleasing/vicino-on-the-lake-apartments/\
availableunits.aspx?control=1&myolePropertyID=539196&UnitCode=1122'

soup = BeautifulSoup(urllib2.urlopen(url))
       
apt_name = []
all_apt = []

for apt in soup.find_all('tbody'):
    all_apt.append(apt.text)    
    
for apt_n in soup.find_all('h3'):
    apt_name.append('Type: ' + apt_n.text[13:]) 

# use csv writer for output    
with open('apt_mining_update.csv', 'wb') as csvfile:
    file_writer = csv.writer(csvfile)
        
    for i in range(len(apt_name)):
        apt_unit = all_apt[i].split('#')
        apt_unit.remove('')
        
        for j in apt_unit:
            if '1 Bedroom' not in apt_name[i]:
                file_writer.writerow([j[:j.find('$')-4],
                j[j.find('$')-4:j.find('$')],j[j.find('$'):j.find('$',14)+6],
                j[j.find('$',14)+6:],apt_name[i]]) # NO. sq. price available type

  
   
new_list = []
new_apt_id = []              
                                              
#creat new list from updated file
with open('apt_mining_update.csv', 'rb') as csvfile:
   new_file = csv.reader(csvfile)
   for a in new_file:
      new_list.append(' '.join(a))
      new_apt_id.append(a[0])
      
with open('apt_mining_update.csv', 'rb') as csvfile:
   new_file = csv.reader(csvfile)   
   new_traget_unit = [i[0] for i in new_file if target_type in i[4]]                          

# show gone
gone = list(set(old_apt_id) - set(new_apt_id))

# show new add
new_add = list(set(new_apt_id) - set(old_apt_id))

# show difference    
difference_new = list(set(new_list) - set(old_list)) 
difference_new.sort() 
difference_old = list(set(old_list) - set(new_list))
difference_old.sort() 

# show gone target unit
target_gone = list(set(old_traget_unit) - set(new_traget_unit))
# show new target unit
target_new_add = list(set(new_traget_unit) - set(old_traget_unit))

with open('apt_mining_difference.csv', 'wb') as csvfile:
    file_writer = csv.writer(csvfile)
    
    print '---New Add:---'
    file_writer.writerow(['New_Add:'])
    for i in new_add:
        print i
        file_writer.writerow([i])
    file_writer.writerow([''])
    
    print '---Gone:---'
    file_writer.writerow(['Gone:'])    
    for k in gone:
        print k
        file_writer.writerow([k])
    file_writer.writerow([''])      
    
    print '---Difference:---'        
    file_writer.writerow(['Difference:'])
    file_writer.writerow(['-From-'])
    print '---From---'
    for j in difference_old:  
        print j     
        file_writer.writerow([j[:j.find('$')-4],
                j[j.find('$')-4:j.find('$')],j[j.find('$'):j.find('$',14)+6],
                j[j.find('$',14)+6:j.find('Type')],j[j.find('Type'):]])
    
    file_writer.writerow(['-To-'])
    print '---To---'
    for j in difference_new:  
        print j     
        file_writer.writerow([j[:j.find('$')-4],
                j[j.find('$')-4:j.find('$')],j[j.find('$'):j.find('$',14)+6],
                j[j.find('$',14)+6:j.find('Type')],j[j.find('Type'):]])
                
special_alram_unit = ['TF1014', 'TF1016', 'TF1018', 'TF1020', 'TF1022', 'TF1024']

key_patio_lake_unit = [i for i in special_alram_unit if i in new_apt_id]
                

# forming text (target type only)
text_combine = '*Lake_patio: ' + ','.join(key_patio_lake_unit) +\
     ' *New_add: ' + ','.join(target_new_add) + ' *Gone: ' + ','.join(target_gone)
     
'''     
if key_patio_lake_unit or target_new_add or target_gone:   # if anything changed
    #text message         
    message_1 = client.messages.create(to="+12174187609",
                                    from_="+12175744152",
                                    body= text_combine)
                                                
    message_2 = client.messages.create(to="+12177512436",
                                    from_="+12175744152",
                                    body= text_combine)   
else:
    print 'No change on Target Units...'                                     
'''    
# Update old files
# use csv writer for output    
with open('apt_mining_previous.csv', 'wb') as csvfile:
    file_writer = csv.writer(csvfile)
        
    for i in range(len(apt_name)):
        apt_unit = all_apt[i].split('#')
        apt_unit.remove('')
        
        for j in apt_unit:
            if '1 Bedroom' not in apt_name[i]:
                file_writer.writerow([j[:j.find('$')-4],
                j[j.find('$')-4:j.find('$')],j[j.find('$'):j.find('$',14)+6],
                j[j.find('$',14)+6:],apt_name[i]]) # NO. sq. price available type                                                                                                                                