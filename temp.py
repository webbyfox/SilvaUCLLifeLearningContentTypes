list=context.objectValues('Silva Publication')
output=''
## Get ids assigned in that folder.

list2=[]

for x in list:
 # if x.meta_type=='Silva Publication':
#  print 'TITLE: ', x.get_title(), 'ID: ', x.getId(), 'CREATION TIME: ', x.get_creation_datetime()
  cr_date=x.get_creation_datetime()
  cr_date=str(cr_date).split(' ')
  cr_date=cr_date[0]
  cr_date=cr_date[:-3]
  item=[cr_date, x.getId(), x.get_title(), x.sec_get_userids(),x.get_local_roles()]
  list2.append(item)    

list2.sort()

#for item in list2:
#   item[0]=item[0].strftime("%B %Y")

months=[]
i=0
j=0
k=list2[0][0]
for l in list2:
   if l[0]==k:
       i=i+1
   if l[0]!=k:
       m=[i, k]
       months.append(m)
       k=l[0]
       i=1
       j=j+1
total=0
print '<table><tr><th>Month</th><th>No. of New Publications</th>'
for month in months:
    mymonth=int(month[1].split('/')[1])
    myyear=month[1].split('/')[0]
    values = { 1: 'Jan', 2: 'Feb', 3: 'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    mymonth=values.get(mymonth, 0)
    #print mymonth
    mydate=mymonth+' '+myyear

    print '<tr><td>', mydate, '</td><td>', '---'*month[0], month[0], '</td></tr>'
    total=total+month[0]
print '</table>'
print '<p>Total: %s' % total
    

print '<table><tr><th>TITLE</th><th>ID</th><th>CREATION DATE</th><th>ASSIGNED USERS</th><th>ASSIGNED ROLES</th></tr>'
for y in list2:
  print '<tr><td>', y[2],'</td><td>', y[1], '</td><td>', y[0], '</td><td>', y[3],'</td><td>', y[4],'</td><td>'
  
  print '<table><tr><th>User</th><th>Role</th></tr>'
  for user, role user in y[4].items():
       print '<tr><td>',user,'</td><td>',role,'</td></tr>'
  print '</table>'    
print '</td></tr></table>'
return printed
