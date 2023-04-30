
def display(tache, filename):
    content = tache.read(filename)
    # Read the contents of the HTML file into a string
    with open('display_file.html', 'r') as file:
        html_string = file.read()

    # Define the text that you want to insert
    insert_text = 'Hello '*10

    # Find the location where you want to insert the text
    # In this example, we want to insert the text inside an element with class="file1"
    insert_location = html_string.find('class="file-1"') + len('class="file-1"') + 1
    tag_end = html_string.find('</', insert_location) 

    # Modify the HTML string to insert the desired text at the specified location
    modified_html_string = html_string[:insert_location] + insert_text + html_string[tag_end:]

    # Write the modified HTML string back to the file
    with open('display_file.html', 'w') as file:
        file.write(modified_html_string)

from runProg import RunProg
tache = RunProg("config.txt")
display(tache, "output.txt")