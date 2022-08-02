#!/usr/bin/env python3
'''
Script to resolve wordpress format from DOI.
The script downloads metadata associated with provided DOI from crossref.org and restructures the data to the correct format used for publishing on the wordpress website 'https://www.socat.info/index.php/publications/'
 
'''
import json
import urllib.request
import re
import os
import sys
import pyperclip

file = open('citations.txt', 'w')  # Retrieved citations are written to this file.
file.write('correctly formatted citations to be published on the website socat.info \n')

[A,Y,T,J,V,P,DOI] = ['','year', 'title', 'journal', 'volume(issue)', 'pages', 'DOI']  #information required to write the ciation
doi = input('enter DOI: ')
moreDOI = True

while moreDOI:
    authorDict = {}
    [A,Y,T,J,V,P,DOI] = ['','year','title','journal','volume(issue)','pages','DOI']
    try:
      url = 'https://api.crossref.org/works/' + str(doi)  #retrieving metadata from crossref.org
      response = urllib.request.urlopen(url)
      data = json.loads(response.read().decode('utf-8'))
      wp_format = '<p class=\"citation\">'
      
      #retrieving data from json-file
      try:
        for index,author in enumerate(data['message']['author']):
            authorDict[index] = {"lastName":author['family'], "firstName":author['given']}
            authorDict[index]['firstName'] = re.sub('[a-z]+', '.',authorDict[index]['firstName'])

            # REFORMATTING AUTHORNAMES
            initials = '' 
            for letter in authorDict[index]['firstName']:
                if letter.islower(): #ignore lower case letters
                   var = ''; 
                elif letter.isupper(): #uppercase
                  initials += letter + '.' #append uppercase followed by period to initials
                else:
                  initials += letter #append other symbols
            
            initials = re.sub('\-','&#8209;',initials)  #replace hyphen with non-breaking hyphen to avoid line-break
            initials = re.sub('\.\.','.',initials)  # remove instances of double-period (occurs when json-files contain only initials)

            A += authorDict[index]['lastName'] + ',&nbsp;' + initials  # constructing author-field
            if index < len(data['message']['author'])-2:
              A = A + ', '
            elif index == len(data['message']['author'])-2: #'and' between two final authors.
              A += ' and '
      except KeyError as e: 
        print('Case encountered: ',e ,' Check author field in final citation for errors...')

      # YEAR 
      Y = str(data['message']['created']['date-parts'][0][0])
      wp_format += A + '(' + Y + '). '

      # TITLE
      try: 
        T = str(data['message']['title'][0])
        T = re.sub('&lt;','<',T)
        T = re.sub('&gt;','>',T) #fixes HTML-formatting-issues
      except UnicodeEncodeError as e: 
        print('Error importing title. Please check for errors.')
        print('Error message: ',e)
        input('Press Enter to confirm you have read the error-message...')
        T = re.sub(r'[^\x00-\x7F]+',r' *** ',data['message']['title'][0])
        pass
      T = re.sub(r'\n','',T) #removes new-lines from title. 
      wp_format += '<span class=\"articleTitle\">' + T + '.</span> '

      # JOURNAL
      try:
        J = str(data['message']['container-title'][0])
        wp_format += '<span class=\"journalTitle\">' + J + '</span>'
      except:
        pass
 
      #VOLUME, ISSUE, PAGE-NUMBERS
      try: 
        V = str(data['message']['volume'])
        wp_format += ', <span class=\"vol\">' + V
        try: 
          I = str(data['message']['issue'])
          wp_format += '(' + I + ')</span>'
        except(KeyError): 
          wp_format += '</span>'
          print('--- No Issue ---')
          pass
      except(KeyError): 
        print('--- No Volume(Issue) ---')
        pass
      try: 
        P = str(data['message']['page'])
        P = re.sub('\-','&#8209;',P) #non-breaking hyphen between page-numbers
        wp_format += ', ' + P 
      except(KeyError): 
        print('--- No pages ---')
        pass
      
      DOIdisp = re.sub('\-','&#8209;',doi) # DOI as displayed on website, non-breaking hyphen. Not suitable for link-generation
      wp_format += ('. <a href=\"https://doi.org/{:s}\" target=\"_blank\" rel=\"noopener\"> doi:{:s}</a>.</p>').format(doi,DOIdisp)

      # creating citation format used on wordpress website: socat.info
      print ("This is the correct format: \n \n " + wp_format  +'\n')
      pyperclip.copy(wp_format) #copies the citation to your clipboard. 

      #Ask for more input
      done = input("Do you have more DOIs to check? y/n " )
      if re.match('y',done):
        doi = input("enter next DOI: ")
      elif re.match('1',done[0]): 
        doi = done
      else: moreDOI = False

    except ValueError as e:
      print ("Could not find a article connected to this DOI: " + doi) 
      print(e)
      file.write('\n Article with DOI:' + doi + ' could not be retrieved.\n') 
      break

    except KeyError as e:
      print ("A value must be entered,",e)
      doi = input   ("enter DOI: " )
    except Exception as e: 
        print(e); 
        print('Failed to run. Encountered: ',e)
        exc_type, exc_obj, exc_tb = sys.exc_info()

        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        break

