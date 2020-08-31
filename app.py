from flask import Flask,render_template,url_for,request
import pickle
import PyPDF2 as pdf
import flashtext
from flashtext import KeywordProcessor
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/searchpdf',methods=['POST'])
def searchpdf():
    if request.method == 'POST':
        search_string = request.form['search_string']

        pdfFiles = []
        for filename in os.listdir('Data_Set'):
            if(filename.endswith('.pdf')):
                pdfFiles.append(filename)
        
        keyword_processor = KeywordProcessor()      
        list_pdf_files = []

        if(search_string.find("AND")):
            substring = search_string.split(' AND ')
            search_words = []
            for i in substring:
                keyword_processor.add_keyword(i)
                search_words.append(i)
    
            for filename in pdfFiles:
    
                pdfFileObj = open(os.path.join('.\Data_Set', filename), 'rb')
                pdf_reader = pdf.PdfFileReader(pdfFileObj)

                pg_num = pdf_reader.getNumPages()
                #print(pg_num)
                extracted_list = []

                for i in range(pg_num):
                    page = pdf_reader.getPage(i)
                    text = page.extractText()
                    #print(text)
                    extracted_list_perpg = keyword_processor.extract_keywords(text)
                
                    extracted_list.extend(extracted_list_perpg)
                    check =  all(item in extracted_list for item in search_words) 
                    if check is True:
                        list_pdf_files.append(filename)
                        break
                    
        #print(list_pdf_files)
    
    

        else:
            if(search_string.find("OR")):
                substring = search_string.split(' OR ')
            else:
                substring = [search_string]
        
            for i in substring:
                keyword_processor.add_keyword(i)
                search_words.append(i)
        
            for filename in pdfFiles:
    
                pdfFileObj = open(os.path.join('.\Data_Set', filename), 'rb')
                pdf_reader = pdf.PdfFileReader(pdfFileObj)

                pg_num = pdf_reader.getNumPages()
                #print(pg_num)    

                for i in range(pg_num):
                    page = pdf_reader.getPage(i)
                    text = page.extractText()
                    #print(text)
                    extracted_list = keyword_processor.extract_keywords(text)
                    if(extracted_list != []):
                        break    

                if(extracted_list != []):
                    list_pdf_files.append(filename) 

    return render_template('result.html', list_pdf_files_ = list_pdf_files, len = len(list_pdf_files))

if __name__ == '__main__':
	app.run(debug=True)

