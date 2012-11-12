import csv, os, sys

def dict_filter(it, *keys):
    for d in it:
        yield dict((k, d[k]) for k in keys)
        
thisdir = sys.path[0]
orig_file = raw_input("Enter Original Testplan File Name, including extension (should be .csv)")
orig_testplanfile = os.path.join(thisdir, orig_file)
results_file = raw_input("Enter Corresponding Testplan Results Name, including extension (should be .csv)")
results_testplanfile = os.path.join(thisdir, results_file)

#the output file assembles some of the original testplan info and merges it into the test plan results csv...
#this single file includes the original questions, Ids and expected results with the test plan responses for each test taker.
output_file = os.path.join(thisdir,orig_file.split(".")[0] + "_results." + orig_file.split(".")[1])

#build list of headers in results
with open(results_testplanfile,'rb') as results:
    headers = results.readline()
    headerlist = headers.split(',')
    
#headers for the results file, only including 'name' and date' plus any data fields
resultsheaders = [s for s in headerlist if 'Name' in s or 'Date' in s or '_data' in s]

#headers for original 
origheaders = ['Procedure_ID','Test_Procedure','Expected_Results']

#--------------------
#Remove extraneous data columns from test results csv.
results_filteredtestplanfile = os.path.join(thisdir,orig_file.split(".")[0] + "_filter." + orig_file.split(".")[1])

f_in = open(results_testplanfile,'rb')
f_out = open(results_filteredtestplanfile,'wb')

reader = csv.DictReader(f_in)
writer = csv.DictWriter(f_out,resultsheaders,extrasaction='ignore')
writer.writerow(dict((fn,fn) for fn in resultsheaders))
for line in reader:
    writer.writerow(line)

#transpose data in filtered test results csv, convert to list...
f = csv.reader(open(results_filteredtestplanfile))
f_transposed = zip(*f)
count = len(f_transposed)

#Open output csv file...
f_output = open(output_file, 'wb')
#open and read all testplan lines
f_testplan = open(orig_testplanfile)
testplan_lines = f_testplan.readlines()

i=0
while i < count:
    #Write the original file info (ID,Procedure,Results) then the test results (Name, James, Aja, Travis, etc).  The number of lines should match (skip the 
    f_output.write(testplan_lines[i].strip() + "," + ",".join(f_transposed[i][1:]) + "\n")
    i += 1

f_output.close()



