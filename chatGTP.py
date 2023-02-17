# get statements formatted into dictionary
# statements formatted in {Question_ID : Question} format
statements_file = open("statements.txt", "r")
statements_array = statements_file.readlines()
statements = {}
for i in range(len(statements_array)):
    statements_array[i] = statements_array[i].strip()
for j in range(0, len(statements_array), 4):
    key = statements_array[j]
    statement = statements_array[j + 2]
    statements[key] = statement


# get subjects formatted into dictionary
# subjects formatted in {Subject_ID : [Subject 1, Subject 2, etc.]} format
subjects_file = open("subjects.txt", "r")
subjects_array = subjects_file.readlines()
subjects = {}
for i in range(len(subjects_array)):
    subjects_array[i] = subjects_array[i].strip()
counter = 0
while counter < len(subjects_array):
    key = subjects_array[counter]
    subjects[key] = []
    counter += 2
    while counter < len(subjects_array) and subjects_array[counter] != "":
        subjects[key].append(subjects_array[counter])
        counter += 1
    counter += 1

# get directives formatted into dicitonary
# directives formatted in [question/directive, [attatching directives]]
directives_file = open("directives.txt", "r")
directives_array = directives_file.readlines()
for i in range(len(directives_array)):
    directives_array[i] = directives_array[i].strip()
counter = 0
directives = []
while counter < len(directives_array):
    if(directives_array[counter] == "Directive:"):
        directives.append(["directive"])
        counter += 1
        while(counter < len(directives_array) and directives_array[counter] != ""):
            directives[-1].append(directives_array[counter])
            counter += 1
        counter += 1
        continue
    elif(directives_array[counter] == "Statement:"):
        directives.append(["statement"])
        counter += 1
        while(counter < len(directives_array) and directives_array[counter] != ""):
            directives[-1].append(directives_array[counter])
            counter += 1
        counter += 1
        continue
    else:
        counter += 1
# print(directives)
# given a directive, it formats it with the proper subject
# code is open to injection
# meant for user-friendlyness of directly putting in text file
def formatDirectiveSubject(directive, subjects):
    all_versions = [""]
    counter = 1
    while counter < len(directive):
        if (counter + 11) < len(directive):
            if '" + [' == directive[counter : counter + 5]:
                counter += 5
                subject = ""
                while counter < len(directive) and directive[counter : counter + 5] != '] + "':
                    subject += directive[counter]
                    counter += 1
                if subject in subjects:
                    new_all_versions = []
                    for word in subjects[subject]:
                        for old_word in all_versions:
                            new_all_versions.append(old_word + word)
                    all_versions = new_all_versions
                counter += 4
            else:
                for i in range(len(all_versions)):
                    all_versions[i] += directive[counter]
        else:
            for i in range(len(all_versions)):
                all_versions[i] += directive[counter]
        counter += 1
    for i in range(len(all_versions)):
        all_versions[i] = all_versions[i][:-1]
    return all_versions


# formatting directives
counter = 1
output = open("output.txt", "w")
for i in range(len(directives)):
    if(directives[i][0] == "statement"and len(directives[i]) > 1):
        for element in directives[i][1:]:
            output.write(statements[element] + "\n")
    if(directives[i][0] == "directive" and len(directives[i]) > 1):
        generated_statements = formatDirectiveSubject(directives[i][1], subjects)
        for question in generated_statements:
            output.write("Question " + str(counter) + ": " + question + "\n")
            counter += 1
output.close()